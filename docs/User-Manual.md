# SupportDesk Pro – User Manual

**Project:** SupportDesk Pro – IT Support Ticketing & Troubleshooting Management System
**Document:** User Manual
**Version:** 1.0
**Document Status:** Approved Project Documentation
**Application Type:** Local web-based application
**Operating Environment:** Windows 10/11
**Database:** Microsoft SQL Server Express

---

## 1. Introduction

### 1.1 Purpose of This Manual

This User Manual explains how to access and use SupportDesk Pro.

It provides step-by-step instructions for the four application roles:

- User
- Technician
- Administrator
- Supervisor

The manual covers login, incident registration, incident tracking, technician assignment, troubleshooting, resolution submission, User confirmation, account management and reporting.

### 1.2 About SupportDesk Pro

SupportDesk Pro is a web-based IT Support Ticketing and Troubleshooting Management System developed as an academic Workplace Integrated Learning project.

The system provides a centralised environment for reporting, managing and tracking IT support incidents.

A key feature is the User confirmation workflow. Technicians submit proposed resolutions for review, and the reporting User must accept or reject the resolution. An incident is only closed after the User accepts the proposed resolution.

### 1.3 Intended Users

| Role | Main Responsibilities |
|---|---|
| User | Register incidents, track personal incidents and review proposed resolutions. |
| Technician | Claim or investigate incidents, record troubleshooting and submit resolutions. |
| Administrator | Manage user accounts and assign incidents to Technicians. |
| Supervisor | Monitor incident activity and access reports. |

### 1.4 System Requirements

To use the local application, the following are required:

- A Windows 10 or Windows 11 computer.
- A supported modern web browser.
- The SupportDesk Pro application running locally.
- A working connection to the configured SQL Server Express database.
- A valid application account.

The application is intended for local academic demonstration and is not a production banking system.

---

## 2. Accessing the Application

### 2.1 Starting SupportDesk Pro

The application must be started on the computer where the project is installed.

1. Open Windows PowerShell.
2. Navigate to the project directory:

```powershell
cd "C:\Users\Amier Apollis\OneDrive - CTU Career\Desktop\TicketManagementSystem"
```

3. Activate the Python virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Start the application:

```powershell
python run.py
```

5. Wait for Flask to indicate that the application is running.
6. Open a web browser and navigate to the local address shown in the terminal. The usual development address is:

```text
http://127.0.0.1:5000
```

The terminal window must remain open while using the application.

### 2.2 Logging In

1. Open the SupportDesk Pro login page.
2. Enter your registered email address.
3. Enter your password.
4. Select the login button.
5. If the credentials are valid, the application opens the appropriate page for your assigned role.

If login fails, check that:

- The email address is correct.
- The password is correct.
- The account is active.
- The application and database are running.

The application displays a general authentication error when credentials are invalid.

### 2.3 Role-Based Navigation

After login, the navigation menu displays the pages available to the current account.

Different roles have different permissions. A User cannot access Administrator functions, and a Technician cannot access Supervisor-only functionality.

### 2.4 Logging Out

1. Open the application navigation menu.
2. Select the Logout option.
3. The application ends the authenticated session and returns to the login page.

Users should log out when they have finished using the application.

---

## 3. User Guide

### 3.1 User Dashboard

The User dashboard provides access to the incident functionality available to the signed-in User.

A User can:

- Create a new incident.
- View their own reported incidents.
- Search and filter their incidents.
- Open incident details.
- Review proposed resolutions when an incident is awaiting confirmation.

Users cannot view or manage other users' private incidents.

### 3.2 Creating a New Incident

To report an IT support issue:

1. Log in using a User account.
2. Open the incident creation page.
3. Enter a short, descriptive incident title.
4. Enter a detailed description of the problem.
5. Select the relevant incident category.
6. Select the incident priority.
7. Submit the form.

The system validates the submitted information.

If the information is valid:

- The incident is saved in the database.
- A unique incident reference is generated.
- The incident is associated with the signed-in User.
- The initial status is Open.

