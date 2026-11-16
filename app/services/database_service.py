from app.repositories.database_repository import DatabaseRepository


class DatabaseService:

    @staticmethod
    def check_database_connection():
        return DatabaseRepository.get_database_status()
