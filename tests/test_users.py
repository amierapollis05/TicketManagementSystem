import pytest
from unittest.mock import patch

from app.security.passwords import hash_password, verify_password
from app.services.auth_service import AuthService
from app.services.user_management_service import UserManagementService

# ==================================================
# PASSWORD SECURITY
# ==================================================


def test_password_is_stored_as_hash_not_plain_text():
    password = "SecurePass123"

    password_hash = hash_password(password)

    assert password_hash != password
    assert password_hash.startswith("scrypt:")


def test_password_hash_verifies_correct_password():
    password_hash = hash_password("SecurePass123")

    assert verify_password("SecurePass123", password_hash) is True


def test_password_hash_rejects_incorrect_password():
    password_hash = hash_password("SecurePass123")

    assert verify_password("WrongPass123", password_hash) is False


@pytest.mark.parametrize("password", ["", "   ", None, 123])
def test_hash_password_rejects_empty_or_invalid_password(password):
    with pytest.raises(ValueError, match="Password cannot be empty"):
        hash_password(password)


@pytest.mark.parametrize(
    "password,password_hash",
    [
        (None, "somehash"),
        ("password", None),
        ("", "somehash"),
        ("password", ""),
        ("password", "invalid-hash"),
    ],
)
def test_verify_password_handles_invalid_input(password, password_hash):
    assert verify_password(password, password_hash) is False


# ==================================================
# USER ACCOUNT CREATION
# ==================================================

VALID_ACCOUNT = {
    "full_name": "Test User",
    "email": "test@example.com",
    "password": "SecurePass123",
    "confirm_password": "SecurePass123",
    "role": "User",
    "administrator_id": 1,
}


@pytest.mark.parametrize("full_name", ["", "   ", None, 123])
def test_create_user_rejects_invalid_full_name(full_name):
    data = VALID_ACCOUNT.copy()
    data["full_name"] = full_name

    with pytest.raises(ValueError, match="Full name is required"):
        UserManagementService.create_user(**data)


def test_create_user_rejects_name_over_100_characters():
    data = VALID_ACCOUNT.copy()
    data["full_name"] = "A" * 101

    with pytest.raises(ValueError, match="100 characters"):
        UserManagementService.create_user(**data)


@pytest.mark.parametrize("email", ["", "   ", None, 123])
def test_create_user_rejects_missing_email(email):
    data = VALID_ACCOUNT.copy()
    data["email"] = email

    with pytest.raises(ValueError, match="Email address is required"):
        UserManagementService.create_user(**data)


@pytest.mark.parametrize(
    "email",
    [
        "not-an-email",
        "user@",
        "user@example",
        "user@example.",
        "A" * 250 + "@example.com",
    ],
)
def test_create_user_rejects_invalid_email(email):
    data = VALID_ACCOUNT.copy()
    data["email"] = email

    with pytest.raises(ValueError, match="valid email address"):
        UserManagementService.create_user(**data)


@pytest.mark.parametrize(
    "role",
    ["Invalid", "Manager", "Guest", "", None],
)
def test_create_user_rejects_invalid_role(role):
    data = VALID_ACCOUNT.copy()
    data["role"] = role

    with pytest.raises(ValueError, match="valid account role"):
        UserManagementService.create_user(**data)


@pytest.mark.parametrize(
    "role",
    ["User", "Technician", "Supervisor", "Administrator"],
)
def test_create_user_accepts_all_supported_roles(role):
    data = VALID_ACCOUNT.copy()
    data["role"] = role

    with patch(
        "app.services.user_management_service.UserRepository.get_by_email",
        return_value=None,
    ), patch(
        "app.services.user_management_service.UserRepository.create_managed_user",
        return_value=10,
    ):
        result = UserManagementService.create_user(**data)

    assert result == 10


@pytest.mark.parametrize(
    "password",
    ["Short1", "1234567", "Password", ""],
)
def test_create_user_rejects_password_without_required_length_or_characters(password):
    data = VALID_ACCOUNT.copy()
    data["password"] = password
    data["confirm_password"] = password

    with pytest.raises(ValueError):
        UserManagementService.create_user(**data)


