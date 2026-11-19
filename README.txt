SUPPORTDESK PRO - ACCOUNT MANAGEMENT PATCH

This patch aligns account creation with the approved DDS decision:
- Public self-registration is disabled.
- Only an Administrator can create an account.
- The Administrator selects User, Technician, Supervisor or Administrator.
- Initial passwords must be at least 8 characters and contain a letter and a digit.
- Passwords are hashed before storage.
- Account creation and its audit entry are saved in one SQL transaction.

INSTALLATION
1. Make a backup of your current project folder.
2. Extract this ZIP into the ROOT of your existing TicketManagementSystem folder.
3. Allow the extracted files to overwrite the existing files.
4. Delete app/templates/auth/register.html from your project (the old public registration page is no longer used).
5. Activate your existing virtual environment and run:

   python -m compileall app
   python -m pytest -q

6. Start the application:

   python run.py

7. Sign in with an Administrator account and open User Management.
8. Create a test account with a unique email address and a password containing at least one letter and one digit, with at least 8 characters.
9. Verify the account appears in the user list and that an AuditLogs row with Action = 'User Account Created' exists.
10. Sign out and test that the new account can sign in with the selected role.

IMPORTANT
- This patch does not modify the SQL schema.
- The new account is active by default.
- The administrator should communicate the initial password to the account holder securely and outside the application. No email notification is added because email notifications are excluded from the approved project scope.
- Test in your local development database first.
