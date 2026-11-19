# SupportDesk Pro – System Design Specification (DDS)

**Document:** System Design Specification
**Project:** SupportDesk Pro – IT Support Ticketing & Troubleshooting Management System
**Organisation Context:** Capitec Bank – Head Office, IT Support (academic simulation)
**Developer:** Amier Apollis
**Project Supervisor:** Rhyno Hendricks
**Project Start Date:** 2 November 2026
**Document Version:** 1.1
**Document Status:** Approved Project Requirements Baseline
**Development Environment:** Windows 10/11

---

## 1. Introduction

### 1.1 Purpose

This System Design Specification (DDS) describes the technical architecture, database structure, application components, user interface, workflows and security controls for SupportDesk Pro.

The document translates the requirements defined in the Software Requirements Specification (SRS) into a technical design that guides implementation, testing, maintenance and evaluation.

### 1.2 Project Background

SupportDesk Pro is a web-based IT Support Ticketing and Troubleshooting Management System developed as an academic Workplace Integrated Learning (WIL) project.

The application simulates an IT support environment in which Users can report incidents, Technicians can investigate and resolve them, and authorised management users can oversee incident activity.

The main design objective is to ensure that technical work being completed is not automatically treated as confirmation that the reported issue has been resolved. The reporting User must be able to review a proposed resolution and accept or reject it.

### 1.3 Project Objectives

The system design aims to:

- Provide a centralised incident management application.
- Enforce authentication and role-based access.
- Support incident registration, searching and tracking.
- Allow Administrators to assign or reassign incidents.
- Allow Technicians to claim unassigned incidents.
- Maintain troubleshooting records and resolution history.
- Require User confirmation before an incident is closed.
- Record acceptance and rejection decisions.
- Maintain an audit history of important system activities.
- Provide reporting and management oversight.
- Protect application data through validation, access controls and secure database operations.

### 1.4 Project Scope

The design covers the following application functionality:

- User authentication and session management.
- Role-based access for User, Technician, Administrator and Supervisor accounts.
- Incident registration, viewing, searching and filtering.
- Incident assignment, reassignment and technician claiming.
- Troubleshooting activity recording.
- Resolution submission and review.
- User acceptance and rejection of proposed resolutions.
- Reopening rejected incidents for further investigation.
- User account administration.
- Audit logging.
- Reporting and data exports.
- Input validation and error handling.

The Knowledge Base functionality identified in the original SRS is excluded from the current implementation.

The project is a local academic simulation. It does not connect to live Capitec systems, use production banking data, integrate with corporate authentication services or deploy to a production environment. Only synthetic or otherwise authorised test data is used.

Email notification functionality exists in the implementation. Its relationship to the original scope exclusion for automated notifications is recorded in Section 10 for requirements reconciliation.

---

## 2. Technology Design

The following technologies form the system's development and execution environment.

| Component | Technology | Purpose |
|---|---|---|
| Programming language | Python 3 | Backend application logic |
| Backend framework | Flask | Request handling, routing and application structure |
| Frontend | HTML5, CSS3 and JavaScript | User interface and browser-side interactivity |
| Template engine | Jinja | Dynamic server-rendered HTML |
| Database | Microsoft SQL Server Express | Relational application data storage |
| Database connectivity | pyodbc | Python-to-SQL Server connectivity |
| Database management | SQL Server Management Studio (SSMS) | Database administration and inspection |
| Development environment | Visual Studio Code | Source code development |
| Version control | Git and GitHub | Source code versioning |
| Testing | pytest | Automated application testing |
| Configuration | python-dotenv | Environment variable loading |
| Request protection | Flask-WTF | CSRF protection |
| Password security | Werkzeug security utilities | Password hashing and verification |
| PDF reporting | ReportLab | PDF report generation |
| Operating system | Windows 10/11 | Local development and execution |

### 2.1 Database Access Approach

The application uses direct parameterised SQL queries through `pyodbc`.

An Object Relational Mapper (ORM) is not used. Repositories execute SQL statements and map database results into Python data structures for use by the service layer.