Keep the incident reference available when discussing the reported issue.

### 3.3 Viewing My Incidents

1. Log in as a User.
2. Open My Incidents from the navigation menu.
3. Review the list of incidents reported by your account.
4. Select an incident reference to open its details.

The incident list provides information such as:

- Incident reference.
- Title.
- Category.
- Priority.
- Current status.
- Date reported.

Only incidents belonging to the signed-in User are displayed.

### 3.4 Searching and Filtering Incidents

The My Incidents page provides search and filter controls.

A User can:

1. Enter an incident reference, title or description into the search field.
2. Select a status filter if required.
3. Select a priority filter if required.
4. Select a category filter if required.
5. Apply the search or filter.
6. Review the matching incidents.

To remove the selected filters, use the Clear Filters option.

### 3.5 Viewing Incident Details

1. Open My Incidents.
2. Select the incident reference.
3. Review the incident information.

The details page may display:

- Incident reference and title.
- Description and category.
- Priority and current status.
- Reporting date.
- Assigned Technician, where applicable.
- Troubleshooting history.
- Resolution history.
- User feedback and previous decisions.

This information allows the User to follow the progress of the reported issue.

### 3.6 Reviewing a Proposed Resolution

When a Technician submits a resolution, the incident moves to Awaiting User Confirmation.

The reporting User can review the proposed resolution through the resolution review link sent by email.

To review the resolution:

1. Open the resolution notification email.
2. Follow the supplied review link.
3. Review the incident and proposed resolution details.
4. Decide whether the proposed resolution has resolved the reported problem.

The review link is time-limited and expires after seven days.

If the link has expired or is invalid, the review page will not be available. Contact the support team to request assistance with the pending resolution.

### 3.7 Accepting a Resolution

If the reported issue has been resolved:

1. Open the resolution review page.
2. Read the proposed resolution.
3. Select the Accept option.
4. Submit the decision.

After acceptance:

- The system records the User's decision.
- The incident status changes to Closed.
- The closure date is recorded.
- The decision remains available in the incident history.

### 3.8 Rejecting a Resolution

If the reported issue has not been resolved:

1. Open the resolution review page.
2. Read the proposed resolution.
3. Select the Reject option.
4. Enter a clear explanation of why the issue remains unresolved.
5. Submit the decision.

A rejection reason is mandatory.

After rejection:

- The system records the rejection and comments.
- The incident status changes to Reopened.
- The incident returns to the support workflow.
- A Technician can investigate the issue further.
- A new resolution can be submitted for review.

The previous resolution and rejection reason remain in the incident history.

---

## 4. Technician Guide

### 4.1 Technician Dashboard

The Technician dashboard provides an overview of incidents requiring attention.

It provides access to incident queues and information such as:

- Reopened incidents.
- The Technician's active incidents.
- Unassigned incidents available to claim.
- Incident details and current status.

Technicians should review their queues regularly to identify incidents requiring investigation.

### 4.2 Viewing the Technician Incident Queue

1. Log in using a Technician account.
2. Open the Technician incidents page.
3. Review the available incidents.
4. Select an incident reference to view its details.

The Technician can search and filter incidents using the available search, status, priority and category controls.

### 4.3 Claiming an Unassigned Incident

A Technician can claim an incident that has not yet been assigned.

1. Open the Technician dashboard or incident queue.
2. Locate an unassigned incident.
3. Select the Claim option.
4. Wait for the application to process the request.
5. Confirm that the incident is now assigned to your account.

The system checks that the incident is still unassigned and is not Closed.

If another Technician claims the incident first, the claim will not succeed.

Claiming an incident changes its assigned Technician but does not automatically change its status.

### 4.4 Working on an Assigned Incident

1. Open the incident details page.
2. Review the incident description, category and priority.
3. Review any existing troubleshooting history.
4. Begin the investigation.
5. Move the incident to In Progress when investigation begins, where the permitted status action is available.

