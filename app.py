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
DATABASE_URL = os.environ.get("DATABASE_URL")
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
MISTRAL_MODEL = "open-mistral-nemo"  # the only model that works for this app — not overridable via env
FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required.")
if not FRONTEND_ORIGIN:
    raise RuntimeError("FRONTEND_ORIGIN environment variable is required (e.g. https://rex-vms.vercel.app).")

# Initial passcodes — ONLY read when a portal has no passcode in the database yet
# (first run). After that, passcodes are managed from the Admin portal and these
# variables are ignored.
DEFAULT_PASSCODES = {
    "security": os.environ.get("SECURITY_PASSCODE"),
    "frontdesk": os.environ.get("FRONTDESK_PASSCODE"),
    "admin": os.environ.get("ADMIN_PASSCODE"),
}

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
            if not code:
                raise RuntimeError(f"No passcode stored for '{portal}' and no {portal.upper()}_PASSCODE env var set to seed it.")
            cur.execute(
                "INSERT INTO rexvms_portal_passcodes (portal, passcode_hash) VALUES (%s, %s)",
                (portal, generate_password_hash(code)),
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


# ============================================================
# AI Guide — powered by Mistral, one endpoint shared by all 3 portals.
# Each portal sends its own name + a short description of its features
# (kept in GUIDE_CONTEXT below) so answers stay grounded to what the
# software actually does, instead of the model guessing.
# ============================================================
SWITCH_NOTE = """
- Switching portals: the top of the page (and the login screen) has links to the two other portals. Each portal has its own separate login and passcode; if the person is already logged in to that portal in this browser, they continue where they left off.
- The round "?" button at the bottom-right opens this help guide."""

GUIDE_RULES = """
Rules:
- Answer ONLY from the feature list above. Never invent buttons, menus, settings, reports or abilities that are not listed.
- If the feature list does not cover the question, say you are not sure and suggest asking an administrator.
- If the question is unrelated to using this portal, say you can only help with using this portal.
- You cannot perform actions, look up real visitor data, or see the screen. You only explain how the portal works.
- Keep answers short: 2-4 sentences, plain language. For how-to questions give the steps in order.
- Do not use markdown headings.
"""

GUIDE_CONTEXT = {
    "security": """
You are the in-app help assistant for the Security Portal of REX Insurance's Visitor Management System. Gate security staff use it. What the portal actually does:
- Login: staff enter their name and the security passcode.
- Registered Visitors table: every visitor ever registered (full name, phone number, ID type, ID number, date registered) with a record count.
- Search box: filters the table by name, phone number, or ID number.
- Register Visitor button: opens a form for a first-time visitor — full name (letters only; spaces, hyphens and apostrophes allowed), an 11-digit phone number, ID type (National ID (NIN), Driver's License, International Passport, or Voter's Card) and ID number.
- Edit button on a row: updates that visitor's stored details.
- Clicking a visitor row opens two choices: "Add New Visit" and "View All Visits".
- Add New Visit: a form where Security picks Walk-in or Scheduled, chooses the department (Claims, Underwriting, Customer Relations, Finance, IT, Executive Office), and enters the host (the staff member being visited) and the purpose. The check-in time is recorded automatically on submit, and the visit goes to the Front Desk portal as Pending for approval.
- View All Visits: that visitor's visit history (department, purpose, host, check-in, check-out, status). Check-out times are recorded by Front Desk, not Security.
- Security cannot approve, reject, hold or check out visitors — that is done in the Front Desk portal.""" + SWITCH_NOTE + "\n" + GUIDE_RULES,
    "frontdesk": """
You are the in-app help assistant for the Front Desk Portal of REX Insurance's Visitor Management System. What the portal actually does:
- Login: staff enter their name and the front desk passcode.
- Stat boxes at the top count today's visits that are Pending review, On hold, Approved, With host, and Rejected.
- Visitor Status Board: every visit Security has logged today — visitor, department, host, appointment type (Walk-in or Scheduled), check-in time and status. It refreshes automatically, so no manual refresh is needed.
- Filter tabs: All, Pending, Hold, Approved, With Host, Rejected, Checked Out. The search box finds a visitor or host by name.
- Clicking a row opens the actions that are valid for that visit's current stage:
  * Pending or Hold: Step 1 is "Host is available" or "Host is unavailable" (unavailable puts the visitor on Hold). If the host is available, Step 2 offers Accept (approves the visitor), Reject, or Hold (visitor waits a bit longer).
  * Approved: "Mark as with host" once the visitor has reached the host's office.
  * With Host: "Check out visitor" when the visitor leaves; the check-out time is recorded automatically.
  * Rejected and Checked Out are final — no further actions.
- The portal does not message the host itself: the Front Desk officer contacts the host directly (call or message) and then records the host's answer in the portal. Hosts have no login.
- Front Desk cannot register visitors or log new visits — that is done in the Security portal.""" + SWITCH_NOTE + "\n" + GUIDE_RULES,
    "admin": """
You are the in-app help assistant for the Admin Portal of REX Insurance's Visitor Management System. What the portal actually does:
- Login: staff enter their name and the admin passcode. A left menu has five sections:
- Dashboard: counts for visitors today, currently inside (visits that are Approved or With host), pending approvals (Pending or On hold), and visitors this month; a Staff Performance bar chart (visits handled by each host in the last 7 days, top 5); and a Recent Activity feed of the latest visit events.
- Users & Roles: a staff roster (name, role — Security Officer, Front Desk Officer or Admin — and Active/Suspended status). Admins can Add Staff Member and Suspend or Activate a person. It is a directory only and is NOT connected to portal login.
- Visitor Logs: the complete all-time visit history (visitor, department, host, check-in, check-out, status), loaded 20 at a time with a "Load more" button. The search box searches visitor, host, or department across the full history.
- Session Control: Active Sessions (who is logged in to which portal, when they logged in and when they were last seen), Passcodes (a "Change Passcode" button for the security, frontdesk and admin portals; at least 4 characters; the new passcode applies to the next login), and Login History (the 50 most recent logins and logouts).
- Reports: four report cards (Daily Visitor Log, Monthly Visitor Count, Staff Visit Frequency, Security & Front Desk Performance), each with PDF and Excel buttons. IMPORTANT: report export is not built yet — the buttons only show a "demo only" message and do not produce a file. Say this plainly if asked about exporting or downloading reports, and suggest using the Visitor Logs search for now.
- There is no force-logout button; admins can only view sessions.""" + SWITCH_NOTE + "\n" + GUIDE_RULES,
}


@app.route("/api/ai/ask", methods=["POST"])
def ai_ask():
    data = request.get_json(force=True, silent=True) or {}
    portal = data.get("portal")
    question = (data.get("question") or "").strip()

    if portal not in GUIDE_CONTEXT:
        return jsonify({"error": "Unknown portal."}), 400
    if not question:
        return jsonify({"error": "Ask a question first."}), 400
    if len(question) > 500:
        return jsonify({"error": "Please keep your question under 500 characters."}), 400
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
                    {"role": "system", "content": GUIDE_CONTEXT[portal]},
                    {"role": "user", "content": question},
                ],
                "max_tokens": 300,
                "temperature": 0.3,
            },
            timeout=25,
        )
        if resp.status_code in (401, 403):
            return jsonify({"error": "The AI guide's API key was rejected. Check MISTRAL_API_KEY on the server."}), 502
        if resp.status_code == 429:
            return jsonify({"error": "The AI guide is busy right now. Try again in a moment."}), 503
        resp.raise_for_status()
        answer = (resp.json()["choices"][0]["message"]["content"] or "").strip()
        if not answer:
            return jsonify({"error": "The AI guide returned an empty answer. Try rephrasing."}), 502
        return jsonify({"answer": answer})
    except requests.exceptions.Timeout:
        return jsonify({"error": "The AI guide took too long to respond. Try again."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"AI guide is temporarily unavailable ({e.__class__.__name__})."}), 502
    except (KeyError, IndexError, ValueError):
        return jsonify({"error": "The AI guide sent back an unexpected response."}), 502


# ============================================================
# Startup
# ============================================================
init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)