Parameterised queries are used for user-supplied values to reduce SQL injection risk.

### 2.2 Development and Runtime Environment

The application runs locally using a Python virtual environment. Configuration values, including database connection settings and the Flask secret key, are loaded from environment variables.

The database is hosted on the local SQL Server Express instance and can be inspected through SSMS.

The application is started through the project's `run.py` entry point.

---

## 3. System Design

### 3.1 High-Level System Architecture

SupportDesk Pro follows a layered Flask application architecture. The browser communicates with the Flask application through HTTP requests. Routes receive requests and delegate application operations to services. Services apply validation and business rules before calling repository methods. Repositories execute parameterised SQL through `pyodbc` to access SQL Server.

The application uses server-rendered Jinja templates. HTML provides page structure, CSS controls presentation and JavaScript supports browser-side interactions.

The logical architecture is:

```text
+-------------------------------+
|       User's Web Browser      |
|       HTML / CSS / JavaScript |
+---------------+---------------+
                |
                | HTTP Requests
                v
+-------------------------------+
|       Flask Application       |
|                               |
|  +-------------------------+  |
|  | Routes / Blueprints     |  |
|  +------------+------------+  |
|               |               |
|  +------------v------------+  |
|  | Service Layer           |  |
|  | Validation and Rules    |  |
|  +------------+------------+  |
|               |               |
|  +------------v------------+  |
|  | Repository / Data Access|  |
|  | Parameterised SQL       |  |
|  +------------+------------+  |
+---------------|---------------+
                |
                | pyodbc
                v
+-------------------------------+
|       SQL Server Express      |
|       SupportDeskProDB        |
+-------------------------------+
```

### 3.2 Architecture Layer Responsibilities

| Layer | Responsibility |
|---|---|
| Presentation | Displays pages, forms, incident information and feedback messages through Jinja templates. |
| Routes / Controllers | Receives HTTP requests, applies route-level access controls and delegates operations to services. |
| Service Layer | Enforces business rules, validates input, coordinates operations and handles application workflows. |
| Repository / Data Access | Executes SQL queries and performs database operations using parameterised statements. |
| Database Connectivity | Establishes and manages connections between Python and SQL Server through `pyodbc`. |
| Database | Stores user accounts, categories, incidents, troubleshooting records, resolutions, feedback and audit information. |

Each layer has a defined responsibility. Database queries are kept out of route handlers and templates. Business rules are implemented in the service layer rather than being duplicated across presentation pages.

### 3.3 Application Structure

The application uses the Flask application factory pattern and Blueprints to organise functionality into separate modules.

The principal application areas are:

- **Authentication:** Login, logout, password verification and session handling.
- **Incident Management:** Incident creation, viewing, searching, filtering and status-related operations.
- **Technician Management:** Technician queues, incident claiming, assignment visibility and troubleshooting.
- **Resolution Management:** Resolution submission, User review, acceptance, rejection and resolution history.
- **Administration:** User account management, role changes, activation and deactivation, and incident assignment.
- **Supervisor Oversight:** Organisation-wide incident visibility and read-only oversight.
- **Reporting:** Incident statistics, date filtering, CSV exports and PDF exports.
- **Security:** Authentication checks, role authorisation, CSRF protection and resolution token verification.
- **Database Access:** SQL Server connection management and repository operations.

### 3.4 Application Folder Organisation

The principal project structure is organised as follows:

