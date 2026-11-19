# SupportDesk Pro
## Project Plan

**Project:** SupportDesk Pro – IT Support Ticketing & Troubleshooting Management System
**Organisation Context:** Capitec Bank – Head Office, IT Support Department (Academic WIL Simulation)
**Prepared by:** Amier Apollis
**Project Supervisor:** Rhyno Hendricks
**Document Version:** 1.1
**Project Start Date:** 2 November 2026
**Project Period:** 2 November 2026 – 20 November 2026 (WIL placement period)
**Development Environment:** Local academic WIL prototype
**Project Status:** Implementation and assessment-readiness activities

---

## 1. Introduction

This Project Plan defines the activities, resources, responsibilities, risks and expected deliverables for the development of SupportDesk Pro.

SupportDesk Pro is an IT Support Ticketing and Troubleshooting Management System developed as part of a Work-Integrated Learning (WIL) project. The application simulates an IT support environment and provides a centralised platform for recording incidents, managing support requests, documenting troubleshooting activities and tracking resolution outcomes.

The main objective is to introduce a formal User acceptance process so that an incident is only closed after the User has accepted the proposed resolution.

This project is an academic simulation and is not an officially commissioned or endorsed Capitec Bank system. It operates locally using fictional accounts and test data. It does not connect to live banking systems or use confidential employee or customer information.

## 2. Project Objectives

The objectives are to:

1. Investigate the existing IT support incident-management process and identify its limitations.
2. Define and document functional and non-functional system requirements.
3. Design the system architecture, database structure and application workflows.
4. Develop a web-based application using Python and Flask.
5. Implement a relational database using Microsoft SQL Server Express.
6. Implement authentication and role-based access control.
7. Provide incident registration, searching, assignment and tracking.
8. Allow technicians to record troubleshooting activities and submit resolutions.
9. Implement User acceptance and rejection of proposed resolutions.
10. Maintain incident history, feedback and audit records.
11. Implement reporting and administrative functionality.
12. Test the application, identify defects and verify that requirements are met.
13. Produce technical documentation and user instructions.
14. Evaluate the completed application against the project requirements.

## 3. Project Scope

### 3.1 Included in scope

- User authentication and role-based access.
- Administrator-managed user accounts.
- Incident registration and viewing.
- Incident searching and filtering.
- Incident assignment and technician claiming of unassigned incidents.
- Incident status management.
- Troubleshooting activity records.
- Resolution submission.
- User acceptance or rejection of resolutions.
- Rejection feedback and reasons.
- Reopening incidents after rejected resolutions.
- Resolution and incident history.
- Audit logging of important system activities.
- Supervisor dashboard and oversight.
- Incident reporting and analytics.
- CSV and PDF report exports.
- Input validation and error handling.
- Database management using SQL Server Express.
- Application testing and technical documentation.

### 3.2 Excluded from scope

- Integration with live banking systems.
- Access to confidential employee or customer information.
- Production deployment.
- Modification of existing organisational infrastructure.
- Integration with real company authentication services.
- Mobile application development.
- Advanced artificial intelligence functionality.
- Knowledge Base functionality.
- Live integration with organisational systems.

The approved project scope is retained. Any implementation differences must be recorded and reconciled with the project documentation.

## 4. Project Methodology

The project follows a structured Software Development Life Cycle (SDLC), with distinct planning, analysis, design, implementation and testing activities.

### Stage 1: Planning and Feasibility Analysis

Activities:
- Identify the business problem.
- Investigate the current incident-management process.
- Define the project objectives and boundaries.
- Evaluate technical, financial and operational feasibility.
- Identify resources and potential risks.

Deliverable: Feasibility Report.

### Stage 2: Requirements Analysis

Activities:
- Identify system users and their responsibilities.
- Define functional requirements.
- Define non-functional requirements.
- Establish business rules and acceptance criteria.
- Document system constraints and assumptions.

Deliverable: Software Requirements Specification (SRS).

### Stage 3: System Design

