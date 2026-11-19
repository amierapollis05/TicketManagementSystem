# SupportDesk Pro
## Software Requirements Specification (SRS)

**Project:** SupportDesk Pro – IT Support Ticketing & Troubleshooting Management System
**Organisation Context:** Capitec Bank – Head Office, IT Support Department (Academic WIL Simulation)
**Prepared by:** Amier Apollis
**Project Supervisor:** Rhyno Hendricks
**Document Version:** 1.1
**Document Date:** 15 November 2026
**Project Start Date:** 2 November 2026
**Document Status:** Approved Project Requirements Baseline
**System Environment:** Local academic WIL prototype

---

## 1. Introduction

### 1.1 Purpose

The purpose of this Software Requirements Specification (SRS) is to define the functional and non-functional requirements of SupportDesk Pro.

This document establishes the expected system behaviour, user requirements, technical constraints, business rules and acceptance criteria. It serves as a reference during the design, development, testing and evaluation phases of the Software Development Life Cycle (SDLC).

### 1.2 Project Scope

SupportDesk Pro is a web-based IT support management application designed to assist with recording, managing and tracking technical support incidents.

The system addresses the problem of incidents being marked as completed without formal confirmation from the User that the reported issue has been resolved.

The system provides the following functionality:

- User authentication and role-based access.
- Registration and management of IT support incidents.
- Viewing, searching and filtering existing incidents.
- Assignment of incidents to support technicians.
- Technician management of assigned incidents.
- Recording troubleshooting activities and proposed resolutions.
- User review of proposed resolutions.
- User acceptance or rejection of resolutions.
- Recording feedback and rejection reasons.
- Returning rejected incidents for further investigation.
- Closing incidents after User acceptance.
- Basic incident reporting and analytics.
- Input validation and error handling.
- Audit logging of important application activities.

The application is an independently developed student improvement prototype informed by operational pain points observed in the IT Support working environment at Capitec Bank Head Office. It is not an officially commissioned or endorsed Capitec system and is not intended for production deployment.

Development and demonstrations use fictional users and synthetic test data. The application must not connect to live organisational systems or process confidential employee or customer information.

### 1.3 Intended Audience

This document is intended for:

- IT Support management.
- IT Support technicians.
- Project supervisors.
- Software developers.
- Project stakeholders.
- Quality assurance personnel.

### 1.4 Definitions and Abbreviations

| Term | Definition |
|---|---|
| SRS | Software Requirements Specification |
| SDLC | Software Development Life Cycle |
| UI | User Interface |
| CRUD | Create, Read, Update and Delete |
| IT | Information Technology |
| FR | Functional Requirement |
| NFR | Non-Functional Requirement |
| DBMS | Database Management System |
| SQL | Structured Query Language |
| SSMS | SQL Server Management Studio |
| DB | Database |
| User | Person who reports an IT support incident. |
| Technician | Person responsible for investigating and resolving incidents. |
| Administrator | Person responsible for managing authorised application users and administrative functions. |
| Supervisor | Person responsible for monitoring incidents and reviewing reports. |
| Incident | A reported technical problem requiring IT support. |
| Resolution | The proposed action or solution provided to address an incident. |
| User Acceptance | Formal confirmation that the reported issue has been resolved. |
| Audit Log | A record of important actions performed within the application. |
| CSRF | Cross-Site Request Forgery |
| WIL | Work-Integrated Learning |

---

## 2. Overall System Description

### 2.1 Product Perspective

SupportDesk Pro is a standalone, full-stack web application designed to simulate an IT Support department's incident-management process.

The application provides a centralised method of recording incidents, tracking their progress and documenting troubleshooting activities and resolutions.

Users access the application through a web browser. The frontend provides the user interface, while the Python Flask backend processes requests, applies business logic and communicates with the SQL Server database.

The application introduces a formal User acceptance process. Once a technician completes the proposed technical work, the incident is moved to Awaiting User Confirmation. The reporting User can review the proposed resolution and either accept or reject it.