def test_create_user_rejects_password_without_letter():
    data = VALID_ACCOUNT.copy()
    data["password"] = "12345678"
    data["confirm_password"] = "12345678"

    with pytest.raises(ValueError, match="at least one letter"):
        UserManagementService.create_user(**data)


def test_create_user_rejects_password_without_number():
    data = VALID_ACCOUNT.copy()
    data["password"] = "PasswordOnly"
    data["confirm_password"] = "PasswordOnly"

    with pytest.raises(ValueError, match="at least one number"):
        UserManagementService.create_user(**data)


def test_create_user_rejects_password_confirmation_mismatch():
    data = VALID_ACCOUNT.copy()
    data["confirm_password"] = "DifferentPass123"

    with pytest.raises(ValueError, match="passwords do not match"):
        UserManagementService.create_user(**data)


def test_create_user_rejects_duplicate_email():
    data = VALID_ACCOUNT.copy()

    with patch(
        "app.services.user_management_service.UserRepository.get_by_email",
        return_value={"user_id": 5},
    ):
        with pytest.raises(ValueError, match="already exists"):
            UserManagementService.create_user(**data)


def test_create_user_normalises_input_and_hashes_password():
    data = VALID_ACCOUNT.copy()
    data["full_name"] = "  Test User  "
    data["email"] = "  TEST@EXAMPLE.COM  "

    with patch(
        "app.services.user_management_service.UserRepository.get_by_email",
        return_value=None,
    ), patch(
        "app.services.user_management_service.UserRepository.create_managed_user",
        return_value=25,
    ) as create_mock:

        result = UserManagementService.create_user(**data)

    assert result == 25

    saved_data = create_mock.call_args.kwargs

    assert saved_data["full_name"] == "Test User"
    assert saved_data["email"] == "test@example.com"
    assert saved_data["password_hash"] != data["password"]
    assert saved_data["password_hash"].startswith("scrypt:")
    assert saved_data["role"] == "User"
    assert saved_data["created_by_user_id"] == 1


# ==================================================
# USER SEARCH AND FILTER VALIDATION
# ==================================================


def test_get_users_rejects_invalid_role_filter():
    with pytest.raises(ValueError, match="Invalid user role"):
        UserManagementService.get_users(role="Invalid")


def test_get_users_rejects_invalid_status_filter():
    with pytest.raises(ValueError, match="Invalid account status"):
        UserManagementService.get_users(status="Pending")


def test_get_users_accepts_valid_filters():
    with patch(
        "app.services.user_management_service.UserRepository.get_all_users",
        return_value=[],
    ) as repository_mock:

        result = UserManagementService.get_users(
            search_term="  Test User  ",
            role="Technician",
            status="Active",
        )

    assert result == []

    repository_mock.assert_called_once_with(
        search_term="Test User",
        role="Technician",
        status="Active",
    )


# ==================================================
# ROLE MANAGEMENT
# ==================================================


def test_change_role_rejects_invalid_role():
    with pytest.raises(ValueError, match="selected role is invalid"):
        UserManagementService.change_role(2, "Invalid", 1)


def test_change_role_prevents_administrator_changing_own_role():
    with pytest.raises(ValueError, match="own account role"):
        UserManagementService.change_role(1, "User", 1)


def test_change_role_calls_repository_for_valid_change():
    with patch(
        "app.services.user_management_service.UserRepository.update_user_role"
    ) as repository_mock:

        UserManagementService.change_role(2, "Technician", 1)

    repository_mock.assert_called_once_with(
        user_id=2,
        new_role="Technician",
        changed_by_user_id=1,
    )


# ==================================================
# ACCOUNT STATUS MANAGEMENT
# ==================================================


def test_change_status_prevents_administrator_changing_own_status():
    with pytest.raises(ValueError, match="own account status"):
        UserManagementService.change_account_status(1, False, 1)


@pytest.mark.parametrize("status", ["Active", "Inactive", 1, 0, None])
def test_change_status_rejects_non_boolean_status(status):
    with pytest.raises(ValueError, match="Invalid account status"):
        UserManagementService.change_account_status(2, status, 1)


