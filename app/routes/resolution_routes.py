from flask import (
    Blueprint,
    abort,
    current_app,
    make_response,
    render_template,
    request,
)

from app.security.resolution_tokens import verify_resolution_token
from app.services.incident_service import IncidentService

resolution_bp = Blueprint(
    "resolution",
    __name__,
    url_prefix="/resolution",
)


def render_private_page(template_name, **context):
    """Prevent sensitive resolution pages from being cached or referenced."""

    response = make_response(render_template(template_name, **context))

    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Referrer-Policy"] = "no-referrer"

    return response


def get_review_context(token):
    """Validate the token and retrieve its pending resolution."""

    payload = verify_resolution_token(token)

    if payload is None:
        abort(404)

    resolution = IncidentService.get_resolution_for_review(
        resolution_id=payload["resolution_id"],
        incident_id=payload["incident_id"],
        user_id=payload["user_id"],
    )

    if resolution is None:
        abort(404)

    return payload, resolution


@resolution_bp.route("/<token>", methods=["GET", "POST"])
def review_resolution(token):
    """Allow the reporting user to accept or reject a proposed resolution."""

    payload, resolution = get_review_context(token)

    if request.method == "GET":
        return render_private_page(
            "resolutions/review.html",
            resolution=resolution,
            token=token,
            error=None,
        )

    decision = request.form.get("decision", "").strip()
    comments = request.form.get("comments", "")

    try:
        result = IncidentService.submit_resolution_feedback(
            resolution_id=payload["resolution_id"],
            incident_id=payload["incident_id"],
            user_id=payload["user_id"],
            decision=decision,
            comments=comments,
        )

        return render_private_page(
            "resolutions/outcome.html",
            result=result,
        )

    except ValueError as error:
        # The resolution remains available if the submitted form
        # contains invalid feedback.
        return render_private_page(
            "resolutions/review.html",
            resolution=resolution,
            token=token,
            error=str(error),
        )

    except Exception:
        current_app.logger.exception(
            "Unexpected error while processing resolution feedback."
        )

        return render_private_page(
            "resolutions/review.html",
            resolution=resolution,
            token=token,
            error=(
                "We could not process your decision. "
                "Please try again. If the problem continues, "
                "contact your support team."
            ),
        )
