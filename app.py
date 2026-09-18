"""
REX Insurance — Visitor Management System
Backend API (Flask + PostgreSQL)

Run locally:
    pip install -r requirements.txt
    python app.py

Deploy on Render:
    Start command: gunicorn app:app
"""

import os
import secrets
from datetime import datetime, timezone

import psycopg2
import psycopg2.extras
import requests
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================================
# Config
# ============================================================
DATABASE_URL = "postgres://avnadmin:AVNS_q_zR9FvhvJHJGbiL0zp@pg-235735e2-ub7499710-7253.j.aivencloud.com:11602/defaultdb?sslmode=require"
MISTRAL_API_KEY = "uZIGi6VCzkcJ0i5X5mYYc0Nr1XWX21YR"
MISTRAL_MODEL = os.environ.get("MISTRAL_MODEL", "mistral-small-latest")
FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "*")  # set to your Vercel URL in production

# Fallback default passcodes — ONLY used the very first time the app runs,
# to seed the database. Change them immediately from the Admin portal after
# your first login. Never trust these in a real deployment.
DEFAULT_PASSCODES = {
    "security": os.environ.get("SECURITY_PASSCODE", "Security#2026"),
    "frontdesk": os.environ.get("FRONTDESK_PASSCODE", "FrontDesk#2026"),
    "admin": os.environ.get("ADMIN_PASSCODE", "Admin#2026"),
}

DEFAULT_CONCURRENCY = {"security": 1, "frontdesk": 2, "admin": 1}
MAX_CONCURRENCY_CEILING = 2

VALID_PORTALS = {"security", "frontdesk", "admin"}

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": FRONTEND_ORIGIN}}, supports_credentials=False)


# ============================================================
# Database helpers
# ============================================================
def get_db():
    """One connection per request, closed automatically after."""
    if "db" not in g:
        g.db = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Creates every table if it doesn't already exist, and seeds defaults.
    Safe to run every time the app starts — CREATE TABLE IF NOT EXISTS never
    wipes existing data.
    """
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rexvms_portal_passcodes (
            portal TEXT PRIMARY KEY,
            passcode_hash TEXT NOT NULL,
            updated_at TIMESTAMPTZ DEFAULT now()
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rexvms_concurrency_limits (
            portal TEXT PRIMARY KEY,
            max_sessions INT NOT NULL DEFAULT 1
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rexvms_sessions (
            id SERIAL PRIMARY KEY,
            portal TEXT NOT NULL,
            display_name TEXT NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMPTZ DEFAULT now(),
            last_seen TIMESTAMPTZ DEFAULT now(),
            active BOOLEAN DEFAULT TRUE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rexvms_login_history (
            id SERIAL PRIMARY KEY,
            portal TEXT NOT NULL,
            display_name TEXT NOT NULL,
            logged_in_at TIMESTAMPTZ DEFAULT now(),
            logged_out_at TIMESTAMPTZ
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rexvms_staff_roster (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active',
            created_at TIMESTAMPTZ DEFAULT now()
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rexvms_visitors (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            id_type TEXT NOT NULL,
            id_number TEXT NOT NULL,
            registered_at TIMESTAMPTZ DEFAULT now()
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rexvms_visits (
            id SERIAL PRIMARY KEY,
            visitor_id INT REFERENCES rexvms_visitors(id) ON DELETE CASCADE,
            department TEXT NOT NULL,
            host TEXT NOT NULL,
            purpose TEXT NOT NULL,
            appt_type TEXT NOT NULL DEFAULT 'walkin',
            checkin TIMESTAMPTZ NOT NULL DEFAULT now(),
            checkout TIMESTAMPTZ,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMPTZ DEFAULT now()
        );
    """)

    # Seed default passcodes only if a portal doesn't have one yet
    for portal, code in DEFAULT_PASSCODES.items():
        cur.execute("SELECT 1 FROM rexvms_portal_passcodes WHERE portal = %s", (portal,))
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO rexvms_portal_passcodes (portal, passcode_hash) VALUES (%s, %s)",
                (portal, generate_password_hash(code)),
            )

    # Seed default concurrency limits only if missing
    for portal, limit in DEFAULT_CONCURRENCY.items():
        cur.execute("SELECT 1 FROM rexvms_concurrency_limits WHERE portal = %s", (portal,))
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO rexvms_concurrency_limits (portal, max_sessions) VALUES (%s, %s)",
                (portal, limit),
            )

    conn.commit()
    cur.close()
    conn.close()