Only the assigned Technician can perform the permitted technical operations for that incident.

### 4.5 Recording Troubleshooting Activities

Technicians must record investigation activities so that the system maintains a history of the work performed.

1. Open an assigned incident.
2. Ensure the incident is In Progress.
3. Locate the troubleshooting section.
4. Enter a clear description of the action performed.
5. Submit the troubleshooting record.
6. Confirm that the action appears in the incident history.

Troubleshooting records should describe the investigation accurately and clearly.

Examples include:

- Checked the network cable and connection status.
- Restarted the workstation and tested connectivity.
- Verified printer configuration and connectivity.
- Reinstalled the required device driver.

Troubleshooting actions can only be added while an incident is In Progress.

### 4.6 Submitting a Proposed Resolution

After completing the investigation:

1. Open the assigned incident.
2. Confirm that the required troubleshooting activity has been recorded.
3. Enter a clear description of the proposed resolution.
4. Submit the resolution.

The system verifies that:

- The Technician is assigned to the incident.
- The incident is in an eligible status.
- At least one troubleshooting action has been recorded for the current investigation cycle.
- The submitted resolution contains valid information.

If the checks pass:

- A new resolution record is created.
- The incident moves to Awaiting User Confirmation.
- An audit event is recorded.
- The reporting User is notified through the configured email functionality.

The Technician should not treat the incident as Closed merely because the technical work has been completed.

### 4.7 Resending a Pending Resolution Notification

If the reporting User has not received or acted on the resolution notification, the assigned Technician may use the available resend functionality for an eligible pending resolution.

The resend operation:

- Applies to a resolution that is still awaiting User confirmation.
- Does not create a new resolution attempt.
- Does not change the incident status.
- Sends a fresh time-limited review link.
- Records the resend activity after successful email delivery.

### 4.8 Handling a Rejected Resolution

When a User rejects a resolution:

1. The incident moves to Reopened.
2. The rejection reason is retained.
3. The Technician reviews the User's feedback.
4. The Technician resumes investigation.
5. The incident is moved to In Progress.
6. Additional troubleshooting is recorded.
7. A new proposed resolution is submitted.

Each resolution attempt remains available in the incident history.

---

## 5. Administrator Guide

### 5.1 Administrator Dashboard

The Administrator dashboard provides access to administrative functions.

An Administrator can:

- View and manage incidents.
- Search and filter incidents.
- Assign incidents to Technicians.
- Reassign incidents.
- Create user accounts.
- Search and manage user accounts.
- Change user roles.
- Activate and deactivate accounts.
- Access incident reports and exports.

Administrative functions are restricted to authorised Administrator accounts.

### 5.2 Viewing and Managing Incidents

1. Log in using an Administrator account.
2. Open the incident management page.
3. Review the incident list.
4. Select an incident reference to inspect its details.

Administrators can view incidents across the system.

### 5.3 Searching and Filtering Incidents

The Administrator incident page supports searching and filtering.

1. Enter a search term to locate an incident.
2. Select a status if required.
3. Select a priority if required.
4. Select a category if required.
5. Apply the filters.
6. Review the matching incidents.

The search supports relevant incident information, including incident references, titles and descriptions. Administrator searches also include reporter information where supported.

Select Clear Filters to reset the search.

### 5.4 Assigning a Technician

1. Open the Administrator incident management page.
2. Locate the incident that requires assignment.
3. Open the incident's assignment controls.
4. Select an eligible Technician.
5. Submit the assignment.
6. Confirm that the assigned Technician is displayed.

The system records the assignment in the audit history.

### 5.5 Reassigning a Technician

If an incident needs to be transferred to another Technician:

1. Open the incident.
2. Locate the assignment controls.
3. Select the replacement Technician.
4. Submit the reassignment.
5. Confirm that the new Technician is displayed.

The system records the reassignment and retains the relevant assignment history.

### 5.6 Creating a User Account

Public self-registration is disabled. New application accounts are created by an Administrator.

