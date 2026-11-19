from app.repositories.user_repository import UserRepository
from app.security.passwords import verify_password


class AuthService:
    """Handles user authentication."""

    @staticmethod
    def authenticate_user(email: str, password: str):
        """Authenticate a user using their email and password."""

        if not isinstance(email, str) or not email.strip():
            return None

        if not isinstance(password, str) or not password:
            return None

        email = email.strip().lower()
        user = UserRepository.get_by_email(email)

        if user is None or not user["is_active"]:
            return None

        if not verify_password(password, user["password_hash"]):
            return None

        # Never expose the password hash to the session or routes.
        return {
            "user_id": user["user_id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "role": user["role"],
        }