# ============================================================
# Auth helpers
# ============================================================
def get_token_from_header():
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:].strip()
    return None


def get_session(token):
    if not token:
        return None
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM rexvms_sessions WHERE token = %s AND active = TRUE", (token,))
    return cur.fetchone()


def require_portal(portal_name):
    """Checks the request carries a valid, active session token for the given portal."""
    token = get_token_from_header()
    session = get_session(token)
    if not session or session["portal"] != portal_name:
        return None
    # touch last_seen so Admin's "active sessions" view reflects real activity
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE rexvms_sessions SET last_seen = now() WHERE id = %s", (session["id"],))
    db.commit()
    return session


def require_admin():
    return require_portal("admin")


# ============================================================
# Health check / cold-start warm-up ping
# ============================================================
@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "time": datetime.now(timezone.utc).isoformat()})


# ============================================================
# Auth routes
# ============================================================
@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json(force=True) or {}
    portal = data.get("portal")
    passcode = data.get("passcode", "")
    name = (data.get("name") or "").strip()

    if portal not in VALID_PORTALS:
        return jsonify({"error": "Unknown portal."}), 400
    if not name or len(name) < 2:
        return jsonify({"error": "Enter your name to continue."}), 400
    if not passcode:
        return jsonify({"error": "Passcode is required."}), 400

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT passcode_hash FROM rexvms_portal_passcodes WHERE portal = %s", (portal,))
    row = cur.fetchone()
    if not row or not check_password_hash(row["passcode_hash"], passcode):
        return jsonify({"error": "Incorrect passcode."}), 401

    cur.execute("SELECT max_sessions FROM rexvms_concurrency_limits WHERE portal = %s", (portal,))
    limit_row = cur.fetchone()
    max_sessions = limit_row["max_sessions"] if limit_row else DEFAULT_CONCURRENCY.get(portal, 1)

    cur.execute("SELECT COUNT(*) AS c FROM rexvms_sessions WHERE portal = %s AND active = TRUE", (portal,))
    active_count = cur.fetchone()["c"]

    if active_count >= max_sessions:
        return jsonify({
            "error": f"{portal.capitalize()} portal is at capacity ({max_sessions} active). "
                     f"Ask an Admin to force-logout a stuck session if this seems wrong."
        }), 423  # 423 Locked

    token = secrets.token_urlsafe(32)
    cur.execute(
        "INSERT INTO rexvms_sessions (portal, display_name, token) VALUES (%s, %s, %s) RETURNING id",
        (portal, name, token),
    )
    cur.execute(
        "INSERT INTO rexvms_login_history (portal, display_name) VALUES (%s, %s)",
        (portal, name),
    )
    db.commit()

    return jsonify({"token": token, "portal": portal, "name": name})


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    token = get_token_from_header()
    session = get_session(token)
    if not session:
        return jsonify({"ok": True})  # already logged out, nothing to do

    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE rexvms_sessions SET active = FALSE WHERE id = %s", (session["id"],))
    cur.execute("""
        UPDATE rexvms_login_history SET logged_out_at = now()
        WHERE portal = %s AND display_name = %s AND logged_out_at IS NULL
        ORDER BY logged_in_at DESC LIMIT 1
    """, (session["portal"], session["display_name"]))
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/auth/verify", methods=["GET"])
def verify():
    token = get_token_from_header()
    session = get_session(token)
    if not session:
        return jsonify({"valid": False}), 401
    return jsonify({"valid": True, "portal": session["portal"], "name": session["display_name"]})


