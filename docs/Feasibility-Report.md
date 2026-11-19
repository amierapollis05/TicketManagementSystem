
# SupportDesk Pro
## Feasibility Report

**Project:** SupportDesk Pro – IT Support Ticketing & Troubleshooting Management System
**Organisation Context:** Capitec Bank – Head Office, IT Support Department (Work-Integrated Learning context)
**Prepared by:** Amier Apollis
**Project Supervisor:** Rhyno Hendricks
**Document Version:** 1.1
**Source:** Approved project documentation, Stage 1 – Planning and Feasibility Analysis
**Project Start Date:** 2 November 2026
**Development Environment:** Local academic WIL prototype

---

## 1. Introduction

### 1.1 Purpose

This report evaluates the technical, financial and operational feasibility of SupportDesk Pro. It establishes whether the proposed IT Support Ticketing and Troubleshooting Management System can be developed and demonstrated using the available resources, technologies and academic development environment.

### 1.2 Project Background

SupportDesk Pro is a student-developed software prototype informed by the IT support working environment at Capitec Bank Head Office.

The proposed application provides a centralised platform for recording IT incidents, managing support requests, tracking troubleshooting activities and documenting resolutions.

A key objective is to introduce a formal user confirmation process so that an incident is not considered fully resolved merely because a technician has submitted a proposed solution.

### 1.3 Problem Statement

The identified problem concerns the lack of a structured process for users to review and formally accept or reject completed IT support incidents.

Without formal confirmation, incidents may be marked as completed even when the reported problem remains unresolved or the user is dissatisfied with the proposed solution.

This can reduce accountability, make follow-up difficult and limit management's visibility of actual resolution outcomes.

### 1.4 Proposed Solution

SupportDesk Pro provides functionality for authorised users to:

- Register IT support incidents.
- View and manage incident records according to their roles.
- Assign incidents to technicians and allow technicians to claim unassigned incidents.
- Record troubleshooting activities.
- Submit proposed resolutions.
- Review proposed resolutions as the original reporting user.
- Accept or reject resolutions and provide rejection feedback.
- Return rejected incidents for further investigation.
- Generate basic incident reports.

---

## 2. Project Objectives

The project objectives are to:

1. Analyse an IT support process and identify opportunities for improvement.
2. Design a software solution that addresses the identified problem.
3. Develop the solution using Python and suitable supporting technologies.
4. Implement appropriate data storage and database management.
5. Apply software engineering and object-oriented programming principles where appropriate.
6. Test the application to identify and resolve defects.
7. Produce technical documentation and user instructions.
8. Evaluate the application against its documented requirements.

---

## 3. Technical Feasibility

### 3.1 Technology Assessment

The project is technically feasible because it uses accessible development technologies suitable for a local full-stack web application.

| Component | Technology | Purpose |
|---|---|---|
| Programming language | Python | Application logic |
| Backend framework | Flask | Request handling and application routing |
| Frontend | HTML5, CSS3, JavaScript | User interface and interactivity |
| Template engine | Jinja | Dynamic page rendering |
| Database | Microsoft SQL Server Express | Relational data storage |
| Database connectivity | pyodbc | Python-to-SQL Server connectivity |
| Database management | SQL Server Management Studio | Database inspection and management |
| Development environment | Visual Studio Code | Source code development |
| Version control | Git and GitHub | Source code management |
| Testing | pytest | Automated testing |

### 3.2 Hardware Requirements

The development environment requires:

- A computer or laptop capable of running Python and the required development software.
- At least 8 GB RAM recommended.
- Sufficient storage for source code, database records, dependencies and documentation.
- An internet connection for research and accessing development resources where required.

### 3.3 Software Requirements

The development environment uses:

- Windows 10 or Windows 11.
- Python 3.
- Flask and the required Python dependencies.
- Visual Studio Code.
- Microsoft SQL Server Express.
- SQL Server Management Studio.
- Git and a GitHub account.
- A compatible Microsoft SQL Server ODBC driver.

### 3.4 Technical Skills Required

The project requires knowledge of:

