from functools import wraps
from flask import abort, redirect, url_for

from app.security.session_user import get_current_user


def login_required(view_function):
    """Require an authenticated user."""

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        current_user = get_current_user()

        if current_user is None:
            return redirect(url_for("auth.login"))

        return view_function(*args, **kwargs)

    return wrapped_view


def roles_required(*allowed_roles):
    """Restrict access to specified user roles."""

    def decorator(view_function):

        @wraps(view_function)
        def wrapped_view(*args, **kwargs):
            current_user = get_current_user()

            if current_user is None:
                return redirect(url_for("auth.login"))

            if current_user["role"] not in allowed_roles:
                abort(403)

            return view_function(*args, **kwargs)

        return wrapped_view

    return decorator
