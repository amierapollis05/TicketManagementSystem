from flask import g, session

from app.repositories.user_repository import UserRepository


def login_user(user: dict) -> None:
    """
    Start an authenticated session for a user.

    Only the user's ID is stored in the session.
    """

    session.clear()
    session.permanent = True
    session["user_id"] = user["user_id"]


def logout_user() -> None:
    """End the current user's session."""

    session.clear()
    g.pop("_current_user", None)


def get_current_user():
    """
    Retrieve the currently authenticated user.

    User details are loaded from SQL Server rather than
    trusting role information stored in the browser session.
    """

    if hasattr(g, "_current_user"):
        return g._current_user

    user_id = session.get("user_id")

    if user_id is None:
        g._current_user = None
        return None

    user = UserRepository.get_by_id(user_id)

    if user is None or not user["is_active"]:
        session.clear()
        g._current_user = None
        return None

    # Never expose the password hash to application routes.
    g._current_user = {
        "user_id": user["user_id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "role": user["role"],
    }

    return g._current_user