# ============================================================
# Visitors (used by Security portal)
# ============================================================
@app.route("/api/visitors", methods=["GET"])
def list_visitors():
    if not require_portal("security"):
        return jsonify({"error": "Unauthorized"}), 401
    q = request.args.get("search", "").strip().lower()
    db = get_db()
    cur = db.cursor()
    if q:
        cur.execute("""
            SELECT * FROM rexvms_visitors
            WHERE LOWER(name) LIKE %s OR phone LIKE %s OR LOWER(id_number) LIKE %s
            ORDER BY registered_at DESC
        """, (f"%{q}%", f"%{q}%", f"%{q}%"))
    else:
        cur.execute("SELECT * FROM rexvms_visitors ORDER BY registered_at DESC")
    return jsonify(cur.fetchall())


@app.route("/api/visitors", methods=["POST"])
def create_visitor():
    if not require_portal("security"):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json(force=True) or {}
    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    id_type = (data.get("idType") or "").strip()
    id_number = (data.get("idNumber") or "").strip()

    if len(name) < 2 or not phone.isdigit() or len(phone) != 11 or not id_type or len(id_number) < 3:
        return jsonify({"error": "Invalid visitor details."}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO rexvms_visitors (name, phone, id_type, id_number)
        VALUES (%s, %s, %s, %s) RETURNING *
    """, (name, phone, id_type, id_number))
    visitor = cur.fetchone()
    db.commit()
    return jsonify(visitor), 201


@app.route("/api/visitors/<int:visitor_id>", methods=["PUT"])
def update_visitor(visitor_id):
    if not require_portal("security"):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json(force=True) or {}
    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    id_type = (data.get("idType") or "").strip()
    id_number = (data.get("idNumber") or "").strip()

    if len(name) < 2 or not phone.isdigit() or len(phone) != 11 or len(id_number) < 3:
        return jsonify({"error": "Invalid visitor details."}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE rexvms_visitors SET name=%s, phone=%s, id_type=%s, id_number=%s
        WHERE id=%s RETURNING *
    """, (name, phone, id_type, id_number, visitor_id))
    visitor = cur.fetchone()
    db.commit()
    if not visitor:
        return jsonify({"error": "Visitor not found."}), 404
    return jsonify(visitor)


@app.route("/api/visitors/<int:visitor_id>/visits", methods=["GET"])
def visitor_visits(visitor_id):
    if not require_portal("security"):
        return jsonify({"error": "Unauthorized"}), 401
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM rexvms_visits WHERE visitor_id = %s ORDER BY checkin DESC", (visitor_id,))
    return jsonify(cur.fetchall())


@app.route("/api/visitors/<int:visitor_id>/visits", methods=["POST"])
def log_visit(visitor_id):
    if not require_portal("security"):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json(force=True) or {}
    department = (data.get("department") or "").strip()
    host = (data.get("host") or "").strip()
    purpose = (data.get("purpose") or "").strip()
    appt_type = data.get("apptType", "walkin")

    if not department or not host or not purpose:
        return jsonify({"error": "Department, host, and purpose are required."}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO rexvms_visits (visitor_id, department, host, purpose, appt_type, status)
        VALUES (%s, %s, %s, %s, %s, 'pending') RETURNING *
    """, (visitor_id, department, host, purpose, appt_type))
    visit = cur.fetchone()
    db.commit()
    return jsonify(visit), 201


# ============================================================
# Visits (used by Front Desk portal — the live status board)
# ============================================================
VALID_TRANSITIONS = {
    "pending": {"hold", "approved", "rejected"},
    "hold": {"hold", "approved", "rejected"},
    "approved": {"with-host"},
    "with-host": {"checked-out"},
    "rejected": set(),
    "checked-out": set(),
}


@app.route("/api/visits", methods=["GET"])
def board_visits():
    if not require_portal("frontdesk"):
        return jsonify({"error": "Unauthorized"}), 401
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT v.*, vi.name AS visitor_name, vi.phone AS visitor_phone
        FROM rexvms_visits v JOIN rexvms_visitors vi ON vi.id = v.visitor_id
        WHERE v.checkin >= CURRENT_DATE
        ORDER BY v.checkin DESC
    """)
    return jsonify(cur.fetchall())


