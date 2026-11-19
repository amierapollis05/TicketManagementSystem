from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.security.decorators import roles_required
from app.security.session_user import get_current_user
from app.services.incident_service import IncidentService

incident_bp = Blueprint("incident", __name__, url_prefix="/incidents")


@incident_bp.route("/new", methods=["GET", "POST"])
@roles_required("User")
def create():
    """Allow a User to submit a new incident."""

    categories = IncidentService.get_categories()

    if request.method == "POST":

        current_user = get_current_user()

        try:
            category_id = int(request.form.get("category_id", ""))

            result = IncidentService.create_incident(
                user_id=current_user["user_id"],
                category_id=category_id,
                title=request.form.get("title", ""),
                description=request.form.get("description", ""),
                priority=request.form.get("priority", ""),
            )

            flash(
                f"Incident submitted successfully. "
                f"Your reference is {result['incident_reference']}.",
                "success",
            )

            return render_template(
                "incidents/create.html",
                categories=categories,
                incident_reference=result["incident_reference"],
            )

        except ValueError as error:
            flash(str(error), "error")

    return render_template(
        "incidents/create.html", categories=categories, incident_reference=None
    )


@incident_bp.route("/my-incidents")
@roles_required("User")
def my_incidents():
    """Display incidents reported by the logged-in user."""

    current_user = get_current_user()

    incidents = IncidentService.get_user_incidents(current_user["user_id"])

    return render_template("incidents/my_incidents.html", incidents=incidents)


@incident_bp.route("/<string:incident_reference>")
@roles_required("User")
def details(incident_reference):
    """Display details of an incident owned by the logged-in user."""

    current_user = get_current_user()

    incident = IncidentService.get_incident(incident_reference)

    if incident is None:
        from flask import abort

        abort(404)

    if incident["user_id"] != current_user["user_id"]:
        from flask import abort

        abort(403)

    return render_template("incidents/details.html", incident=incident)
