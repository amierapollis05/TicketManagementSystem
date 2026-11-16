import pyodbc

from app.config import Config


def get_connection():
    """
    Establish a connection to the SupportDesk Pro database
    using Windows Authentication.
    """

    connection_string = (
        f"DRIVER={{{Config.DB_DRIVER}}};"
        f"SERVER={Config.DB_SERVER};"
        f"DATABASE={Config.DB_NAME};"
        f"Trusted_Connection={Config.DB_TRUSTED_CONNECTION};"
        f"Encrypt={Config.DB_ENCRYPT};"
        f"TrustServerCertificate={Config.DB_TRUST_SERVER_CERTIFICATE};"
    )

    connection = pyodbc.connect(connection_string, timeout=5)

    return connection