@app.route("/api/visits/<int:visit_id>", methods=["PATCH"])
def update_visit_status(visit_id):
    if not require_portal("frontdesk"):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json(force=True) or {}
    new_status = data.get("status")

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM rexvms_visits WHERE id = %s", (visit_id,))
    visit = cur.fetchone()
    if not visit:
        return jsonify({"error": "Visit not found."}), 404

    allowed = VALID_TRANSITIONS.get(visit["status"], set())
    if new_status not in allowed:
        return jsonify({"error": f"Cannot move from '{visit['status']}' to '{new_status}'."}), 400

    if new_status == "checked-out":
        cur.execute(
            "UPDATE rexvms_visits SET status=%s, checkout=now() WHERE id=%s RETURNING *",
            (new_status, visit_id),
        )
    else:
        cur.execute(
            "UPDATE rexvms_visits SET status=%s WHERE id=%s RETURNING *",
            (new_status, visit_id),
        )
    updated = cur.fetchone()
    db.commit()
    return jsonify(updated)


# ============================================================
# Admin routes
# ============================================================
@app.route("/api/admin/stats", methods=["GET"])
def admin_stats():
    if not require_admin():
        return jsonify({"error": "Unauthorized"}), 401
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT COUNT(*) AS c FROM rexvms_visits WHERE checkin >= CURRENT_DATE")
    today = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) AS c FROM rexvms_visits WHERE status IN ('approved', 'with-host')")
    inside = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) AS c FROM rexvms_visits WHERE status IN ('pending', 'hold')")
    pending = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) AS c FROM rexvms_visits WHERE checkin >= date_trunc('month', now())")
    month = cur.fetchone()["c"]

    cur.execute("""
        SELECT host, COUNT(*) AS visits FROM rexvms_visits
        WHERE checkin >= now() - interval '7 days'
        GROUP BY host ORDER BY visits DESC LIMIT 5
    """)
    performance = cur.fetchall()

    cur.execute("""
        SELECT v.id, vi.name AS visitor_name, v.status, v.host, v.created_at
        FROM rexvms_visits v JOIN rexvms_visitors vi ON vi.id = v.visitor_id
        ORDER BY v.created_at DESC LIMIT 8
    """)
    activity = cur.fetchall()

    return jsonify({
        "visitorsToday": today,
        "currentlyInside": inside,
        "pendingApprovals": pending,
        "visitorsThisMonth": month,
        "staffPerformance": performance,
        "recentActivity": activity,
    })


@app.route("/api/admin/visits", methods=["GET"])
def admin_all_visits():
    if not require_admin():
        return jsonify({"error": "Unauthorized"}), 401
    q = request.args.get("search", "").strip().lower()
    limit = min(int(request.args.get("limit", 20)), 100)
    offset = int(request.args.get("offset", 0))

    db = get_db()
    cur = db.cursor()
    base = """
        SELECT v.*, vi.name AS visitor_name FROM rexvms_visits v
        JOIN rexvms_visitors vi ON vi.id = v.visitor_id
    """
    where = ""
    params = []
    if q:
        where = " WHERE LOWER(vi.name) LIKE %s OR LOWER(v.host) LIKE %s OR LOWER(v.department) LIKE %s "
        params = [f"%{q}%", f"%{q}%", f"%{q}%"]

    cur.execute(f"SELECT COUNT(*) AS c FROM ({base}{where}) sub", params)
    total = cur.fetchone()["c"]

    cur.execute(f"{base}{where} ORDER BY v.checkin DESC LIMIT %s OFFSET %s", params + [limit, offset])
    rows = cur.fetchall()

    return jsonify({"total": total, "rows": rows})


@app.route("/api/admin/roster", methods=["GET"])
def get_roster():
    if not require_admin():
        return jsonify({"error": "Unauthorized"}), 401
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM rexvms_staff_roster ORDER BY created_at DESC")
    return jsonify(cur.fetchall())