If the User accepts the resolution, the incident is closed. If the User rejects it, the incident is reopened for further investigation.

The application operates locally within an academic development and demonstration environment.

### 2.2 Product Functions

The system provides the following main functions:

1. Authenticate authorised users.
2. Apply role-based access restrictions.
3. Register and create support incidents.
4. Display registered incidents.
5. Search and filter incidents.
6. View incident details.
7. Assign incidents to support technicians.
8. Allow technicians to claim eligible unassigned incidents.
9. Update incident information and permitted statuses.
10. Record troubleshooting activities.
11. Submit proposed resolutions.
12. Allow Users to review proposed resolutions.
13. Accept or reject proposed resolutions.
14. Record User feedback and rejection reasons.
15. Return rejected incidents for further investigation.
16. Maintain incident and resolution history.
17. Generate basic incident reports.
18. Maintain audit records.
19. Manage application users.
20. Display appropriate validation and error messages.

### 2.3 User Classes and Characteristics

| User Role | Responsibilities |
|---|---|
| Administrator | Manage authorised users, assign and reassign incidents, view incidents and access reports. |
| User | Register incidents, view their own incidents and accept or reject proposed resolutions. |
| Technician | View assigned and unassigned incidents, claim eligible incidents, investigate incidents, record troubleshooting and submit resolutions. |
| Supervisor | View organisation-wide incident information, monitor support activity and access reports. |

### 2.4 Operating Environment

| Component | Technology |
|---|---|
| Programming language | Python 3.x |
| Backend framework | Flask |
| Frontend | HTML, CSS and JavaScript |
| Template engine | Jinja |
| Database engine | Microsoft SQL Server Express |
| Database connectivity | pyodbc |
| Database management | SQL Server Management Studio |
| Development environment | Visual Studio Code |
| Operating system | Windows 10/11 |
| User interface | Web browser |
| Version control | Git and GitHub |
| Testing | Python pytest |

### 2.5 Design and Implementation Constraints

The following constraints apply:

- The application must be developed using Python.
- Flask must be used as the backend web framework.
- HTML, CSS and JavaScript must be used for the frontend.
- Microsoft SQL Server Express must be used as the database engine.
- Python must communicate with SQL Server through pyodbc.
- SSMS must be available for database inspection and management.
- Only fictional user information and synthetic test incidents may be used.
- The application must not connect to live banking systems.
- Development must be completed within the available WIL timeframe.
- Input validation and appropriate error handling must be implemented.
- User permissions must be enforced for restricted operations.
- Database operations must use parameterised SQL queries.
- The application is intended for local academic demonstration, not production deployment.

### 2.6 Assumptions and Dependencies

The project is based on the following assumptions:

- The development computer has sufficient resources to run Python and SQL Server Express.
- Python, Flask and the required database driver are available.
- SQL Server Express and SSMS are available for development.
- The developer has access to the required development software.
- Simulated IT Support stakeholders can provide feedback.
- Fictional users and incidents will be used during development and testing.
- The project supervisor provides academic guidance and reviews project documentation.
- A compatible SQL Server ODBC driver is available for pyodbc connectivity.

---

## 3. Functional Requirements

Functional requirements describe what the application must do. Each requirement has a unique identifier and priority.

Priority definitions:

- **High:** Essential for the main system workflow.
- **Medium:** Important supporting functionality.
- **Low:** Optional or lower-priority functionality.

### 3.1 Authentication and User Management

| ID | Functional Requirement | Priority |
|---|---|---|
| FR-001 | The system shall allow authorised users to log in using their credentials. | High |
| FR-002 | The system shall identify the user's role after successful authentication. | High |
| FR-003 | The system shall restrict functionality according to the user's assigned role. | High |
| FR-004 | The Administrator shall be able to register and manage authorised users. | Medium |
| FR-005 | The system shall prevent unauthorised users from accessing restricted functions. | High |

