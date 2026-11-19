from app.repositories.user_repository import UserRepository
from app.security.passwords import verify_password


class AuthService:
    """Handles user authentication."""

    @staticmethod
    def authenticate_user(email: str, password: str):
        """Authenticate a user and record the login attempt."""

        email = email.strip().lower() if isinstance(email, str) else ""

        if not email or not isinstance(password, str) or not password:
            UserRepository.record_login_attempt(
                user_id=None,
                email=email,
                successful=False,
            )
            return None

        user = UserRepository.get_by_email(email)

        if user is None or not user["is_active"]:
            UserRepository.record_login_attempt(
                user_id=user["user_id"] if user else None,
                email=email,
                successful=False,
            )
            return None

        if not verify_password(password, user["password_hash"]):
            UserRepository.record_login_attempt(
                user_id=user["user_id"],
                email=email,
                successful=False,
            )
            return None

        UserRepository.record_login_attempt(
            user_id=user["user_id"],
            email=email,
            successful=True,
        )

        # Never expose the password hash to the session or routes.
        return {
            "user_id": user["user_id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "role": user["role"],
        }
