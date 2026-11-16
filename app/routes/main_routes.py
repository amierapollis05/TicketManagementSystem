from flask import Blueprint, jsonify, render_template

from app.services.database_service import DatabaseService

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
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