### 3.2 Incident Management

| ID | Functional Requirement | Priority |
|---|---|---|
| FR-006 | The system shall allow Users to register new IT support incidents. | High |
| FR-007 | The system shall generate a unique reference number for each incident. | High |
| FR-008 | The system shall record the incident title, description, category, priority and creation date. | High |
| FR-009 | The system shall allow authorised users to view incident details. | High |
| FR-010 | The system shall allow users to search for incidents using relevant information. | High |
| FR-011 | The system shall allow technicians to view incidents requiring attention. | High |
| FR-012 | The system shall allow authorised technicians to update incident information and status according to permitted workflow transitions. | High |
| FR-013 | The system shall allow incidents to be assigned to support technicians. | Medium |

### 3.3 Troubleshooting Management

| ID | Functional Requirement | Priority |
|---|---|---|
| FR-014 | The system shall allow technicians to record troubleshooting activities. | High |
| FR-015 | The system shall store the actions taken during incident investigation. | High |
| FR-016 | The system shall allow technicians to record the proposed resolution. | High |
| FR-017 | The system shall associate troubleshooting records with the relevant incident. | High |
| FR-018 | The system shall allow authorised users to view previous troubleshooting records. | Medium |

### 3.4 User Acceptance and Rejection

| ID | Functional Requirement | Priority |
|---|---|---|
| FR-019 | The system shall allow technicians to mark an incident as Awaiting User Confirmation after completing the technical work. | High |
| FR-020 | The system shall allow the relevant User to view the proposed resolution. | High |
| FR-021 | The system shall allow the User to accept a completed resolution. | High |
| FR-022 | The system shall allow the User to reject a completed resolution. | High |
| FR-023 | The system shall require a reason or feedback when a User rejects a resolution. | High |
| FR-024 | The system shall close an incident after the User accepts the resolution. | High |
| FR-025 | The system shall return a rejected incident to the support team for further investigation. | High |
| FR-026 | The system shall record the User's decision, feedback and date of submission. | High |
| FR-027 | The system shall prevent Users from accepting or rejecting incidents that are not awaiting confirmation. | High |
| FR-028 | The system shall maintain a record of previous acceptance and rejection decisions. | High |

### 3.5 Knowledge Base

The following requirements were identified in the original requirements analysis but are excluded from the current implementation scope.

| ID | Functional Requirement | Priority | Scope |
|---|---|---|---|
| FR-029 | The system shall allow authorised users to create basic Knowledge Base articles. | Low | Excluded |
| FR-030 | The system shall allow users to view available troubleshooting articles. | Low | Excluded |
| FR-031 | The system shall allow authorised users to update existing Knowledge Base articles. | Low | Excluded |

The Knowledge Base module is not part of the current project implementation.

### 3.6 Reporting

| ID | Functional Requirement | Priority |
|---|---|---|
| FR-032 | The system shall generate a report of registered incidents. | Medium |
| FR-033 | The system shall display incidents according to their current statuses. | Medium |
| FR-034 | The system shall identify incidents Awaiting User Confirmation. | High |
| FR-035 | The system shall display the number of accepted and rejected resolutions. | Medium |
| FR-036 | The system shall provide basic incident statistics. | Low |

### 3.7 Input Validation and Error Handling

| ID | Functional Requirement | Priority |
|---|---|---|
| FR-037 | The system shall validate required fields before saving information. | High |
| FR-038 | The system shall reject invalid input values. | High |
| FR-039 | The system shall display appropriate error messages when operations fail. | High |
| FR-040 | The system shall prevent invalid incident status transitions. | High |
| FR-041 | The system shall handle database connection and query errors appropriately. | High |

---

## 4. Non-Functional Requirements

Non-functional requirements define the quality standards and operating characteristics the application must satisfy.

### 4.1 Performance

| ID | Requirement |
|---|---|
| NFR-001 | The application should respond to normal user operations within an acceptable timeframe. |
| NFR-002 | The system should retrieve incident records efficiently. |
| NFR-003 | Database operations should complete efficiently for the expected academic test dataset. |

