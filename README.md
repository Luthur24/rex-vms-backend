Rex VMS Backend

Flask backend for Rex Insurance's Visitor Management System (Rex VMS), providing authentication, role-based portal access, visitor management, session control, administrative operations, notifications, and PostgreSQL integration.

Overview

Rex VMS is a visitor-management platform designed around the operational workflow of a corporate reception and security environment.

The backend provides the API and server-side logic supporting three primary operational portals:

- Security
- Front Desk
- Admin

Each portal has a defined set of permissions and responsibilities within the visitor-management workflow.

The backend was developed as part of an SIWES project based on the visitor-management workflow used at Rex Insurance.

Portal Architecture

                         Rex VMS
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
      Security          Front Desk          Admin
          │                 │                 │
          ▼                 ▼                 ▼
     Visitors         Visitor Status      System
     Registration         Board           Management
     Search             Actions          Staff Roster
     Check-in           Check-out        Sessions
     Verification       Host Actions     Login History

The backend explicitly defines "security", "frontdesk", and "admin" as the supported portals.

Core Features

Authentication & Sessions

- Portal-based authentication
- Passcode authentication
- Secure session tokens
- Login verification
- Logout handling
- Active-session tracking
- Login history
- Session concurrency limits
- Administrative force logout

The login flow validates the selected portal and passcode, checks the portal's active-session capacity, creates a session token, and records login history.

Security Portal

Security personnel can:

- View registered visitors
- Search visitors
- Search by visitor name
- Search by phone number
- Search by identification number
- Register new visitors
- Manage visitor check-in workflows

The backend restricts visitor-list operations to the Security portal.

Front Desk Portal

Front Desk staff operate a live visitor-status workflow.

Supported visitor states include:

Pending Review
Hold
Approved
With Host
Rejected
Checked Out

Front Desk users can search and filter visitors, check host availability, accept/reject/hold visitors, mark visitors as being with their host, and complete check-out operations.

Admin Portal

Administrative functionality includes:

- Staff roster management
- Staff activation/suspension
- Active-session monitoring
- Force logout
- Login-history inspection
- Portal passcode management
- Portal concurrency configuration

The backend provides dedicated administrative endpoints for these operations.

AI Help Assistant

Rex VMS also includes an in-app help assistant powered by Mistral.

The assistant is given portal-specific context so that responses remain grounded in the actual functionality available to Security, Front Desk, and Admin users rather than relying entirely on generic model knowledge.

API

Representative endpoints include:

POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/verify

GET  /api/visitors

GET  /api/admin/roster
POST /api/admin/roster
PATCH /api/admin/roster/<id>

GET  /api/admin/sessions
POST /api/admin/sessions/<id>/force-logout

GET  /api/admin/login-history

POST /api/admin/passcode

GET  /api/admin/concurrency
POST /api/admin/concurrency

Session Management

Rex VMS implements server-side session records rather than treating authentication as a purely client-side concern.

Login
  │
  ▼
Validate Portal
  │
  ▼
Validate Passcode
  │
  ▼
Check Session Capacity
  │
  ▼
Create Session Token
  │
  ▼
Store Session
  │
  ▼
Record Login History

The backend also supports session verification and logout state management.

Technology Stack

- Python
- Flask
- PostgreSQL
- psycopg2
- REST API
- Server-side sessions
- Password hashing
- Mistral API
- Git & GitHub

Repository Structure

rex-vms-backend/
├── app.py
├── requirements.txt
└── README.md

The primary Flask application is contained in "app.py", with dependencies defined in "requirements.txt".

Running Locally

Clone the repository:

git clone <repository-url>
cd rex-vms-backend

Install dependencies:

pip install -r requirements.txt

Configure the required environment variables for:

DATABASE
SESSION / AUTHENTICATION
MISTRAL
PORTAL CONFIGURATION

Start the Flask application:

python app.py

Security

Production credentials must never be committed to source control.

Portal passcodes, database credentials, API keys, session secrets, and other sensitive configuration should be supplied through environment variables or a dedicated secret-management system.

The backend itself hashes portal passcodes before storing them in the database and validates them during authentication.

Project Context

Rex VMS was developed as an SIWES project during placement at Rex Insurance.

The project was developed around the organization's visitor-management workflow and was implemented as a software engineering project to reproduce and understand the underlying operational process.

Project Status

Backend / Operational MVP

Rex VMS is maintained as the backend component of the visitor-management system.

Related Repository

The corresponding Rex VMS frontend contains dedicated interfaces for Security, Front Desk, and Admin users.