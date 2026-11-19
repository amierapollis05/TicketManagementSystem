from flask import Blueprint, jsonify, redirect, render_template, url_for

from app.security.session_user import get_current_user
from app.services.database_service import DatabaseService

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    current_user = get_current_user()

    if current_user:
        if current_user["role"] == "Supervisor":
            return redirect(url_for("supervisor.dashboard"))

        return redirect(url_for("dashboard.index"))

    return render_template("home.html")


@main_bp.route("/health")
def health():
    return jsonify({"application": "SupportDesk Pro", "status": "running"}), 200


@main_bp.route("/health/database")
def database_health():
    try:
        database_status = DatabaseService.check_database_connection()

        return (
            jsonify(
                {
                    "application": "SupportDesk Pro",
                    "database_status": "connected",
                    "database": database_status["database"],
                    "server": database_status["server"],
                }
            ),
            200,
        )

    except Exception:
        return (
            jsonify(
                {
                    "application": "SupportDesk Pro",
                    "database_status": "disconnected",
                    "message": "Unable to connect to the database.",
                }
            ),
            503,
        )