### 4.2 Security

| ID | Requirement |
|---|---|
| NFR-004 | The system must authenticate users before granting access to protected functions. |
| NFR-005 | User permissions must be based on assigned roles. |
| NFR-006 | Passwords must not be stored as plain text. |
| NFR-007 | Database queries must use parameterised statements to reduce SQL injection risks. |
| NFR-008 | The application must use fictional information and must not expose confidential organisational data. |

### 4.3 Reliability

| ID | Requirement |
|---|---|
| NFR-009 | The application should store valid incident information accurately. |
| NFR-010 | The system should prevent incomplete or invalid records from being saved. |
| NFR-011 | The system should handle unexpected errors without terminating unnecessarily. |
| NFR-012 | Important incident status changes and User decisions should be recorded consistently. |

### 4.4 Usability

| ID | Requirement |
|---|---|
| NFR-013 | The application should provide clear menu options and instructions. |
| NFR-014 | Error messages should explain what went wrong and, where possible, how to correct the problem. |
| NFR-015 | The system should use consistent terminology for incidents, statuses and user roles. |
| NFR-016 | Users should be able to perform common operations without unnecessary complexity. |

### 4.5 Maintainability

| ID | Requirement |
|---|---|
| NFR-017 | The application should use modular and organised Python code. |
| NFR-018 | Functions should have clear responsibilities. |
| NFR-019 | Source code should include appropriate comments and documentation. |
| NFR-020 | The application should allow future improvements without requiring a complete redesign. |

### 4.6 Compatibility

| ID | Requirement |
|---|---|
| NFR-021 | The application must operate in the selected Windows development environment. |
| NFR-022 | The Python application must be compatible with the selected SQL Server database driver. |
| NFR-023 | The database must be accessible through SQL Server Management Studio. |

### 4.7 Data Integrity

| ID | Requirement |
|---|---|
| NFR-024 | Each incident must have a unique identifier. |
| NFR-025 | Related database records must maintain valid relationships. |
| NFR-026 | A User must only be able to submit an acceptance or rejection decision for an incident associated with that User. |
| NFR-027 | An incident must not be considered fully closed until the User has accepted the resolution. |

---

## 5. Business Rules

The following business rules define how the application must operate.

| ID | Business Rule |
|---|---|
| BR-01 | Every registered incident must have a unique incident reference number. |
| BR-02 | Every incident must be associated with a User. |
| BR-03 | Only authorised technicians may update technical incident information. |
| BR-04 | Technicians must record troubleshooting actions before submitting a resolution for User confirmation. |
| BR-05 | An incident must be marked as Awaiting User Confirmation before the User can accept or reject it. |
| BR-06 | Only the User associated with an incident may submit its acceptance or rejection decision. |
| BR-07 | A User must provide feedback when rejecting a resolution. |
| BR-08 | An accepted incident must move to Closed status. |
| BR-09 | A rejected incident must return to the support team for further investigation. |
| BR-10 | A reopened incident must be investigated before another User confirmation request can be submitted. |
| BR-11 | Previous User decisions must remain available as historical records. |
| BR-12 | Users must only access functionality permitted by their assigned roles. |

### 5.1 Incident Status Definitions

| Status | Description |
|---|---|
| Open | An incident has been registered and is awaiting investigation. |
| In Progress | A technician is investigating or working on the incident. |
| Awaiting User Confirmation | The technician has submitted a proposed resolution and is waiting for the User's decision. |
| Reopened | The User has rejected the proposed resolution and further investigation is required. |
| Closed | The User has accepted the resolution and the incident is considered resolved. |

### 5.2 Incident Status Workflow

**Normal workflow:**

`Open → In Progress → Awaiting User Confirmation → Closed`

**Rejected resolution workflow:**

`Awaiting User Confirmation → Reopened → In Progress → Awaiting User Confirmation`

