import logging

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    url_for,
    request,
)

from app.security.decorators import roles_required
from app.security.session_user import get_current_user
from app.services.incident_service import IncidentService
from app.services.user_management_service import UserManagementService

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/incidents")
@roles_required("Administrator")
def incidents():
    """Display and filter all incidents for administrative management."""

    search_term = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()
    priority = request.args.get("priority", "").strip()
    category_value = request.args.get("category_id", "").strip()

    try:
        category_id = int(category_value) if category_value else None

        all_incidents = IncidentService.search_all_incidents(
            search_term=search_term,
            status=status,
            priority=priority,
            category_id=category_id,
        )

    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("admin.incidents"))

    technicians = IncidentService.get_active_technicians()
    categories = IncidentService.get_categories()

    return render_template(
        "admin/incidents.html",
        incidents=all_incidents,
        technicians=technicians,
        categories=categories,
        search_term=search_term,
        selected_status=status,
        selected_priority=priority,
        selected_category_id=category_id,
    )


@admin_bp.route("/incidents/<int:incident_id>/assign", methods=["POST"])
@roles_required("Administrator")
def assign_technician(incident_id):
    """Assign a technician to an incident."""

    current_user = get_current_user()

    try:
        technician_id = int(request.form.get("technician_id", ""))

        result = IncidentService.assign_technician(
            incident_id=incident_id,
            technician_id=technician_id,
            assigned_by_user_id=current_user["user_id"],
        )

        flash(
            f"{result['technician_name']} was successfully assigned "
            f"to the incident.",
            "success",
        )

    except ValueError as error:
        flash(str(error), "error")

    except Exception:
        current_app.logger.exception(
            "Failed to assign technician to incident %s.",
            incident_id,
        )

        flash(
            "An unexpected error occurred while assigning the technician.",
            "error",
        )

    return redirect(url_for("admin.incidents"))


@admin_bp.route("/users")
@roles_required("Administrator")
def users():
    """Display and filter registered user accounts."""

    search_term = request.args.get("search", "").strip()
    role = request.args.get("role", "").strip()
    status = request.args.get("status", "").strip()

    try:
        all_users = UserManagementService.get_users(
            search_term=search_term,
            role=role,
            status=status,
        )

    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("admin.users"))

    return render_template(
        "admin/users.html",
        users=all_users,
        search_term=search_term,
        selected_role=role,
        selected_status=status,
        current_user=get_current_user(),
    )


@admin_bp.route("/users/create", methods=["POST"])
@roles_required("Administrator")
def create_user():
    """Create a new authorised account."""

    current_user = get_current_user()

    try:
        UserManagementService.create_user(
            full_name=request.form.get("full_name", ""),
            email=request.form.get("email", ""),
            password=request.form.get("password", ""),
            confirm_password=request.form.get("confirm_password", ""),
            role=request.form.get("role", ""),
            administrator_id=current_user["user_id"],
        )

        flash("User account successfully created.", "success")

    except ValueError as error:
        flash(str(error), "error")

    except Exception:
        current_app.logger.exception("Failed to create a user account.")
        flash("An unexpected error occurred while creating the account.", "error")

    return redirect(url_for("admin.users"))


@admin_bp.route("/users/<int:user_id>/role", methods=["POST"])
@roles_required("Administrator")
def change_user_role(user_id):
    """Change a user's role."""

    current_user = get_current_user()

    try:
        new_role = request.form.get("role", "").strip()

        UserManagementService.change_role(
            target_user_id=user_id,
            new_role=new_role,
            administrator_id=current_user["user_id"],
        )

        flash("User role successfully updated.", "success")

    except ValueError as error:
        flash(str(error), "error")

    except Exception:
        current_app.logger.exception(
            "Failed to change role for user %s.",
            user_id,
        )

        flash(
            "An unexpected error occurred while updating the user's role.",
            "error",
        )

    return redirect(url_for("admin.users"))


@admin_bp.route("/users/<int:user_id>/status", methods=["POST"])
@roles_required("Administrator")
def change_user_status(user_id):
    """Activate or deactivate a user account."""

    current_user = get_current_user()

    try:
        requested_status = request.form.get("status", "").strip()

        if requested_status not in {"Active", "Inactive"}:
            raise ValueError("Invalid account status selected.")

        is_active = requested_status == "Active"

        UserManagementService.change_account_status(
            target_user_id=user_id,
            is_active=is_active,
            administrator_id=current_user["user_id"],
        )

        flash(
            "User account successfully "
            + ("activated." if is_active else "deactivated."),
            "success",
        )

    except ValueError as error:
        flash(str(error), "error")

    except Exception:
        current_app.logger.exception(
            "Failed to change account status for user %s.",
            user_id,
        )

        flash(
            "An unexpected error occurred while updating the account status.",
            "error",
        )

    return redirect(url_for("admin.users"))
