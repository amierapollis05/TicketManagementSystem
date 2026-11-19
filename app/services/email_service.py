import smtplib
import ssl
from email.message import EmailMessage

from app.config import Config


class EmailService:

    @staticmethod
    def send_email(
        recipient: str,
        subject: str,
        body_text: str,
        html_body: str = None,
    ) -> None:

        if not Config.MAIL_USERNAME or not Config.MAIL_PASSWORD:
            raise RuntimeError("Email credentials are not configured.")

        if not recipient or "@" not in recipient:
            raise ValueError("A valid recipient email address is required.")

        if not subject.strip():
            raise ValueError("Email subject cannot be empty.")

        if not body_text.strip():
            raise ValueError("Email body cannot be empty.")

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = Config.MAIL_DEFAULT_SENDER
        message["To"] = recipient

        message.set_content(body_text)

        if html_body:
            message.add_alternative(html_body, subtype="html")

        context = ssl.create_default_context()

        with smtplib.SMTP(
            Config.MAIL_SERVER,
            Config.MAIL_PORT,
            timeout=30,
        ) as server:

            server.ehlo()

            if Config.MAIL_USE_TLS:
                server.starttls(context=context)
                server.ehlo()

            server.login(
                Config.MAIL_USERNAME,
                Config.MAIL_PASSWORD,
            )

            server.send_message(message)