The process may repeat until the User accepts the resolution.

A Closed incident is terminal and cannot be reopened through the normal incident workflow.

---

## 6. External Interface Requirements

### 6.1 User Interface

The interface must provide:

- A login page.
- Role-specific navigation and functionality.
- Incident registration.
- Incident viewing and searching.
- Incident management for technicians.
- Incident assignment and administration.
- Troubleshooting record functionality.
- Resolution review and acceptance or rejection.
- Basic reporting functionality.
- Clear success and error messages.
- Appropriate access-denied and error pages.

### 6.2 Software Interfaces

| Software | Purpose |
|---|---|
| Python | Executes application functionality. |
| Flask | Processes application requests and routes. |
| Microsoft SQL Server Express | Stores application information. |
| SQL Server Management Studio | Provides database management and inspection. |
| pyodbc | Connects the Python application to SQL Server. |
| Git | Tracks source-code changes. |
| GitHub | Hosts and manages the project repository. |
| pytest | Executes automated tests. |

### 6.3 Database Interface

The application must communicate with SQL Server to store, retrieve and update application information.

The database must contain records relating to:

- Users.
- Incidents.
- Categories.
- Troubleshooting records.
- Resolutions.
- User feedback.
- Audit logs.

The database must maintain relationships between relevant records to preserve data integrity.

The Knowledge Base entity is excluded from the current implementation.

---

## 7. Data Requirements

### 7.1 Main Data Entities

| Entity | Purpose |
|---|---|
| Users | Stores user details, login information, account status and assigned roles. |
| Categories | Stores incident categories such as Hardware, Software, Network and Access Issues. |
| Incidents | Stores incident details, priorities, statuses, reporting users and assigned technicians. |
| TroubleshootingRecords | Stores investigation activities and technical actions. |
| Resolutions | Stores proposed resolutions submitted by technicians. |
| UserFeedback | Stores User acceptance or rejection decisions and comments. |
| AuditLogs | Records important application activities and status changes. |

### 7.2 Data Validation

The system must validate information before storing it in the database.

Examples include:

- Required fields must not be empty.
- User email addresses must follow a valid format.
- Passwords must satisfy the defined password requirements.
- Incident priorities must use approved values.
- Incident statuses must use approved values.
- Each incident must have a valid User reference.
- Each assigned technician must be a valid authorised account.
- User rejection decisions must include a reason.
- Database relationships must reference existing records.
- Duplicate user email addresses must be prevented.
- Invalid incident status transitions must be rejected.

### 7.3 Data Storage

Application information is stored in Microsoft SQL Server Express.

The database

## 8. Use Cases

| Use Case | Actor | Description |
|---|---|---|
| UC-01: Login | All users | User enters credentials to access the application. |
| UC-02: Register Incident | User | User creates a new support incident. |
| UC-03: View Incident | User, Technician, Supervisor, Administrator | User views incident information according to permissions. |
| UC-04: Assign Incident | Administrator | Administrator assigns an incident to a support technician. |
| UC-05: Update Incident | Technician | Technician updates permitted incident information and status. |
| UC-06: Record Troubleshooting | Technician | Technician records investigation activities. |
| UC-07: Submit for Confirmation | Technician | Technician submits a proposed resolution and moves the incident to Awaiting User Confirmation. |
| UC-08: Accept Resolution | User | User accepts the proposed resolution and the incident is closed. |
| UC-09: Reject Resolution | User | User rejects the proposed resolution and provides feedback. |
| UC-10: Reinvestigate Incident | Technician | Technician investigates a rejected incident. |
| UC-11: Generate Report | Supervisor, Administrator | Authorised users view and export incident reports. |
| UC-12: Manage Users | Administrator | Administrator manages authorised application users. |

---

## 9. Requirements Validation and Acceptance Criteria

The application will be evaluated against the following acceptance conditions:

