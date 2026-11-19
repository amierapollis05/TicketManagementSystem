from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from html import escape

from app.security.resolution_tokens import generate_resolution_token
from app.services.email_service import EmailService
from app.security.decorators import roles_required
from app.security.session_user import get_current_user
from app.services.incident_service import IncidentService

technician_bp = Blueprint(
    "technician",
    __name__,
    url_prefix="/technician",
)


@technician_bp.route("/")
@roles_required("Technician")
def dashboard():
    """Display the technician workspace."""

    current_user = get_current_user()

    incidents = IncidentService.get_technician_incidents(current_user["user_id"])

    statistics = {
        "total": len(incidents),
        "open": sum(1 for incident in incidents if incident["status"] == "Open"),
        "in_progress": sum(
            1 for incident in incidents if incident["status"] == "In Progress"
        ),
        "awaiting_confirmation": sum(
            1
            for incident in incidents
            if incident["status"] == "Awaiting User Confirmation"
        ),
        "reopened": sum(
            1 for incident in incidents if incident["status"] == "Reopened"
        ),
    }

    return render_template(
        "technician/dashboard.html",
        current_user=current_user,
        incidents=incidents,
        statistics=statistics,
    )


@technician_bp.route("/incidents")
@roles_required("Technician")
def incidents():
    """Display all incidents assigned to the technician."""

    current_user = get_current_user()

    assigned_incidents = IncidentService.get_technician_incidents(
        current_user["user_id"]
    )

    return render_template(
        "technician/incidents.html",
        incidents=assigned_incidents,
    )


@technician_bp.route("/incidents/<int:incident_id>")
@roles_required("Technician")
def incident_details(incident_id):
    """Display details and investigation history."""

    current_user = get_current_user()
    technician_id = current_user["user_id"]

    incident = IncidentService.get_technician_incident_details(
        incident_id=incident_id,
        technician_id=technician_id,
    )

    if incident is None:
        abort(404)

    troubleshooting_records = IncidentService.get_troubleshooting_records(incident_id)

    pending_resolution = None

    if incident["status"] == "Awaiting User Confirmation":
        pending_resolution = IncidentService.get_latest_pending_resolution(
            incident_id=incident_id,
            technician_id=technician_id,
        )

    return render_template(
        "technician/details.html",
        incident=incident,
        troubleshooting_records=troubleshooting_records,
        pending_resolution=pending_resolution,
    )


@technician_bp.route(
    "/incidents/<int:incident_id>/troubleshooting",
    methods=["POST"],
)
@roles_required("Technician")
def add_troubleshooting(incident_id):
    """Save a troubleshooting action for an assigned incident."""

    current_user = get_current_user()

    # Verify ownership before processing the submitted form.
    incident = IncidentService.get_technician_incident_details(
        incident_id=incident_id,
        technician_id=current_user["user_id"],
    )

    if incident is None:
        abort(404)

    action_taken = request.form.get("action_taken", "")

    try:
        IncidentService.add_troubleshooting_record(
            incident_id=incident_id,
            technician_id=current_user["user_id"],
            action_taken=action_taken,
        )

        flash("Troubleshooting action recorded successfully.", "success")

    except ValueError as error:
        flash(str(error), "error")

    except Exception:
        flash(
            "An unexpected error occurred while saving the troubleshooting record.",
            "error",
        )

    return redirect(
        url_for(
            "technician.incident_details",
            incident_id=incident_id,
        )
    )