- Python programming and application logic.
- Web application development.
- Relational database design and SQL.
- Database connectivity.
- Input validation and error handling.
- Authentication and role-based access control.
- Testing and debugging.
- Git version control.
- Technical documentation.

### 3.5 Potential Technical Challenges

Potential challenges include:

- Establishing reliable connectivity between Flask and SQL Server.
- Maintaining accurate incident statuses throughout the resolution workflow.
- Restricting access to authorised users.
- Ensuring that only the original reporting user can accept or reject a resolution.
- Recording troubleshooting activities and retaining resolution history.
- Validating submitted information.
- Handling database errors without exposing sensitive technical information.
- Testing different incident scenarios and role permissions.

These challenges can be addressed through modular application design, server-side validation, parameterised SQL queries, role-based authorisation, database constraints and automated testing.

### 3.6 Technical Feasibility Conclusion

The project is technically feasible. The selected technologies support the required application functionality and are suitable for the available local development environment.

---

## 4. Financial Feasibility

### 4.1 Estimated Development Costs

SupportDesk Pro is developed as an academic Work-Integrated Learning project using existing computer equipment and freely available development tools.

| Resource | Estimated Cost |
|---|---:|
| Development software | R0.00 |
| Database software | R0.00 |
| Development hardware | Existing equipment |
| Hosting or deployment | R0.00 |
| Internet access | Existing connection |
| Additional resources | R0.00 |
| **Estimated additional project cost** | **R0.00** |

These estimates relate to the local academic prototype and do not represent the cost of deploying or supporting an enterprise production system.

### 4.2 Potential Benefits

The proposed system may provide the following operational benefits:

- Reduce manual follow-up associated with completed support incidents.
- Improve retrieval of incident information and resolution records.
- Provide a structured way to record user feedback.
- Identify incidents awaiting user confirmation.
- Improve visibility of accepted and rejected resolutions.
- Maintain a clearer record of incident progress.

### 4.3 Financial Feasibility Conclusion

The project is financially feasible because it can be developed and demonstrated using existing equipment and available software without requiring additional hardware purchases, commercial software licences or paid hosting.

---

## 5. Operational Feasibility

### 5.1 Operational Suitability

The application is operationally feasible within a simulated IT support environment.

It models an incident management process in which users report issues, technicians investigate them, and users formally confirm whether proposed resolutions have addressed their problems.

### 5.2 Expected Benefits

**Users:**
- Submit incidents through a centralised application.
- View their own incident records and progress.
- Review proposed resolutions.
- Accept or reject resolutions.
- Provide a reason when rejecting a resolution.

**Technicians:**
- View assigned and unassigned incidents.
- Claim unassigned incidents.
- Record troubleshooting activities.
- Submit proposed resolutions.
- Identify incidents awaiting user confirmation.
- Continue investigating rejected incidents.

**Supervisors:**
- View organisation-wide incident information.
- Monitor incident progress.
- Review reporting and resolution statistics.

**Administrators:**
- Manage user accounts.
- Assign and reassign incidents.
- View incident information and reports.

### 5.3 Training Requirements

Basic user guidance may be required to familiarise users and support personnel with the application.

Training and user instructions should cover:

- Logging in and navigating the application.
- Creating and submitting incidents.
- Viewing incident details and progress.
- Assigning or claiming incidents where authorised.
- Recording troubleshooting activities.
- Submitting proposed resolutions.
- Reviewing and deciding on proposed resolutions.
- Providing feedback when rejecting a resolution.
- Viewing reports where authorised.

### 5.4 Workflow Compatibility

The application simulates a typical IT support workflow:

1. A user submits an incident.
2. The incident is assigned to a technician or claimed by an authorised technician.
3. The technician investigates the incident.
4. Troubleshooting activities are recorded.
5. The technician submits a proposed resolution.
6. The incident moves to Awaiting User Confirmation.
7. The original reporting user reviews the proposed resolution.
8. If accepted, the incident is closed.
9. If rejected, the incident is reopened for further investigation.

### 5.5 Operational Feasibility Conclusion