```text
TicketManagementSystem/
|
+-- app/
|   +-- __init__.py
|   +-- config.py
|   +-- errors.py
|   |
|   +-- db/
|   |   +-- connection.py
|   |
|   +-- repositories/
|   |   +-- database_repository.py
|   |   +-- incident_repository.py
|   |   +-- user_repository.py
|   |   +-- supervisor_repository.py
|   |   +-- reporting_repository.py
|   |
|   +-- routes/
|   |   +-- auth_routes.py
|   |   +-- main_routes.py
|

## 4. Database Design

### 4.1 Database Tables and Main Attributes

The following tables describe the principal database attributes and their intended roles in the system design.

#### 4.1.1 Users

| Attribute | Data Type | Description |
|---|---|---|
| UserId | INT | Primary key identifying the user. |
| FullName | NVARCHAR(100) | User's full name. |
| Email | NVARCHAR(254) | Unique email address used for account identification. |
| PasswordHash | NVARCHAR(255) | Secure password hash. |
| Role | NVARCHAR(20) | Assigned role: User, Technician, Administrator or Supervisor. |
| IsActive | BIT | Indicates whether the account is active. |

#### 4.1.2 Categories

| Attribute | Data Type | Description |
|---|---|---|
| CategoryId | INT | Primary key identifying the category. |
| Name | NVARCHAR(50) | Category name. |
| Description | NVARCHAR(250) | Description of the category. |

Initial categories include Hardware, Software, Network and Access Issues. Category records are inserted through a database seed script.

#### 4.1.3 Incidents

| Attribute | Data Type | Description |
|---|---|---|
| IncidentId | INT | Primary key identifying the incident. |
| IncidentReference | NVARCHAR | Unique incident reference displayed to users. |
| UserId | INT | Foreign key referencing the reporting User. |
| TechnicianId | INT, nullable | Foreign key referencing the assigned Technician. |
| CategoryId | INT | Foreign key referencing Categories. |
| Title | NVARCHAR(150) | Incident title. |
| Description | NVARCHAR(4000) | Description of the reported issue. |
| Priority | NVARCHAR(10) | Incident priority. |
| Status | NVARCHAR(30) | Current incident status. |
| CreatedAt | DATETIME2(7) | Date and time the incident was created. |
| ClosedAt | DATETIME2(7), nullable | Date and time the incident was closed. |

#### 4.1.4 TroubleshootingRecords

| Attribute | Data Type | Description |
|---|---|---|
| RecordId | INT | Primary key identifying the record. |
| IncidentId | INT | Foreign key referencing Incidents. |
| TechnicianId | INT | Technician who performed the action. |
| ActionTaken | NVARCHAR(2000) | Description of the troubleshooting activity. |
| CreatedAt | DATETIME2(7) | Date and time the activity was recorded. |

#### 4.1.5 Resolutions

| Attribute | Data Type | Description |
|---|---|---|
| ResolutionId | INT | Primary key identifying the resolution. |
| IncidentId | INT | Foreign key referencing Incidents. |
| TechnicianId | INT | Technician who submitted the resolution. |
| ResolutionText | NVARCHAR(2000) | Proposed resolution details. |
| SubmittedAt | DATETIME2(7) | Date and time the resolution was submitted. |

#### 4.1.6 UserFeedback

| Attribute | Data Type | Description |
|---|---|---|
| FeedbackId | INT | Primary key identifying the feedback record. |
| IncidentId | INT | Foreign key referencing Incidents. |
| ResolutionId | INT | Foreign key referencing Resolutions. |
| UserId | INT | User who submitted the decision. |
| Decision | NVARCHAR(10) | Accepted or Rejected. |
| Comments | NVARCHAR(1000) | User feedback or rejection reason. |
| SubmittedAt | DATETIME2(7) | Date and time the decision was submitted. |

#### 4.1.7 AuditLogs

| Attribute | Data Type | Description |
|---|---|---|
| AuditLogId | INT | Primary key identifying the audit record. |
| IncidentId | INT, nullable | Related incident, where applicable. |
| UserId | INT, nullable | User responsible for the action, where applicable. |
| Action | NVARCHAR(50) | Description of the recorded action. |
| FromStatus | NVARCHAR(30), nullable | Previous incident status, where applicable. |
| ToStatus | NVARCHAR(30), nullable | New incident status, where applicable. |
| Details | NVARCHAR(500) | Additional information about the action. |
| CreatedAt | DATETIME2(7) | Date and time the action was recorded. |

*Note: The data types above describe the logical design. The SQL creation scripts in the project are the implementation reference for exact column definitions and constraints.*

### 4.2 Database Constraints and Integrity

The database design applies the following integrity rules:

- Every user must have a unique email address.
- Every incident must have a unique incident reference.
- Every incident must reference a valid reporting User and Category.
- An incident may have an assigned Technician or remain unassigned.
- User roles are restricted to User, Technician, Administrator and Supervisor.
- Incident priorities are restricted to Low, Medium and High.
- Incident statuses are restricted to Open, In Progress, Awaiting User Confirmation, Reopened and Closed.
- Feedback decisions are restricted to Accepted and Rejected.
- A resolution can receive only one feedback decision.
- A rejected resolution must have a reason recorded in the feedback comments.
- A closed incident must have a closure date.
- Historical troubleshooting, resolution, feedback and audit records must be retained.
- Foreign keys must reference existing records.

### 4.3 Database Transaction Design

Operations that update multiple related records must be performed within database transactions.

Examples include:

- Assigning or claiming an incident and recording the corresponding audit entry.
- Recording a troubleshooting action and its audit entry.
- Submitting a resolution and updating the incident status.
- Accepting or rejecting a resolution, inserting UserFeedback, updating the incident status and recording the audit entry.
- Creating a managed user account and recording the associated audit entry.

If a transaction fails, the repository must roll back the changes so that incomplete related updates are not committed.

The resolution decision process also uses database locking to protect the incident from conflicting simultaneous decisions.

---

## 5. User Roles and Access Control Design

### 5.1 Role Definitions

The application uses four roles.

| Role | Description |
|---|---|
| User | Reports incidents, views their own incidents and reviews proposed resolutions. |
| Technician | Investigates assigned incidents, claims unassigned incidents, records troubleshooting and submits resolutions. |
| Administrator | Manages user accounts, assigns and reassigns incidents, and accesses administrative reporting. |
| Supervisor | Provides organisation-wide oversight and accesses reports without performing administrative changes. |

### 5.2 Role Permission Matrix

| Functionality | User | Technician | Administrator | Supervisor |
|---|:---:|:---:|:---:|:---:|
| Log in and log out | Yes | Yes | Yes | Yes |
| Create an incident | Yes | No | No | No |
| View own incidents | Yes | No | No | No |
| Search and filter own incidents | Yes | No | No | No |
| Review and decide on own resolution | Yes | No | No | No |
| View technician incident queue | No | Yes | No | No |
| Claim unassigned incidents | No | Yes | No | No |
| Record troubleshooting | No | Yes | No | No |
| Submit proposed resolutions | No | Yes | No | No |
| View all incidents | No | No | Yes | Yes |
| Assign and reassign Technicians | No | No | Yes | No |
| Manage user accounts | No | No | Yes | No |
| Change user roles and account status | No | No | Yes | No |
| View organisation-wide dashboard | No | No | No | Yes |
| Access incident reports | No | No | Yes | Yes |
| Export reports | No | No | Yes | Yes |

Access is enforced through authentication checks, role-based route decorators and service-level business rules. Hiding a link or button in the interface is not treated as a substitute for server-side authorisation.

### 5.3 Account Management Rules

- Administrator accounts create and manage application users.
- Public self-registration is disabled.
- Email addresses must be unique.
- Passwords must meet the configured password policy.
- Administrators may change user roles and account status within permitted rules.
- Administrators cannot change their own role or deactivate their own account through the account-management workflow.
- The application must prevent the last active Administrator from being removed or deactivated.
- A Technician with outstanding non-Closed incidents must have those incidents reassigned before their account can be deactivated.

### 5.4 Technician Assignment and Claiming

Administrators can assign or reassign incidents to Technicians.

Technicians can claim an unassigned incident. The claim operation must verify that the incident is still unassigned and is not Closed.

The assignment or claim operation must be protected against simultaneous conflicting claims. The database operation records the successful assignment and corresponding audit event.

Claiming an incident changes its assigned Technician but does not automatically change its incident status.

---

## 6. Incident Workflow Design

### 6.1 Incident Lifecycle

The incident lifecycle uses the following statuses:

| Status | Meaning |
|---|---|
| Open | Incident has been registered and is awaiting investigation. |
| In Progress | A Technician is actively investigating the incident. |
| Awaiting User Confirmation | A proposed resolution has been submitted for the reporting User to review. |
| Reopened | The User rejected the proposed resolution and further investigation is required. |
| Closed | The User accepted the proposed resolution. |

The normal workflow is:

```text
          +------+
          | Open |
          +--+---+
             |
             v
       +------------+
       | In Progress|
       +------+-----+
              |
              | Resolution submitted
              v
 +-----------------------------+
 | Awaiting User Confirmation  |
 +--------------+--------------+
                |
          User decision
           /        \
          /          \
      Accept         Reject
        |               |
        v               v
   +---------+     +----------+
   | Closed  |     | Reopened |
   +---------+     +----+-----+
                         |
                         | Investigation resumes
                         v
                   +------------+
                   | In Progress|
                   +------------+