Activities:
- Design the system architecture.
- Define application modules and responsibilities.
- Design the relational database and entity relationships.
- Define role permissions.
- Design incident and resolution workflows.
- Identify security and validation controls.

Deliverable: Design Document Specification (DDS).

### Stage 4: Implementation

Activities:
- Configure the Python development environment.
- Establish SQL Server connectivity.
- Create database tables, relationships and seed data.
- Develop the Flask application.
- Implement authentication and authorisation.
- Develop incident-management functionality.
- Implement troubleshooting and resolution workflows.
- Implement reporting and administrative functions.
- Integrate the application layers.

Deliverables:
- Application source code.
- SQL database scripts.
- Working local application.

### Stage 5: Testing and Quality Assurance

Activities:
- Conduct unit testing.
- Test service and repository functionality.
- Test database connectivity and operations.
- Test role-based permissions.
- Test incident lifecycle scenarios.
- Test resolution acceptance and rejection.
- Test validation and error handling.
- Perform regression testing after changes.
- Record and resolve defects.

Deliverables:
- Test cases and results.
- Automated test suite.
- Defect and verification records.

### Stage 6: Documentation and Assessment Readiness

Activities:
- Complete the project documentation.
- Prepare the user manual.
- Verify the README and setup instructions.
- Review security controls.
- Verify requirements against implemented functionality.
- Capture screenshots and supporting evidence.
- Prepare the project demonstration.
- Complete WIL logbook evidence and required sign-offs.

Deliverables:
- Completed project documentation.
- User manual.
- Test evidence.
- Screenshots and demonstration material.
- WIL assessment evidence.

**Deployment note:** The project is intended to run locally for academic demonstration and assessment. Production deployment is outside the project scope.

## 5. Project Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Project Developer – Amier Apollis | Requirements analysis, design, coding, database development, testing and documentation. |
| Project Supervisor – Rhyno Hendricks | Provide guidance, review progress and oversee project requirements and WIL activities. |
| Simulated Users | Submit incidents, monitor progress and review proposed resolutions. |
| Simulated Technicians | Investigate incidents, record troubleshooting and submit resolutions. |
| Simulated Administrator | Manage user accounts, assign incidents and oversee administrative functions. |
| Simulated Supervisor | Monitor system activity and review reports. |

## 6. Resource Planning

| Resource | Purpose |
|---|---|
| Python 3 | Main programming language. |
| Flask | Backend web application framework. |
| HTML5, CSS3 and JavaScript | User interface and browser functionality. |
| Jinja | Dynamic HTML templates. |
| Microsoft SQL Server Express | Relational database management. |
| SQL Server Management Studio | Database administration and inspection. |
| pyodbc | Python-to-SQL Server connectivity. |
| Visual Studio Code | Source-code development and editing. |
| Git and GitHub | Source-code version control and project backup. |
| pytest | Automated application testing. |
| Windows computer | Local development and demonstration environment. |
| Internet connection | Research and development support. |

The project uses existing development equipment and freely available development tools. No paid hosting or production infrastructure is required.

## 7. Project Schedule and Milestones

The project follows the WIL placement period from 2 November 2026 to 20 November 2026.

| Phase | Planned activity | Progress |
|---|---|---|
| 1 | Planning and feasibility analysis | Documentation prepared. |
| 2 | Requirements analysis | SRS prepared as part of the approved project documentation. |
| 3 | System design | DDS prepared as part of the approved project documentation. |
| 4 | Environment and database setup | Flask environment and SQL Server database established. |
| 5 | Core application development | Main application functionality implemented. |
| 6 | User acceptance workflow | Resolution submission, acceptance and rejection implemented and tested. |
| 7 | Testing and quality assurance | Automated tests and functional verification conducted. |
| 8 | Documentation and assessment readiness | Documentation restoration, requirements audit and evidence preparation in progress. |

The schedule identifies project phases and progress without assigning unverified completion dates or claiming activities that have not been recorded.

## 8. Risk Management

