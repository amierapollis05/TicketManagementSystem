import logging

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from app.config import Config
from app.errors import register_error_handlers

csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    csrf.init_app(app)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    from app.security.session_user import get_current_user

    @app.context_processor
    def inject_current_user():
        return {"current_user": get_current_user()}

    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.incident_routes import incident_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.technician_routes import technician_bp
    from app.routes.resolution_routes import resolution_bp
    from app.routes.supervisor_routes import supervisor_bp
    from app.routes.reporting_routes import reporting_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(incident_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(resolution_bp)
    app.register_blueprint(technician_bp)
    app.register_blueprint(supervisor_bp)
    app.register_blueprint(reporting_bp)

    register_error_handlers(app)

    app.logger.info("SupportDesk Pro application initialized.")

    return app