```

### 6.2 Incident Registration

1. The User opens the incident registration page.
2. The User provides the incident title, description, category and priority.
3. The system validates the submitted information.
4. The system associates the incident with the authenticated User.
5. The system generates a unique incident reference.
6. The incident is saved with Open status.
7. The creation event is recorded in the audit history.

### 6.3 Incident Assignment

1. An Administrator views incidents requiring assignment.
2. The Administrator assigns an available Technician.
3. The system validates the selected Technician.
4. The assignment is saved and recorded in the audit history.

Alternatively, a Technician can claim an unassigned incident through the technician queue. The system checks that another Technician has not already claimed it.

### 6.4 Investigation and Troubleshooting

1. The assigned Technician opens the incident.
2. The Technician moves the incident into In Progress when investigation begins.
3. The Technician records troubleshooting actions against the incident.
4. Each troubleshooting record is associated with the Technician and incident.
5. The system retains the troubleshooting history.

Troubleshooting actions may only be added while the incident is In Progress.

### 6.5 Resolution Submission

1. The Technician records the proposed resolution.
2. The system verifies that the Technician is assigned to the incident.
3. The system verifies that the incident is in an eligible status.
4. The system verifies that at least one troubleshooting action has been recorded for the current investigation cycle.
5. The resolution is stored as a separate record.
6. The incident moves to Awaiting User Confirmation.
7. An audit event is recorded.

### 6.6 User Decision

The original reporting User reviews the proposed resolution.

The User can:

**Accept the resolution**
- The system records an Accepted decision.
- The incident status changes to Closed.
- The closure date is recorded.
- The decision and related audit event are retained.

**Reject the resolution**
- The User must provide a rejection reason.
- The system records a Rejected decision and comments.
- The incident status changes to Reopened.
- The rejection and related audit event are retained.

Only the reporting User may make the decision on their own incident.

### 6.7 Further Investigation

When a resolution is rejected:

1. The rejection reason is retained.
2. The incident returns to the support workflow as Reopened.
3. The assigned Technician resumes investigation.
4. The Technician changes the incident to In Progress.
5. Further troubleshooting is recorded.
6. A new resolution is submitted for User confirmation.

This process repeats until the User accepts a proposed resolution.

Closed incidents are treated as final and cannot be reopened through normal application operations.

### 6.8 Resolution History

Every resolution attempt is stored separately.

For example, if a resolution is rejected twice before being accepted, the system retains:

- Resolution attempt 1 and its rejection reason.
- Resolution attempt 2 and its rejection reason.
- Resolution attempt 3 and its acceptance decision.

Previous records must remain available in the incident history. A new resolution must not overwrite an earlier resolution or its decision.

### 6.9 Audit Logging

The application records important activities, including:

- Successful and unsuccessful login attempts.
- Incident creation.
- Technician assignment and reassignment.
- Technician incident claims.
- Status changes.
- Troubleshooting activities.
- Resolution submissions.
- Resolution acceptance and rejection.
- User account creation and updates.
- User account activation and deactivation.

Audit records contain relevant user, incident, action, details and timestamp information.

---

## 7. Component and Function Design

### 7.1 Authentication Module

Responsible for:

- Validating login details.
- Verifying stored password hashes.
- Identifying the user's role.
- Creating and ending user sessions.
- Recording successful and unsuccessful login attempts.
- Preventing unauthorised access.
- Verifying that accounts remain active.

### 7.2 Incident Management Module

Responsible for:

- Creating incidents.
- Generating incident references.
- Displaying incident information.
- Searching and filtering incidents.
- Managing incident assignments.
- Supporting technician claiming.
- Controlling permitted status changes.
- Enforcing User ownership restrictions.

### 7.3 Troubleshooting Module

Responsible for:

- Recording troubleshooting activities.
- Associating actions with incidents and Technicians.
- Displaying previous troubleshooting records.
- Ensuring troubleshooting actions are recorded while an incident is In Progress.
- Supporting the requirement for troubleshooting before resolution submission.

### 7.4 Resolution Module

Responsible for:

- Recording proposed resolutions.
- Submitting resolutions for User confirmation.
- Providing the User with a review process.
- Processing acceptance decisions.
- Processing rejection decisions and feedback.
- Maintaining resolution history.
- Preventing duplicate decisions for the same resolution.

### 7.5 Administration Module

Responsible for:

- Creating authorised user accounts.
- Updating user information and roles.
- Activating and deactivating accounts.
- Assigning and reassigning incidents.
- Enforcing account-management restrictions.

### 7.6 Supervisor Module

Responsible for:

- Providing organisation-wide incident visibility.
- Displaying oversight information.
- Supporting read-only monitoring of incident activity.
- Providing access to reporting functionality.

### 7.7 Reporting Module

Responsible for generating basic reports, including:

- Total registered incidents.
- Incidents grouped by current status.
- Incidents Awaiting User Confirmation.
- Accepted and rejected resolution counts.
- Basic incident statistics.
- Date-filtered report results.
- CSV and PDF exports.

Both Administrator and Supervisor roles are permitted to access reporting functionality.

### 7.8 Email Notification Component

The implementation includes an email service used for resolution notifications and resending pending resolution links.

The email service uses SMTP configuration and sends notification messages to the reporting User. Email delivery is separate from the database transaction that records a resolution. A notification failure does not undo a resolution that has already been saved.

The email functionality and its relationship to the original scope are documented in Section 10.

---

## 8. Security and Error Handling

### 8.1 Authentication and Access Control

The system requires users to authenticate before accessing protected functionality.

Passwords are stored as secure hashes and are never stored as plaintext.

The application stores the authenticated user's identifier in the session and retrieves the current account information from the database when processing protected requests. This allows account status and role changes to take effect without relying on outdated role information stored in the session.

Role-based decorators restrict access to protected routes.

### 8.2 Password Security

The application uses Werkzeug password hashing utilities.

Password verification compares the submitted password with the stored password hash.

The account-management validation policy requires:

- At least eight characters.
- At least one letter.
- At least one digit.
- Matching password and confirmation values during account creation.

Passwords are not written to audit logs.

### 8.3 Database Security

The following controls are applied:

- Parameterised SQL queries for database operations.
- Environment variables for sensitive configuration.
- Windows Authentication for the local SQL Server connection.
- Input validation before database operations.
- Foreign keys and database constraints to maintain data integrity.
- Restricted access through application roles.
- Synthetic or authorised test data only.

### 8.4 Session and Request Security

The application uses Flask session handling.

The session cookie is configured with HTTPOnly and SameSite protections. The session inactivity lifetime is configured as 30 minutes.

CSRF protection is enabled globally through Flask-WTF. State-changing forms include CSRF tokens.

GET requests are used to retrieve information. POST requests are used for operations that modify application data.

### 8.5 Resolution Review Link Security

The resolution review workflow uses a signed, time-limited token.

The token is generated using `itsdangerous.URLSafeTimedSerializer` and is associated with the resolution, incident and reporting User.

The token expires after seven days.

The token is verified before the resolution can be retrieved or a decision can be submitted. The application checks that the resolution belongs to the incident and reporting User and that the incident is still awaiting confirmation.

The review page uses response headers to prevent caching and restrict referrer information.

The review link acts as a temporary bearer credential. Anyone possessing a valid link may attempt to access the review page, so links must be sent only to the intended reporting User.

### 8.6 Error Handling

The application handles errors without exposing sensitive technical information to normal users.

| Error | System Response |
|---|---|
| Invalid login | Display a generic authentication error. |
| Missing required information | Display validation messages. |
| Unauthorised access | Display an access-denied response. |
| Incident not found or not visible | Display a not-found response. |
| Invalid status transition | Explain that the requested action is not permitted. |
| Invalid or expired resolution token | Display a not-found response. |
| Database connection failure | Display a general system error. |
| Unexpected application error | Display a friendly error page. |

Detailed technical errors may be recorded in application logs for debugging but must not be exposed to normal users.

### 8.7 Local Execution Security Configuration

The application is intended to run locally for academic demonstration and assessment. Its configuration is therefore designed for the local Windows and SQL Server Express environment.

The Flask debug setting is disabled for normal execution. The session cookie Secure flag remains disabled because the local application is accessed over HTTP rather than deployed behind HTTPS. If the application were ever hosted over HTTPS, this setting would need to be enabled.

---

## 9. Validation and Data Integrity

The application validates information before it is submitted to the database.

The following validation rules apply:

- Required fields must not be empty.
- Email addresses must follow a valid format.
- Email addresses must be unique.
- Passwords must meet the configured password requirements.
- Incident titles and descriptions must meet defined length limits.
- Search terms must meet their permitted length.
- Priority and status values must belong to the permitted values.
- Users may only access incidents they are authorised to view.
- Only the reporting User may accept or reject their incident's resolution.
- A rejection must include a reason.
- Feedback comments must not exceed the permitted length.
- Technicians must record troubleshooting activities before submitting a resolution.
- A resolution may only be submitted by the assigned Technician.
- An incident cannot be closed without User acceptance.
- A resolution may receive only one User decision.
- Previous resolution decisions must remain available.
- Closed incidents cannot be changed through normal workflow operations.

Validation is performed in the application service layer and, where appropriate, through SQL Server constraints.

---

## 10. Requirements and Design Reconciliation

The approved SRS and DDS provide the project requirements baseline. The following items document differences between the original design and the implemented system so that the technical documentation accurately reflects the application.

### 10.1 Knowledge Base

FR-029 to FR-031 describe Knowledge Base functionality. The module is excluded from the current implementation scope and is not delivered as part of this project.

### 10.2 Email Notifications

The original DDS scope excludes automated email and SMS notifications. The current implementation includes email notifications for resolution submission and resending pending resolution links.

The existing email functionality is retained. Its inclusion is recorded as an implementation difference that must be reconciled with the approved requirements and project guidance. This document does not claim that a separate approval for the email feature has been granted.

### 10.3 Incident Reference Format

The original design documentation provides `INC-000042` as an example incident reference format.

The current implementation generates references using the format `SD-YYYYMMDD-XXXXXX`.

The implementation format is retained and the difference is recorded here for documentation consistency. The code should not be changed solely to match the example without an agreed project decision.

### 10.4 Architecture Clarification

The original design describes a data access layer and database connectivity through `pyodbc`. The implemented system uses repositories and direct parameterised SQL statements.

The application does not use an ORM. This DDS therefore describes the actual repository and database access approach.

### 10.5 Technician Claiming

The current implementation allows Technicians to claim unassigned incidents. This operation records the assignment and audit event without automatically changing the incident status.

### 10.6 Reporting Access

The implemented reporting functionality is available to both Administrator and Supervisor roles. The permission matrix in this DDS reflects that access.

---

## 11. Requirements Traceability

The following table links the main SRS requirements to the design components responsible for implementing them.

| Requirement Area | SRS References | Design Component |
|---|---|---|
| Authentication and user roles | FR-001 to FR-005 | Authentication and Security |
| Incident registration | FR-006 to FR-008 | Incident Management |
| Incident viewing and searching | FR-009 to FR-010 | Incident Management |
| Technician incident management | FR-011 to FR-013 | Technician and Incident Management |
| Troubleshooting activities | FR-014 to FR-018 | Troubleshooting Module |
| Resolution submission | FR-019 to FR-020 | Resolution Module |
| User acceptance and rejection | FR-021 to FR-028 | Resolution Module and UserFeedback |
| Knowledge Base | FR-029 to FR-031 | Excluded from current scope |
| Reporting | FR-032 to FR-036 | Reporting Module |
| Validation and error handling | FR-037 to FR-041 | Services, Validators and Error Handling |
| Performance | NFR-001 to NFR-003 | Application and Database Architecture |
| Security | NFR-004 to NFR-008 | Authentication and Security |
| Reliability | NFR-009 to NFR-012 | Database and Transaction Management |
| Usability | NFR-013 to NFR-016 | User Interface |
| Maintainability | NFR-017 to NFR-020 | Modular Application Structure |
| Compatibility | NFR-021 to NFR-023 | Technology Design |
| Data Integrity | NFR-024 to NFR-027 | Database Design and Business Rules |

Knowledge Base requirements FR-029 to FR-031 are retained as excluded requirements and must not be treated as delivered functionality.

---

## 12. Implementation and Testing Considerations

### 12.1 Implementation Structure

The application is implemented in stages:

1. Set up the Python environment and install dependencies.
2. Configure SQL Server Express and establish database connectivity.
3. Create database tables, relationships and initial category records.
4. Develop the Flask application structure and shared templates.
5. Implement authentication and role-based access.
6. Implement incident registration, viewing and searching.
7. Implement technician assignment, claiming and troubleshooting.
8. Implement resolution submission and User acceptance or rejection.
9. Implement audit logging, administration and reporting.
10. Conduct testing, correct defects and refine the application.

### 12.2 Testing Strategy

Testing includes:

- Unit tests for validation and service-level business rules.
- Tests for authentication and role-based access.
- Tests for incident creation, assignment and claiming.
- Tests for troubleshooting and resolution submission.
- Tests for User acceptance and rejection.
- Tests for audit logging and account management.
- Database integration tests.
- End-to-end workflow checks through the browser.
- Compilation and source-code checks.

A separate test database should be used for integration testing where practical, to prevent test data from affecting the demonstration dataset.

### 12.3 Testing Evidence

Evidence may include:

- Automated pytest results.
- Database records inspected through SSMS.
- Screenshots of role-specific application pages.
- Screenshots of incident status changes.
- Audit log records.
- Resolution history and User decision records.
- CSV and PDF report outputs.
- Demonstration of invalid input and access restrictions.

---

## 13. Design Decisions and Business Rules

The following design decisions govern the implemented workflow:

1. User accounts are created and managed by an Administrator; public self-registration is disabled.
2. Technicians may claim unassigned incidents.
3. Administrators may assign and reassign incidents.
4. Administrator and Supervisor roles do not directly change incident statuses through the normal incident workflow.
5. Closed incidents are final and cannot be reopened through normal application operations.
6. Each resolution attempt has its own record.
7. Each resolution attempt may receive only one User decision.
8. Rejection feedback must be provided before a resolution can be rejected.
9. The password policy requires at least eight characters, including a letter and a digit.
10. The session inactivity timeout is 30 minutes.
11. Incident categories are inserted through a database seed script rather than managed through a category administration screen.
12. A Technician with outstanding non-Closed incidents must have those incidents reassigned before account deactivation.
13. Troubleshooting actions may only be added while an incident is In Progress.
14. A resolution cannot be submitted until at least one troubleshooting action has been recorded for the current investigation cycle.
15. An incident can only be closed after the reporting User accepts a proposed resolution.

---

## 14. Conclusion

This System Design Specification defines the technical architecture and design approach for SupportDesk Pro.

It documents the technology stack, application structure, database entities and relationships, role permissions, incident lifecycle, application components, security controls, validation rules and requirements traceability.

The design focuses on maintaining a clear separation between technical resolution and formal User acceptance. By storing each resolution attempt and its associated User decision, the application maintains a history of incident outcomes and supports accountability throughout the incident lifecycle.

The DDS provides the technical reference for implementation, testing, maintenance and academic evaluation.

**End of System Design Specification**