| Risk | Potential impact | Mitigation |
|---|---|---|
| Unclear requirements | Incorrect functionality or rework | Use the approved SRS and DDS as the project baseline. |
| Limited development experience | Delays and implementation difficulties | Research technical issues, test incrementally and seek guidance. |
| Software defects | Application failure or incorrect results | Use automated tests, manual verification and regression testing. |
| Database connection problems | Application unable to retrieve or store records | Verify SQL Server configuration and test database connectivity. |
| Unauthorised access | Users accessing restricted functions | Implement authentication, role checks and session controls. |
| Data security risks | Exposure of sensitive information | Use fictional test data, password hashing, parameterised SQL and appropriate security controls. |
| Invalid incident data | Inconsistent or incomplete records | Apply input validation and database constraints. |
| Scope changes | Delays and unnecessary development | Maintain the approved scope and document required changes. |
| Insufficient testing | Undetected defects | Test normal, invalid, boundary and role-specific scenarios. |
| Documentation gaps | Incomplete assessment evidence | Maintain and verify project documentation throughout the finalisation stage. |

## 9. Testing Strategy

Testing is conducted to verify that the application meets its functional and non-functional requirements.

The testing strategy includes:

- **Unit testing:** Verify individual validation, service and repository functions.
- **Integration testing:** Verify interactions between application layers and the SQL Server database.
- **Functional testing:** Verify incident creation, assignment, searching, troubleshooting and resolution workflows.
- **Security testing:** Verify authentication, role permissions, session behaviour, CSRF protection and access restrictions.
- **Validation testing:** Verify that invalid or incomplete information is rejected.
- **Regression testing:** Confirm that changes do not break existing functionality.

The automated test suite has reached 154 passing tests at the time this plan was updated. This result is evidence of automated verification, not a claim that every requirement has already passed formal user acceptance testing.

## 10. Project Monitoring and Control

Project progress is monitored through:

- Comparing implementation against the approved SRS and DDS.
- Reviewing completed project milestones.
- Running automated tests after significant changes.
- Checking application behaviour through the browser.
- Inspecting database records and audit history.
- Reviewing source-code changes through Git.
- Recording outstanding defects and documentation tasks.
- Maintaining WIL logbook evidence for activities actually completed.

Changes to the approved requirements must be identified and documented rather than silently introduced into the application.

## 11. Expected Project Deliverables

The expected deliverables are:

1. Feasibility Report.
2. Software Requirements Specification.
3. Design Document Specification.
4. Flask application source code.
5. SQL Server database creation and seed scripts.
6. Automated test suite and test results.
7. Project README and setup instructions.
8. User Manual.
9. Architecture diagram.
10. Entity Relationship Diagram.
11. Incident workflow diagram.
12. Screenshots and practical demonstration evidence.
13. WIL logbook and supporting assessment evidence.

## 12. Project Constraints and Assumptions

- The application is developed for an academic WIL simulation.
- The application runs locally on the developer's computer.
- Fictional users and test records are used.
- No live banking systems are accessed.
- No confidential employee or customer information is used.
- The project uses the technologies identified in the approved design.
- The project is limited to the functionality defined in the approved scope.
- Project completion and WIL sign-off must be based on actual completed work and verified evidence.

## 13. Scope Reconciliation Note

The approved planning documentation excludes automated email or SMS notifications. The current implementation contains email functionality for resolution notifications and resending pending resolution links.

This implementation difference must remain visible in the project records and be reconciled with the approved requirements and supervisor guidance. Existing functionality is retained unless an authorised project decision requires a change.

The incident reference format and any other differences between the approved design and the implemented application must likewise be recorded and reconciled.

## 14. Conclusion

This Project Plan establishes the approach for developing, testing and documenting SupportDesk Pro within the WIL placement period.

The project follows a structured SDLC and uses Python, Flask and Microsoft SQL Server Express to provide a centralised IT incident-management application.

The main purpose is to improve incident tracking and accountability by ensuring that proposed resolutions are reviewed by the reporting User before incidents are closed.

The final project activities focus on verifying the implementation against the approved requirements, completing the documentation, reviewing security and testing evidence, and preparing the application for local academic demonstration and assessment.

**End of Project Plan**
