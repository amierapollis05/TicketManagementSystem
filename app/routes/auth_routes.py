from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.auth_service import AuthService
from app.security.session_user import login_user, logout_user, get_current_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Public self-registration is disabled; administrators create accounts."""

    flash(
        "Public registration is disabled. Please contact the system administrator "
        "to request an account.",
        "info",
    )
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if get_current_user() is not None:
        return redirect(url_for("main.home"))

    if request.method == "POST":

        email = request.form.get("email", "")
        password = request.form.get("password", "")

        user = AuthService.authenticate_user(email, password)

        if user is None:
            flash("Invalid email address or password.", "error")
            return render_template("auth/login.html")

        login_user(user)

        flash(f"Welcome back, {user['full_name']}!", "success")

        return redirect(url_for("main.home"))

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():

    if get_current_user() is not None:
        logout_user()
        flash("You have been logged out successfully.", "success")

    return redirect(url_for("auth.login"))