@technician_bp.route(
    "/incidents/<int:incident_id>/resolution",
    methods=["POST"],
)
@roles_required("Technician")
def submit_resolution(incident_id):
    """Submit a proposed resolution and notify the reporting user."""

    current_user = get_current_user()

    incident = IncidentService.get_technician_incident_details(
        incident_id=incident_id,
        technician_id=current_user["user_id"],
    )

    if incident is None:
        abort(404)

    resolution_text = request.form.get("resolution_text", "")

    try:
        # Save the resolution and update the incident first.
        result = IncidentService.submit_resolution(
            incident_id=incident_id,
            technician_id=current_user["user_id"],
            resolution_text=resolution_text,
        )

    except ValueError as error:
        flash(str(error), "error")
        return redirect(
            url_for(
                "technician.incident_details",
                incident_id=incident_id,
            )
        )

    except Exception:
        current_app.logger.exception(
            "Failed to submit resolution for incident %s.",
            incident_id,
        )
        flash(
            "The resolution could not be submitted due to an unexpected error.",
            "error",
        )
        return redirect(
            url_for(
                "technician.incident_details",
                incident_id=incident_id,
            )
        )

    # The database transaction has committed at this point.
    # Email delivery is a separate operation.
    try:
        token = generate_resolution_token(
            resolution_id=result["resolution_id"],
            incident_id=result["incident_id"],
            user_id=result["user_id"],
        )

        review_url = url_for(
            "resolution.review_resolution",
            token=token,
            _external=True,
        )

        safe_name = escape(result["reporter_name"])
        safe_reference = escape(result["incident_reference"])
        safe_title = escape(result["incident_title"])
        safe_resolution = escape(result["resolution_text"])

        body_text = (
            f"Hello {result['reporter_name']},\n\n"
            "A technician has submitted a proposed resolution "
            "for your SupportDesk Pro incident.\n\n"
            f"Incident: {result['incident_reference']}\n"
            f"Title: {result['incident_title']}\n\n"
            "Proposed resolution:\n"
            f"{result['resolution_text']}\n\n"
            "Please review the proposed resolution and accept or reject it:\n"
            f"{review_url}\n\n"
            "This secure review link expires after seven days.\n\n"
            "SupportDesk Pro"
        )

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #263238;">
            <h2>SupportDesk Pro - Resolution Confirmation</h2>

            <p>Hello {safe_name},</p>

            <p>
                A technician has submitted a proposed resolution
                for your incident.
            </p>

            <p><strong>Incident:</strong> {safe_reference}</p>
            <p><strong>Title:</strong> {safe_title}</p>

            <h3>Proposed Resolution</h3>

            <div style="
                background: #f4f6f9;
                padding: 16px;
                border-left: 4px solid #174ea6;
                white-space: pre-wrap;
            ">{safe_resolution}</div>

            <p>
                Please review the resolution and indicate whether
                your issue has been resolved.
            </p>

            <p>
                <a href="{escape(review_url, quote=True)}"
                   style="
                       background: #174ea6;
                       color: white;
                       padding: 12px 20px;
                       text-decoration: none;
                       border-radius: 5px;
                       display: inline-block;
                   ">
                    Review Proposed Resolution
                </a>
            </p>

            <p>This secure link expires after seven days.</p>

            <p>SupportDesk Pro</p>
        </body>
        </html>
        """

        EmailService.send_email(
            recipient=result["reporter_email"],
            subject=(
                f"Resolution awaiting your confirmation - "
                f"{result['incident_reference']}"
            ),
            body_text=body_text,
            html_body=html_body,
        )

        flash(
            "Resolution submitted successfully. "
            "The reporting user has been emailed.",
            "success",
        )

    except Exception:
        current_app.logger.exception(
            "Resolution saved, but notification email failed for incident %s.",
            incident_id,
        )

        flash(
            "The resolution was saved, but the notification email could not "
            "be sent. The incident is awaiting user confirmation. "
            "Email delivery needs to be retried.",
            "error",
        )

    return redirect(
        url_for(
            "technician.incident_details",
            incident_id=incident_id,
        )
    )


@technician_bp.route(
    "/incidents/<int:incident_id>/resolution/<int:resolution_id>/resend",
    methods=["POST"],
)
@roles_required("Technician")
def resend_resolution_email(incident_id, resolution_id):
    """Resend the notification for an existing pending resolution."""

    current_user = get_current_user()
    technician_id = current_user["user_id"]

    try:
        # Retrieve the existing resolution and verify technician ownership.
        result = IncidentService.get_pending_resolution_for_resend(
            incident_id=incident_id,
            technician_id=technician_id,
            resolution_id=resolution_id,
        )

        # Generate a fresh, time-limited review token.
        token = generate_resolution_token(
            resolution_id=result["resolution_id"],
            incident_id=result["incident_id"],
            user_id=result["user_id"],
        )

        review_url = url_for(
            "resolution.review_resolution",
            token=token,
            _external=True,
        )

        safe_name = escape(result["reporter_name"])
        safe_reference = escape(result["incident_reference"])
        safe_title = escape(result["incident_title"])
        safe_resolution = escape(result["resolution_text"])

        body_text = (
            f"Hello {result['reporter_name']},\n\n"
            "This is a reminder that a technician has submitted "
            "a proposed resolution for your SupportDesk Pro incident.\n\n"
            f"Incident: {result['incident_reference']}\n"
            f"Title: {result['incident_title']}\n\n"
            "Proposed resolution:\n"
            f"{result['resolution_text']}\n\n"
            "Please review the proposed resolution and accept or reject it:\n"
            f"{review_url}\n\n"
            "This secure review link expires after seven days.\n\n"
            "SupportDesk Pro"
        )

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #263238;">
            <h2>SupportDesk Pro - Resolution Confirmation</h2>

            <p>Hello {safe_name},</p>

            <p>
                This is a reminder that a technician has submitted
                a proposed resolution for your incident.
            </p>

            <p><strong>Incident:</strong> {safe_reference}</p>
            <p><strong>Title:</strong> {safe_title}</p>

            <h3>Proposed Resolution</h3>

            <div style="
                background: #f4f6f9;
                padding: 16px;
                border-left: 4px solid #174ea6;
                white-space: pre-wrap;
            ">{safe_resolution}</div>

            <p>Please review the resolution and indicate whether
            your issue has been resolved.</p>

            <p>
                <a href="{escape(review_url, quote=True)}"
                   style="
                       background: #174ea6;
                       color: white;
                       padding: 12px 20px;
                       text-decoration: none;
                       border-radius: 5px;
                       display: inline-block;
                   ">
                    Review Proposed Resolution
                </a>
            </p>

            <p>This secure link expires after seven days.</p>
            <p>SupportDesk Pro</p>
        </body>
        </html>
        """

        # Send the existing resolution notification.
        EmailService.send_email(
            recipient=result["reporter_email"],
            subject=(
                "Reminder: Resolution awaiting your confirmation - "
                f"{result['incident_reference']}"
            ),
            body_text=body_text,
            html_body=html_body,
        )

        # Record the resend only after successful email delivery to SMTP.
        IncidentService.record_resolution_email_resent(
            incident_id=incident_id,
            technician_id=technician_id,
            resolution_id=resolution_id,
        )

        flash(
            "The existing resolution notification was successfully resent "
            f"to {result['reporter_email']}.",
            "success",
        )

    except ValueError as error:
        flash(str(error), "error")

    except Exception:
        current_app.logger.exception(
            "Failed to resend resolution notification for incident %s "
            "and resolution %s.",
            incident_id,
            resolution_id,
        )

        flash(
            "The notification could not be resent. Check the application logs.",
            "error",
        )

    return redirect(
        url_for(
            "technician.incident_details",
            incident_id=incident_id,
        )
    )