@pytest.mark.parametrize("status", [True, False])
def test_change_status_calls_repository_for_valid_change(status):
    with patch(
        "app.services.user_management_service.UserRepository.update_user_status"
    ) as repository_mock:

        UserManagementService.change_account_status(2, status, 1)

    repository_mock.assert_called_once_with(
        user_id=2,
        is_active=status,
        changed_by_user_id=1,
    )


# ==================================================
# AUTHENTICATION
# ==================================================


def make_test_user():
    return {
        "user_id": 5,
        "full_name": "Test User",
        "email": "test@example.com",
        "role": "User",
        "password_hash": "stored-hash",
        "is_active": True,
    }


def test_authentication_normalises_email():
    user = make_test_user()

    with patch(
        "app.services.auth_service.UserRepository.get_by_email",
        return_value=user,
    ) as get_user_mock, patch(
        "app.services.auth_service.verify_password",
        return_value=True,
    ), patch(
        "app.services.auth_service.UserRepository.record_login_attempt"
    ):

        AuthService.authenticate_user("  TEST@EXAMPLE.COM  ", "SecurePass123")

    get_user_mock.assert_called_once_with("test@example.com")


def test_authentication_returns_user_without_password_hash():
    user = make_test_user()

    with patch(
        "app.services.auth_service.UserRepository.get_by_email",
        return_value=user,
    ), patch(
        "app.services.auth_service.verify_password",
        return_value=True,
    ), patch(
        "app.services.auth_service.UserRepository.record_login_attempt"
    ):

        result = AuthService.authenticate_user("test@example.com", "SecurePass123")

    assert result == {
        "user_id": 5,
        "full_name": "Test User",
        "email": "test@example.com",
        "role": "User",
    }

    assert "password_hash" not in result


def test_authentication_rejects_unknown_email_and_records_failure():
    with patch(
        "app.services.auth_service.UserRepository.get_by_email",
        return_value=None,
    ), patch(
        "app.services.auth_service.UserRepository.record_login_attempt"
    ) as audit_mock:

        result = AuthService.authenticate_user("unknown@example.com", "SecurePass123")

    assert result is None

    audit_mock.assert_called_once_with(
        user_id=None,
        email="unknown@example.com",
        successful=False,
    )


def test_authentication_rejects_inactive_account_and_records_failure():
    user = make_test_user()
    user["is_active"] = False

    with patch(
        "app.services.auth_service.UserRepository.get_by_email",
        return_value=user,
    ), patch("app.services.auth_service.verify_password") as verify_mock, patch(
        "app.services.auth_service.UserRepository.record_login_attempt"
    ) as audit_mock:

        result = AuthService.authenticate_user("test@example.com", "SecurePass123")

    assert result is None
    verify_mock.assert_not_called()

    audit_mock.assert_called_once_with(
        user_id=5,
        email="test@example.com",
        successful=False,
    )


def test_authentication_rejects_incorrect_password_and_records_failure():
    user = make_test_user()

    with patch(
        "app.services.auth_service.UserRepository.get_by_email",
        return_value=user,
    ), patch(
        "app.services.auth_service.verify_password",
        return_value=False,
    ), patch(
        "app.services.auth_service.UserRepository.record_login_attempt"
    ) as audit_mock:

        result = AuthService.authenticate_user("test@example.com", "WrongPass123")

    assert result is None

    audit_mock.assert_called_once_with(
        user_id=5,
        email="test@example.com",
        successful=False,
    )


def test_authentication_records_successful_login():
    user = make_test_user()

    with patch(
        "app.services.auth_service.UserRepository.get_by_email",
        return_value=user,
    ), patch(
        "app.services.auth_service.verify_password",
        return_value=True,
    ), patch(
        "app.services.auth_service.UserRepository.record_login_attempt"
    ) as audit_mock:

        result = AuthService.authenticate_user("test@example.com", "SecurePass123")

    assert result is not None

    audit_mock.assert_called_once_with(
        user_id=5,
        email="test@example.com",
        successful=True,
    )


def test_authentication_rejects_missing_credentials_and_records_failure():
    with patch(
        "app.services.auth_service.UserRepository.record_login_attempt"
    ) as audit_mock:

        result = AuthService.authenticate_user("", "")

    assert result is None

    audit_mock.assert_called_once_with(
        user_id=None,
        email="",
        successful=False,
    )
