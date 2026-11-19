from flask import Blueprint, abort, redirect, render_template, url_for

from app.security.decorators import login_required, roles_required
from app.security.session_user import get_current_user
from app.services.dashboard_service import DashboardService

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def index():
    current_user = get_current_user()
    if current_user["role"] == "Supervisor":
        return redirect(url_for("supervisor.dashboard"))
    dashboard = DashboardService.get_dashboard(current_user["role"])

    if dashboard is None:
        abort(403)

    return render_template(
        "dashboard/index.html", current_user=current_user, dashboard=dashboard
    )


@dashboard_bp.route("/user")
@login_required
@roles_required("User")
def user_dashboard():
    return "User access granted.", 200


@dashboard_bp.route("/technician")
@login_required
@roles_required("Technician")
def technician_dashboard():
    return redirect(url_for("technician.dashboard"))


@dashboard_bp.route("/administrator")
@login_required
@roles_required("Administrator")
def administrator_dashboard():
    return "Administrator access granted.", 200


@dashboard_bp.route("/supervisor")
@login_required
@roles_required("Supervisor")
def supervisor_dashboard():
    return redirect(url_for("supervisor.dashboard"))