1. A User can log in successfully using valid credentials.
2. Users can only access functions permitted by their assigned roles.
3. A User can register a new incident.
4. Each incident receives a unique reference number.
5. Technicians can view and manage incidents within their permissions.
6. Technicians can record troubleshooting actions and proposed resolutions.
7. Technicians can submit completed incidents for User confirmation.
8. Users can view the proposed resolution.
9. Users can accept a proposed resolution.
10. Accepted incidents are automatically moved to Closed status.
11. Users can reject a proposed resolution and provide a reason.
12. Rejected incidents are returned to the support team for further investigation.
13. The system stores User decisions and relevant feedback.
14. Invalid information is rejected with appropriate error messages.
15. Incident information is successfully stored and retrieved from SQL Server.
16. Basic incident reports can be generated.
17. Unauthorised users cannot access restricted application functions.
18. Previous resolution decisions remain available as historical records.
19. Invalid status transitions are prevented.
20. Database failures are handled without exposing sensitive technical information to application users.

The User acceptance and rejection workflow is the most important acceptance criterion because it directly addresses the problem identified during project planning.

---

## 10. Requirements Traceability Matrix

| Identified Problem or Requirement | Requirement Reference | Planned Verification |
|---|---|---|
| Users cannot formally confirm completed incidents. | FR-021 | Verify that a User can accept an incident awaiting confirmation. |
| Users cannot reject unsuccessful resolutions. | FR-022 | Verify that a User can reject a proposed resolution. |
| Rejection reasons are not formally recorded. | FR-023 and BR-07 | Verify that a rejection without a reason is prevented. |
| Incidents may be closed without User confirmation. | FR-024, NFR-027 and BR-08 | Verify that an incident closes only after acceptance. |
| Rejected incidents require additional investigation. | FR-025 and BR-09 | Verify that rejected incidents return to the support team. |
| Previous User decisions may not be available. | FR-026, FR-028 and BR-11 | Verify that acceptance and rejection records are retained. |
| Users may access restricted functions. | FR-003, FR-005 and NFR-005 | Verify role-specific access restrictions. |
| Incident information may be difficult to locate. | FR-009 and FR-010 | Verify incident viewing and search functionality. |
| Support management lacks visibility of confirmation status. | FR-034 and FR-035 | Verify reports identify pending, accepted and rejected incidents. |
| Invalid information may be stored. | FR-037 and FR-038 | Verify required-field and invalid-input validation. |
| Incorrect status changes may occur. | FR-040 and BR-05 | Verify that invalid status transitions are prevented. |
| Database operations may fail. | FR-041 and NFR-011 | Verify appropriate handling of database errors. |

---

## 11. Scope and Implementation Reconciliation

The approved requirements baseline remains the reference for project evaluation.

### 11.1 Knowledge Base

FR-029 to FR-031 describe Knowledge Base functionality. This module is excluded from the current project implementation and is not required for the current assessment scope.

### 11.2 Email Notifications

The original project scope excludes automated email or SMS notifications. The current implementation contains email functionality for resolution notifications and resending pending resolution links.

This is an implementation difference that must be reconciled with the approved requirements and supervisor guidance. Existing functionality is retained unless an authorised project decision requires a change.

### 11.3 Incident Reference Format

The design documentation specifies an example reference format of `INC-000042`. The current implementation uses the format `SD-YYYYMMDD-XXXXXX`.

The difference must be recorded and reconciled with the design documentation. The implementation should not be silently changed without an agreed project decision.

---

## 12. Conclusion

This Software Requirements Specification defines the functional requirements, non-functional requirements, business rules, operating environment, data requirements and acceptance criteria for SupportDesk Pro.

The system is intended to improve IT support incident management by introducing a formal User confirmation process.

By allowing Users to accept or reject proposed resolutions, the application provides greater visibility into incident outcomes and distinguishes technical completion from confirmed resolution.

The requirements documented in this SRS provide the baseline for system design, implementation, testing and evaluation.

**End of Software Requirements Specification**
