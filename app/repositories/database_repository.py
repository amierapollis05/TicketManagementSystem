from app.db.connection import get_connection


class DatabaseRepository:

    @staticmethod
    def get_database_status():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    DB_NAME() AS DatabaseName,
                    @@SERVERNAME AS ServerName
            """)

            result = cursor.fetchone()

            return {"database": result.DatabaseName, "server": result.ServerName}

        finally:
            connection.close()
