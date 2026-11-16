from flask import render_template
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):

    @app.errorhandler(HTTPException)
    def handle_http_error(error):

        return (
            render_template(
                "errors/error.html",
                error_code=error.code,
                error_name=error.name,
                error_description=error.description,
            ),
            error.code,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):

        app.logger.exception("An unexpected application error occurred.")

        return (
            render_template(
                "errors/error.html",
                error_code=500,
                error_name="Internal Server Error",
                error_description=("Something went wrong. Please try again later."),
            ),
            500,
        )