The project is operationally feasible because the proposed workflow addresses the identified incident confirmation problem and can be demonstrated using simulated users and fictional incident records.

---

## 6. Project Scope

### 6.1 Included in Scope

The project includes:

- User authentication and role-based access.
- Incident registration and viewing.
- Incident searching and filtering.
- Incident assignment and technician claiming.
- Incident status management.
- Troubleshooting records.
- Resolution submission.
- User acceptance and rejection of resolutions.
- Rejection feedback.
- Reopening rejected incidents for further investigation.
- Audit history.
- Basic incident reporting.
- Input validation and error handling.
- SQL Server database management.
- Application testing and technical documentation.
- User instructions.

### 6.2 Excluded from Scope

The project excludes:

- Integration with live banking systems.
- Access to confidential employee or customer information.
- Production deployment.
- Modification of organisational infrastructure.
- Automated access to internal systems.
- Integration with real organisational authentication services.
- Advanced analytics or artificial intelligence functionality.
- Mobile application development.
- Knowledge Base functionality.
- Automated email or SMS notifications in the original documented scope.

**Implementation note:** The current application contains resolution email notification functionality. This difference from the original documented scope must be reconciled in the project documentation. Its presence does not imply permission to connect to live organisational email systems.

The application remains a locally operated academic prototype using synthetic test data unless separate authorisation is obtained.

---

## 7. Risk Analysis

| Risk | Potential Impact | Mitigation |
|---|---|---|
| Unclear requirements | Incorrect functionality | Refer to the approved requirements and document discrepancies |
| Limited development experience | Development delays | Research, test and seek appropriate guidance |
| Software errors | Application failure | Perform regular automated and manual testing |
| Data security risks | Unauthorised access | Use synthetic data, authentication, authorisation and secure coding practices |
| Scope changes | Project delays | Control changes against the approved project scope |
| Insufficient testing time | Undetected defects | Prioritise critical workflows and maintain test evidence |
| Database connectivity problems | Application functionality affected | Test database connectivity and handle connection failures |
| Incorrect status transitions | Inconsistent incident records | Validate transitions in the application service and database layers |

---

## 8. Project Deliverables

The project deliverables include:

1. Project Plan.
2. Feasibility Report.
3. Software Requirements Specification (SRS).
4. System Design Specification (DDS).
5. System architecture diagrams.
6. Database design and Entity Relationship Diagram.
7. Functional Python web application.
8. SQL Server database.
9. Test plan and test results.
10. Technical documentation.
11. User Manual.
12. Final project report and supporting evidence.

---

## 9. Feasibility Recommendation

Based on the technical, financial and operational assessments, SupportDesk Pro is considered feasible as a local academic WIL prototype.

**Technical feasibility:** The selected technologies are accessible and suitable for implementing the required application.

**Financial feasibility:** The project can be completed using existing computer equipment and available development tools without additional project expenditure.

**Operational feasibility:** The application models a realistic incident management and user confirmation workflow within a simulated environment.

### Overall Recommendation: Proceed

The project is suitable for development and academic demonstration, provided that implementation remains within the defined scope and uses synthetic test data.

---

## 10. Project Boundary and Data Protection

SupportDesk Pro is an independently developed student prototype informed by the developer's WIL context. It is not an officially commissioned, endorsed or approved Capitec production system.

The project does not authorise:

- Production deployment within Capitec.
- Connection to live banking systems.
- Use of confidential employee or customer information.
- Access to internal systems without explicit authorisation.

Development and demonstrations must use synthetic test data unless specific additional permission is obtained.

---

## 11. Conclusion

The feasibility assessment establishes that SupportDesk Pro can be developed using the available technical resources, software tools and academic development environment.

The proposed system addresses the identified problem of insufficient user confirmation after technical incident resolution. Its workflow provides a structured method for recording incidents, documenting troubleshooting, submitting resolutions and obtaining user acceptance or rejection.

The project is technically, financially and operationally feasible as a local academic prototype.

**Final recommendation: Proceed with the development, testing and evaluation of SupportDesk Pro.**
