import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")

    DB_SERVER = os.getenv("DB_SERVER", r"Amier\SQLEXPRESS")

    DB_NAME = os.getenv("DB_NAME", "SupportDeskProDB")

    DB_TRUSTED_CONNECTION = os.getenv("DB_TRUSTED_CONNECTION", "yes")

    DB_ENCRYPT = os.getenv("DB_ENCRYPT", "yes")

    DB_TRUST_SERVER_CERTIFICATE = os.getenv("DB_TRUST_SERVER_CERTIFICATE", "yes")

    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    TESTING = False


class TestingConfig(Config):
    TESTING = True