1. Log in as an Administrator.
2. Open User Management.
3. Select the option to create a user.
4. Enter the user's full name.
5. Enter a valid email address.
6. Select the appropriate role.
7. Enter a password.
8. Confirm the password.
9. Submit the form.

The system validates the information before creating the account.

The password must:

- Contain at least eight characters.
- Include at least one letter.
- Include at least one digit.

The email address must be unique. The password is stored as a secure hash rather than plaintext.

### 5.7 Searching for Users

1. Open User Management.
2. Enter a name or email search term.
3. Apply any available role or account-status filters.
4. Review the matching accounts.

The user list provides information to help Administrators identify the correct account.

### 5.8 Changing a User's Role

1. Open User Management.
2. Locate the relevant account.
3. Select the role-management option.
4. Choose the appropriate role.
5. Submit the change.

The available roles are:

- User
- Technician
- Administrator
- Supervisor

Role changes affect the functionality available to the account.

The application prevents Administrators from changing their own role through this workflow.

### 5.9 Activating and Deactivating Accounts

Administrators can manage whether an account is active.

To change an account's status:

1. Open User Management.
2. Locate the relevant account.
3. Select the account-status action.
4. Confirm the operation where required.
5. Verify the updated account status.

Important restrictions apply:

- Administrators cannot deactivate their own account through this workflow.
- The last active Administrator cannot be deactivated.
- A Technician with outstanding non-Closed incidents must have those incidents reassigned before deactivation.

Account status changes are recorded in the audit history.

### 5.10 Accessing Reports

Administrators can access the reporting functionality.

1. Open the Reports page.
2. Review the available incident statistics.
3. Apply date filters where required.
4. Review the displayed report information.
5. Use the available export options to generate CSV or PDF reports.

Reports provide information such as total incidents, incident statuses and resolution outcomes.

---

## 6. Supervisor Guide

### 6.1 Supervisor Dashboard

The Supervisor dashboard provides organisation-wide oversight of incident activity.

Supervisors can:

- View incidents across the system.
- Monitor incident statuses.
- Review incident details.
- Access reporting and analytics.
- Export reports.

The Supervisor role is intended for oversight rather than operational administration.

### 6.2 Viewing Incidents

1. Log in using a Supervisor account.
2. Open the Supervisor dashboard.
3. Review the available incident information.
4. Open an incident to inspect its details.

Supervisors have read-only oversight access. They do not assign Technicians, manage user accounts or directly change incident statuses through the normal workflow.

### 6.3 Using Reporting and Analytics

1. Open the Reports page.
2. Review the summary statistics.
3. Examine incident totals and status groupings.
4. Review incidents awaiting User confirmation.
5. Review accepted and rejected resolution counts.
6. Apply date filters if required.
7. Export a CSV or PDF report if needed.

Reports help Supervisors monitor the incident workload and the outcome of proposed resolutions.

---

## 7. Understanding Incident Statuses

The following table explains the incident statuses used by SupportDesk Pro.

| Status | Explanation | Typical Next Step |
|---|---|---|
| Open | The incident has been registered. | Assignment and investigation. |
| In Progress | A Technician is actively investigating the incident. | Record troubleshooting and submit a resolution. |
| Awaiting User Confirmation | A proposed resolution has been submitted. | Reporting User accepts or rejects it. |
| Reopened | The User rejected the proposed resolution. | Further investigation by the support team. |
| Closed | The User accepted the proposed resolution. | No further normal workflow action. |

An incident must not be treated as resolved and closed until the reporting User accepts the proposed resolution.

---

## 8. Common Problems and Troubleshooting

### 8.1 Unable to Log In

Possible causes:

- Incorrect email address.
- Incorrect password.
- Account is inactive.
- Application cannot connect to the database.

Recommended actions:

1. Check the email address.
2. Check the password.
3. Confirm that the account is active with an Administrator.
4. Confirm that the application is running.
5. If the issue continues, contact the person responsible for the local application.

