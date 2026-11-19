# SupportDesk Pro
### IT Support Ticketing & Troubleshooting Management System

SupportDesk Pro is a Python-based web application developed as part of a Work-Integrated Learning (WIL) project. It simulates an IT support environment where users can report incidents, technicians can investigate and document troubleshooting activities, and users can review and accept or reject proposed resolutions.

The project demonstrates software development, database management, application security, testing and technical documentation.

> **Project status:** Academic WIL prototype. Designed for local execution using synthetic test data. It is not an officially commissioned or approved Capitec system and is not authorised for production deployment or connection to live banking systems.

---

## 1. Project Objectives

- Centralise IT incident registration and tracking.
- Provide role-based access to incident management functionality.
- Allow technicians to investigate incidents and record troubleshooting activities.
- Introduce a formal resolution review and user acceptance process.
- Maintain an audit trail of important system activities.
- Provide reporting and management oversight.
- Demonstrate secure database access, validation and software testing.

## 2. Technologies Used

| Component | Technology |
|---|---|
| Programming language | Python 3.13 |
| Backend framework | Flask |
| Frontend | HTML, CSS, JavaScript |
| Template engine | Jinja |
| Database | Microsoft SQL Server Express |
| Database connectivity | pyodbc |
| Database management | SQL Server Management Studio |
| Security | Flask-WTF CSRF protection, Werkzeug password hashing, signed resolution tokens |
| Testing | pytest |
| Development environment | Visual Studio Code |
| Version control | Git and GitHub |

## 3. Project Structure

```text
TicketManagementSystem/
│
├── app/
│   ├── db/
│   ├── repositories/
│   ├── routes/
│   ├── security/
│   ├── services/
│   └── templates/
│
├── database/
│   ├── 02_create_tables.sql
│   └── 03_seed_data.sql
│
├── docs/
│   ├── DDS.md
│   ├── Feasibility-Report.md
│   ├── Project-Plan.md
│   ├── SRS.md
│   └── User-Manual.md
│
├── scripts/
│   └── configure_test_accounts.py
│
├── screenshots/
├── logs/
├── tests/
├── src/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-lock.txt
└── run.py
```

## 4. System Architecture

The application follows a layered architecture to separate web requests, business logic and database operations.

```text
User / Web Browser
        |
        v
Flask Routes
        |
        v
Service Layer
        |
        v
Repository / Data Access Layer
        |
        v
pyodbc
        |
        v
Microsoft SQL Server
```

### Architectural responsibilities

- **Routes:** Handle HTTP requests, authentication checks and responses.
- **Services:** Apply business rules, validation and application logic.
- **Repositories:** Execute database operations using parameterised SQL.
- **Database:** Store users, incidents, troubleshooting records, resolutions, feedback and audit information.

## 5. User Roles

| Role | Main responsibilities |
|---|---|
| User | Create incidents, view personal incidents and review proposed resolutions. |
| Technician | View assigned and unassigned incidents, claim incidents, troubleshoot and submit resolutions. |
| Supervisor | Monitor organisation-wide incidents and access reports. |
| Administrator | Manage user accounts, assign incidents and access reports and administrative functions. |

Access to protected functionality is restricted according to the authenticated user's current role.

## 6. Main Features

### Authentication and account management
- User login and logout.
- Password hashing.
- Role-based access control.
- Administrator-managed user accounts.
- User activation and deactivation.
- Login attempt audit records.

### Incident management
- Incident registration.
- Unique incident reference generation.
- Incident viewing and searching.
- Filtering by status, priority and category.
- Technician assignment and reassignment.
- Technician self-claiming of unassigned incidents.

### Troubleshooting and resolution
- Recording troubleshooting activities.
- Viewing troubleshooting and resolution history.
- Submitting proposed resolutions.
- Secure, time-limited resolution review links.
- User acceptance or rejection of resolutions.
- Rejection feedback and incident reopening.
- Incident closure following user acceptance.

### Reporting and oversight
- Organisation-wide incident monitoring.
- Incident statistics and reporting.
- Date-based report filtering.
- CSV and PDF report exports.
- Administrator and supervisor reporting access.

### Audit logging
Important application activities are recorded to support accountability and traceability.

## 7. Incident Lifecycle

```text
Open
  |
  v
In Progress
  |
  v
Awaiting User Confirmation
  |
  +------ User accepts ------> Closed
  |
  +------ User rejects ------> Reopened
                                  |
                                  v
                              In Progress
```

An incident is not considered fully resolved until the reporting user accepts the proposed resolution.

## 8. Technologies and Dependencies

Direct project dependencies are listed in `requirements.txt`.

`requirements-lock.txt` contains pinned dependency versions for more reproducible installations.

Install the locked dependencies using:

```powershell
python -m pip install -r requirements-lock.txt
```

## 9. Local Development Setup

### Prerequisites

- Windows 10 or Windows 11.
- Python 3.13.
- Microsoft SQL Server Express.
- SQL Server Management Studio.
- Microsoft ODBC Driver 18 for SQL Server.
- Visual Studio Code.
- Git.

### Clone the repository

```powershell
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd TicketManagementSystem
```

### Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
python -m pip install -r requirements-lock.txt
```

### Configure environment variables

Copy `.env.example` to `.env` in the project root.

```powershell
Copy-Item .env.example .env
```

Open `.env` in Visual Studio Code and replace the placeholder secret key with a randomly generated value.

Generate a secret key using:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Update the database server and database settings if your local SQL Server configuration differs from the example.

**Important:** Never commit `.env` files, passwords, secret keys or other credentials to GitHub. The `.gitignore` file excludes these sensitive files.

## 10. Database Setup

SupportDesk Pro uses Microsoft SQL Server Express.

### Step 1: Create the database

In SQL Server Management Studio, connect to your local SQL Server instance and create a database