@app.route("/api/admin/roster", methods=["POST"])
def add_roster_member():
    if not require_admin():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json(force=True) or {}
    name = (data.get("name") or "").strip()
    role = data.get("role")
    if len(name) < 2 or role not in VALID_PORTALS:
        return jsonify({"error": "Valid name and role are required."}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO rexvms_staff_roster (name, role) VALUES (%s, %s) RETURNING *",
        (name, role),
    )
    member = cur.fetchone()
    db.commit()
    return jsonify(member), 201


@app.route("/api/admin/roster/<int:member_id>", methods=["PATCH"])
def toggle_roster_member(member_id):
    if not require_admin():
        return jsonify({"error": "Unauthorized"}), 401
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM rexvms_staff_roster WHERE id = %s", (member_id,))
    member = cur.fetchone()
    if not member:
        return jsonify({"error": "Not found."}), 404
    new_status = "suspended" if member["status"] == "active" else "active"
    cur.execute(
        "UPDATE rexvms_staff_roster SET status=%s WHERE id=%s RETURNING *",
        (new_status, member_id),
    )
    updated = cur.fetchone()
    db.commit()
    return jsonify(updated)


@app.route("/api/admin/sessions", methods=["GET"])
def active_sessions():
    if not require_admin():
        return jsonify({"error": "Unauthorized"}), 401
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM rexvms_sessions WHERE active = TRUE ORDER BY created_at DESC")
    return jsonify(cur.fetchall())


@app.route("/api/admin/sessions/<int:session_id>/force-logout", methods=["POST"])
def force_logout(session_id):
    if not require_admin():
        return jsonify({"error": "Unauthorized"}), 401
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM rexvms_sessions WHERE id = %s", (session_id,))
    session = cur.fetchone()
    if not session:
        return jsonify({"error": "Session not found."}), 404
    cur.execute("UPDATE rexvms_sessions SET active = FALSE WHERE id = %s", (session_id,))
    # FIX: PostgreSQL doesn't support ORDER BY / LIMIT directly on UPDATE
    # (that's MySQL syntax). Wrapped in a subquery instead — SELECT supports
    # ORDER BY/LIMIT, so it picks the right row first, then UPDATE targets
    # that row by id. This was silently breaking the whole request before,
    # which also meant the "UPDATE rexvms_sessions SET active = FALSE" line above
    # never actually committed either — the transaction failed and rolled
    # back entirely, so the session was never really deactivated.
    cur.execute("""
        UPDATE rexvms_login_history SET logged_out_at = now()
        WHERE id = (
            SELECT id FROM rexvms_login_history
            WHERE portal = %s AND display_name = %s AND logged_out_at IS NULL
            ORDER BY logged_in_at DESC LIMIT 1
        )
    """, (session["portal"], session["display_name"]))
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/admin/login-history", methods=["GET"])
def login_history():
    if not require_admin():
        return jsonify({"error": "Unauthorized"}), 401
    limit = min(int(request.args.get("limit", 50)), 200)
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM rexvms_login_history ORDER BY logged_in_at DESC LIMIT %s", (limit,))
    return jsonify(cur.fetchall())


@app.route("/api/admin/passcode", methods=["POST"])
def change_passcode():
    if not require_admin():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json(force=True) or {}
    portal = data.get("portal")
    new_passcode = data.get("newPasscode", "")
    if portal not in VALID_PORTALS or len(new_passcode) < 4:
        return jsonify({"error": "Valid portal and a passcode of at least 4 characters are required."}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "UPDATE rexvms_portal_passcodes SET passcode_hash=%s, updated_at=now() WHERE portal=%s",
        (generate_password_hash(new_passcode), portal),
    )
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/admin/concurrency", methods=["GET"])
def get_concurrency():
    if not require_admin():
        return jsonify({"error": "Unauthorized"}), 401
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM rexvms_concurrency_limits")
    return jsonify(cur.fetchall())