### 8.2 Application Page Does Not Load

Possible causes:

- Flask application is not running.
- The browser is using the wrong local address.
- The application encountered an unexpected error.

Recommended actions:

1. Check the PowerShell window where the application was started.
2. Confirm that Flask is still running.
3. Open the local address shown in the terminal.
4. If an error appears, check the application logs.

### 8.3 Database Connection Error

Possible causes:

- SQL Server Express is stopped.
- Database connection settings are incorrect.
- The database does not exist.
- The required ODBC driver is unavailable.

Recommended actions:

1. Confirm that SQL Server Express is running.
2. Confirm that `SupportDeskProDB` exists.
3. Check the database settings in the local environment configuration.
4. Confirm that the required ODBC Driver 18 for SQL Server is installed.
5. Restart the application after correcting the issue.

Do not share the `.env` file or disclose its secret values when requesting support.

### 8.4 Unable to Claim an Incident

Possible causes:

- Another Technician has already claimed the incident.
- The incident is Closed.
- The account does not have the Technician role.
- The claim request failed.

Recommended actions:

1. Refresh the Technician incident queue.
2. Check whether the incident is still unassigned.
3. Confirm that the account is active and has the Technician role.
4. Try again only if the incident remains eligible.

### 8.5 Unable to Submit a Resolution

Possible causes:

- The incident is not assigned to the current Technician.
- The incident is not in an eligible status.
- No troubleshooting activity has been recorded.
- The submitted resolution is invalid.

Recommended actions:

1. Confirm that the incident is assigned to your account.
2. Confirm that the incident is In Progress or Reopened as appropriate.
3. Record at least one troubleshooting action.
4. Enter a valid proposed resolution.
5. Submit again.

### 8.6 Resolution Review Link Does Not Work

Possible causes:

- The link has expired.
- The token is invalid.
- The resolution has already received a decision.
- The incident is no longer awaiting confirmation.

Recommended actions:

1. Confirm that the link is the latest notification.
2. Contact the support Technician if the link has expired.
3. Ask the assigned Technician to resend the pending resolution notification where the resolution remains eligible.

### 8.7 Unable to Reject a Resolution

A rejection requires a reason.

Recommended actions:

1. Return to the resolution review page.
2. Select Reject.
3. Enter a clear explanation of why the issue remains unresolved.
4. Submit the decision.

### 8.8 Access Denied

An access-denied response usually means that the signed-in account does not have permission to access the requested page or operation.

Recommended actions:

1. Confirm which account is signed in.
2. Confirm that the account has the required role.
3. Contact an Administrator if access is required for the user's responsibilities.

---

## 9. Security and Responsible Use

Users must follow these guidelines:

- Keep account passwords confidential.
- Do not share resolution review links with other people.
- Log out after completing work.
- Use only authorised application accounts.
- Do not enter real confidential banking or customer information.
- Use synthetic or authorised test information for academic demonstrations.
- Do not attempt to access another user's incidents or restricted functions.
- Report unexpected errors or suspicious application behaviour.

The application records important activities for accountability and testing.

---

## 10. Support and Maintenance

SupportDesk Pro is a local academic project.

The application must be started on the computer where the project and its database are configured. If the application is stopped, users will not be able to access it until it is started again.

For application problems, the person maintaining the project should:

1. Check that the Python virtual environment is active.
2. Check that the SQL Server Express instance is running.
3. Check the application terminal for errors.
4. Review relevant application logs.
5. Run the automated tests after making code changes.

The automated test suite can be executed from the project directory using:

```powershell
python -m pytest -q
```

The Python source can be checked for syntax errors using:

```powershell
python -m compileall app
```

---

## 11. Conclusion

This User Manual provides instructions for using SupportDesk Pro according to the permissions of each application role.

It explains the complete incident workflow, from initial reporting through investigation and troubleshooting to User acceptance or rejection.

The User confirmation process ensures that an incident is only marked Closed after the reporting User has accepted the proposed resolution.

**End of User Manual**
