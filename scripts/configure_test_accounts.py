import sys
from pathlib import Path
from getpass import getpass

# Add the project root to Python's module search path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.db.connection import get_connection
from app.security.passwords import hash_password

TEST_ACCOUNTS = [
    {"email": "user@supportdesk.local", "role": "User"},
    {"email": "technician@supportdesk.local", "role": "Technician"},
    {"email": "admin@supportdesk.local", "role": "Administrator"},
    {"email": "supervisor@supportdesk.local", "role": "Supervisor"},
]


def configure_test_accounts():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        for account in TEST_ACCOUNTS:
            email = account["email"]
            expected_role = account["role"]

            cursor.execute(
                """
                SELECT Role, PasswordHash
                FROM dbo.Users
                WHERE Email = ?
            """,
                (email,),
            )

            user = cursor.fetchone()

            if user is None:
                print(f"Account not found: {email}")
                raise ValueError("A required test account is missing.")

            if user.Role != expected_role:
                raise ValueError(f"Unexpected role for {email}.")

            if user.PasswordHash != "TEMPORARY_HASH":
                print(f"Already configured: {email}")
                continue

            print(f"\nConfigure password for: {email}")

            password = getpass("Enter test password: ")
            confirmation = getpass("Confirm test password: ")

            if len(password) < 8:
                raise ValueError("Password must contain at least 8 characters.")

            if password != confirmation:
                raise ValueError("Passwords do not match.")

            password_hash = hash_password(password)

            cursor.execute(
                """
                UPDATE dbo.Users
                SET PasswordHash = ?
                WHERE Email = ?
                  AND PasswordHash = 'TEMPORARY_HASH'
            """,
                (password_hash, email),
            )

            if cursor.rowcount != 1:
                raise RuntimeError(f"Could not update account: {email}")

            print(f"Password configured successfully: {email}")

        connection.commit()
        print("\nAll test accounts have been processed.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    configure_test_accounts()
