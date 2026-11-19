from flask import Blueprint, render_template

from app.security.decorators import roles_required
from app.security.session_user import get_current_user
from app.services.supervisor_service import SupervisorService

supervisor_bp = Blueprint(
    "supervisor",
    __name__,
    url_prefix="/supervisor",
)


@supervisor_bp.route("/")
@roles_required("Supervisor")
def dashboard():
    """Display organisation-wide operational oversight."""

    current_user = get_current_user()

    dashboard_data = SupervisorService.get_dashboard_data()

    return render_template(
        "supervisor/dashboard.html",
        current_user=current_user,
        data=dashboard_data,
    )
