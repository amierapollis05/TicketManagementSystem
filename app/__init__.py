import logging

from flask import Flask

from app.config import Config
from app.errors import register_error_handlers


def create_app(config_class=Config):

    app = Flask(__name__)

    app.config.from_object(config_class)

    logging.basicConfig(
        level=logging.INFO,
        format=("%(asctime)s - %(levelname)s - " "%(name)s - %(message)s"),
    )

    from app.routes.main_routes import main_bp

    app.register_blueprint(main_bp)

    register_error_handlers(app)

    app.logger.info("SupportDesk Pro application initialized.")

    return app
