from app.db.connection import get_connection


class UserRepository:
    """Handles database operations for users."""

    @staticmethod
    def get_by_email(email: str):
        """Retrieve a user by their email address."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    UserId,
                    FullName,
                    Email,
                    PasswordHash,
                    Role,
                    IsActive
                FROM dbo.Users
                WHERE Email = ?
                """,
                (email,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "user_id": row.UserId,
                "full_name": row.FullName,
                "email": row.Email,
                "password_hash": row.PasswordHash,
                "role": row.Role,
                "is_active": row.IsActive,
            }

        finally:
            connection.close()

    @staticmethod
    def get_by_id(user_id: int):
        """Retrieve a user by their ID."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    UserId,
                    FullName,
                    Email,
                    PasswordHash,
                    Role,
                    IsActive
                FROM dbo.Users
                WHERE UserId = ?
                """,
                (user_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "user_id": row.UserId,
                "full_name": row.FullName,
                "email": row.Email,
                "password_hash": row.PasswordHash,
                "role": row.Role,
                "is_active": row.IsActive,
            }

        finally:
            connection.close()

    @staticmethod
    def get_active_technicians():
        """Retrieve all active technician accounts."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    UserId,
                    FullName,
                    Email
                FROM dbo.Users
                WHERE Role = 'Technician'
                  AND IsActive = 1
                ORDER BY FullName
                """)

            rows = cursor.fetchall()

            return [
                {
                    "user_id": row.UserId,
                    "full_name": row.FullName,
                    "email": row.Email,
                }
                for row in rows
            ]

        finally:
            connection.close()

    @staticmethod
    def get_all_users(search_term=None, role=None, status=None):
        """Retrieve users with optional search and filters."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            query = """
                SELECT
                    UserId,
                    FullName,
                    Email,
                    Role,
                    IsActive
                FROM dbo.Users
                WHERE 1 = 1
            """

            parameters = []

            if search_term:
                query += """
                    AND (
                        FullName LIKE ?
                        OR Email LIKE ?
                    )
                """

                search_pattern = f"%{search_term}%"
                parameters.extend([search_pattern, search_pattern])

            if role:
                query += " AND Role = ?"
                parameters.append(role)

            if status == "Active":
                query += " AND IsActive = 1"

            elif status == "Inactive":
                query += " AND IsActive = 0"

            query += " ORDER BY FullName ASC"

            cursor.execute(query, parameters)

            rows = cursor.fetchall()

            return [
                {
                    "user_id": row.UserId,
                    "full_name": row.FullName,
                    "email": row.Email,
                    "role": row.Role,
                    "is_active": row.IsActive,
                }
                for row in rows
            ]

        finally:
            connection.close()

    @staticmethod
    def update_user_role(user_id: int, new_role: str, changed_by_user_id: int):
        """Change a user's role and record the change."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT Role, IsActive
                FROM dbo.Users WITH (UPDLOCK, ROWLOCK)
                WHERE UserId = ?
                """,
                (user_id,),
            )

            user = cursor.fetchone()

            if user is None:
                raise ValueError("The selected user does not exist.")

            old_role = user.Role

            if old_role == new_role:
                raise ValueError("The user already has this role.")

            if old_role == "Administrator" and user.IsActive:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM dbo.Users
                    WHERE Role = 'Administrator'
                      AND IsActive = 1
                    """)

                active_admin_count = cursor.fetchone()[0]

                if active_admin_count <= 1:
                    raise ValueError(
                        "You cannot remove the role of the last active Administrator."
                    )

            cursor.execute(
                """
                UPDATE dbo.Users
                SET Role = ?
                WHERE UserId = ?
                """,
                (new_role, user_id),
            )

            cursor.execute(
                """
                INSERT INTO dbo.AuditLogs (
                    IncidentId,
                    UserId,
                    Action,
                    FromStatus,
                    ToStatus,
                    Details
                )
                VALUES (
                    NULL,
                    ?,
                    'User Role Changed',
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    changed_by_user_id,
                    old_role,
                    new_role,
                    f"Administrator changed the role of UserId {user_id}.",
                ),
            )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def update_user_status(user_id: int, is_active: bool, changed_by_user_id: int):
        """Activate or deactivate an account and record the change."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT Role, IsActive
                FROM dbo.Users WITH (UPDLOCK, ROWLOCK)
                WHERE UserId = ?
                """,
                (user_id,),
            )

            user = cursor.fetchone()

            if user is None:
                raise ValueError("The selected user does not exist.")

            old_status = bool(user.IsActive)

            if old_status == is_active:
                raise ValueError("The account already has this status.")

            if user.Role == "Administrator" and old_status and not is_active:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM dbo.Users
                    WHERE Role = 'Administrator'
                      AND IsActive = 1
                    """)

                active_admin_count = cursor.fetchone()[0]

                if active_admin_count <= 1:
                    raise ValueError(
                        "You cannot deactivate the last active Administrator."
                    )

            new_status = "Active" if is_active else "Inactive"
            previous_status = "Active" if old_status else "Inactive"

            cursor.execute(
                """
                UPDATE dbo.Users
                SET IsActive = ?
                WHERE UserId = ?
                """,
                (is_active, user_id),
            )

            action = (
                "User Account Activated" if is_active else "User Account Deactivated"
            )

            cursor.execute(
                """
                INSERT INTO dbo.AuditLogs (
                    IncidentId,
                    UserId,
                    Action,
                    FromStatus,
                    ToStatus,
                    Details
                )
                VALUES (
                    NULL,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    changed_by_user_id,
                    action,
                    previous_status,
                    new_status,
                    f"Administrator changed the account status of UserId {user_id}.",
                ),
            )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def create_managed_user(
        full_name: str,
        email: str,
        password_hash: str,
        role: str,
        created_by_user_id: int,
    ):
        """Create an active account and audit the action in one transaction."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO dbo.Users (
                    FullName,
                    Email,
                    PasswordHash,
                    Role,
                    IsActive
                )
                OUTPUT INSERTED.UserId
                VALUES (?, ?, ?, ?, 1)
                """,
                (full_name, email, password_hash, role),
            )

            new_user_id = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO dbo.AuditLogs (
                    IncidentId,
                    UserId,
                    Action,
                    FromStatus,
                    ToStatus,
                    Details
                )
                VALUES (NULL, ?, 'User Account Created', NULL, ?, ?)
                """,
                (
                    created_by_user_id,
                    role,
                    f"Administrator created UserId {new_user_id}.",
                ),
            )

            connection.commit()
            return new_user_id

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()
