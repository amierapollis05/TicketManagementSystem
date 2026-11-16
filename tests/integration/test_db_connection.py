from app.db.connection import get_connection


def test_database_connection():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                DB_NAME() AS DatabaseName,
                @@SERVERNAME AS ServerName
        """)

        result = cursor.fetchone()

        assert result is not None
        assert result.DatabaseName == "SupportDeskProDB"

        print(f"Connected database: {result.DatabaseName}")
        print(f"SQL Server: {result.ServerName}")

    finally:
        connection.close()