@app.route("/api/admin/concurrency", methods=["POST"])
def set_concurrency():
    if not require_admin():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json(force=True) or {}
    portal = data.get("portal")
    max_sessions = data.get("maxSessions")
    if portal not in VALID_PORTALS or not isinstance(max_sessions, int) or not (1 <= max_sessions <= MAX_CONCURRENCY_CEILING):
        return jsonify({"error": f"maxSessions must be between 1 and {MAX_CONCURRENCY_CEILING}."}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "UPDATE rexvms_concurrency_limits SET max_sessions=%s WHERE portal=%s",
        (max_sessions, portal),
    )
    db.commit()
    return jsonify({"ok": True})


# ============================================================
# AI Guide — powered by Mistral, one endpoint shared by all 3 portals.
# Each portal sends its own name + a short description of its features
# (kept in GUIDE_CONTEXT below) so answers stay grounded to what the
# software actually does, instead of the model guessing.
# ============================================================
GUIDE_CONTEXT = {
    "security": """
You are the in-app help assistant for the Security Portal of REX Insurance's
Visitor Management System. This portal lets gate security staff:
- View a table of all previously registered visitors (name, phone, ID type/number, date registered)
- Search visitors by name, phone, or ID number
- Click "Register Visitor" to add a brand-new visitor to the system
- Click any visitor row to either "Log a New Visit" (records department, host,
  purpose, check-in/out time — this is sent to Front Desk for approval) or
  "View All Visits" (that visitor's full visit history)
- Edit an existing visitor's stored details from the table
Answer only based on these actual features. If asked about something this
portal doesn't do (like approving visitors — that's Front Desk's job), say so
plainly and point to the right portal.
""",
    "frontdesk": """
You are the in-app help assistant for the Front Desk Portal of REX Insurance's
Visitor Management System. This portal shows a live Visitor Status Board of
everyone Security has checked in today. Front Desk staff:
- See each visitor's status: Pending Review, Hold, Approved, With Host, Rejected, Checked Out
- Click a visitor row to open actions valid for their current stage:
  check host availability, then Accept / Reject / Hold on the host's behalf
  (Front Desk calls or messages the host directly — there's no separate host login)
- Mark a visitor "With Host" once they've reached the host's office
- Check the visitor out once they leave
- Filter the board by status and search by visitor or host name
Answer only based on these actual features.
""",
    "admin": """
You are the in-app help assistant for the Admin Portal of REX Insurance's
Visitor Management System. This portal has four sections:
- Dashboard: visitor counts (today/month), who's currently inside, pending
  approvals, a staff performance chart, and a recent activity feed
- Users & Roles: a staff roster (name, role, active/suspended) — this is a
  directory only, it is NOT connected to portal login
- Visitor Logs: the complete all-time visit history, loaded in batches of 20
  with a "Load more" button, searchable across the full history
- Reports: export buttons for Daily/Monthly/Staff/Performance reports (PDF/Excel)
- Session control: view who is logged into each portal right now, force-logout
  a stuck session, change any portal's passcode, view login history, and
  adjust each portal's concurrency limit (max 2 people at once per portal)
Answer only based on these actual features.
""",
}


@app.route("/api/ai/ask", methods=["POST"])
def ai_ask():
    data = request.get_json(force=True) or {}
    portal = data.get("portal")
    question = (data.get("question") or "").strip()

    if portal not in GUIDE_CONTEXT:
        return jsonify({"error": "Unknown portal."}), 400
    if not question:
        return jsonify({"error": "Ask a question first."}), 400
    if not MISTRAL_API_KEY:
        return jsonify({"error": "AI guide isn't configured on the server yet (missing MISTRAL_API_KEY)."}), 503

    try:
        resp = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {MISTRAL_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MISTRAL_MODEL,
                "messages": [
                    {"role": "system", "content": GUIDE_CONTEXT[portal] + "\nKeep answers short — 2-4 sentences, plain language, no markdown headers."},
                    {"role": "user", "content": question},
                ],
                "max_tokens": 300,
                "temperature": 0.3,
            },
            timeout=20,
        )
        resp.raise_for_status()
        answer = resp.json()["choices"][0]["message"]["content"]
        return jsonify({"answer": answer})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"AI guide is temporarily unavailable ({str(e)})."}), 502


# ============================================================
# Startup
# ============================================================
init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)