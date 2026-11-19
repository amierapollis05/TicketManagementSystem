from app.repositories.user_repository import UserRepository
from app.security.passwords import hash_password


class UserManagementService:
    """Handles administrator user-management operations."""

    ALLOWED_ROLES = {
        "User",
        "Technician",
        "Supervisor",
        "Administrator",
    }

    @staticmethod
    def create_user(full_name, email, password, confirm_password, role, administrator_id):
        """Validate and create an account on behalf of an Administrator."""

        if not isinstance(full_name, str) or not full_name.strip():
            raise ValueError("Full name is required.")

        full_name = full_name.strip()
        if len(full_name) > 100:
            raise ValueError("Full name must not exceed 100 characters.")

        if not isinstance(email, str) or not email.strip():
            raise ValueError("Email address is required.")

        email = email.strip().lower()
        if len(email) > 254 or "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            raise ValueError("Enter a valid email address.")

        if role not in UserManagementService.ALLOWED_ROLES:
            raise ValueError("Select a valid account role.")

        if not isinstance(password, str) or len(password) < 8:
            raise ValueError("Password must contain at least 8 characters.")

        if not any(character.isalpha() for character in password):
            raise ValueError("Password must contain at least one letter.")

        if not any(character.isdigit() for character in password):
            raise ValueError("Password must contain at least one number.")

        if password != confirm_password:
            raise ValueError("The passwords do not match.")

        if UserRepository.get_by_email(email) is not None:
            raise ValueError("An account with this email address already exists.")

        password_hash = hash_password(password)

        return UserRepository.create_managed_user(
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=role,
            created_by_user_id=administrator_id,
        )

    @staticmethod
    def get_users(search_term=None, role=None, status=None):
        """Retrieve users using validated filters."""

        if role and role not in UserManagementService.ALLOWED_ROLES:
            raise ValueError("Invalid user role filter.")

        if status and status not in {"Active", "Inactive"}:
            raise ValueError("Invalid account status filter.")

        search_term = (search_term or "").strip()

        return UserRepository.get_all_users(
            search_term=search_term or None,
            role=role or None,
            status=status or None,
        )

    @staticmethod
    def change_role(
        target_user_id: int,
        new_role: str,
        administrator_id: int,
    ):
        """Validate and change a user's role."""

        if new_role not in UserManagementService.ALLOWED_ROLES:
            raise ValueError("The selected role is invalid.")

        if target_user_id == administrator_id:
            raise ValueError("You cannot change your own account role.")

        UserRepository.update_user_role(
            user_id=target_user_id,
            new_role=new_role,
            changed_by_user_id=administrator_id,
        )

    @staticmethod
    def change_account_status(
        target_user_id: int,
        is_active: bool,
        administrator_id: int,
    ):
        """Validate and change a user's account status."""

        if target_user_id == administrator_id:
            raise ValueError("You cannot deactivate or change your own account status.")

        if not isinstance(is_active, bool):
            raise ValueError("Invalid account status.")

        UserRepository.update_user_status(
            user_id=target_user_id,
            is_active=is_active,
            changed_by_user_id=administrator_id,
        )
