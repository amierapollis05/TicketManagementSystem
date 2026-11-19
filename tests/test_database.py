from unittest.mock import MagicMock, patch

import pytest

from app.repositories.database_repository import DatabaseRepository


def test_get_database_status_returns_database_and_server():
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_connection.cursor.return_value = mock_cursor

    mock_result = MagicMock()
    mock_result.DatabaseName = "SupportDeskProDB"
    mock_result.ServerName = "Amier\\SQLEXPRESS"

    mock_cursor.fetchone.return_value = mock_result

    with patch(
        "app.repositories.database_repository.get_connection",
        return_value=mock_connection,
    ):
        result = DatabaseRepository.get_database_status()

    assert result == {
        "database": "SupportDeskProDB",
        "server": "Amier\\SQLEXPRESS",
    }

    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchone.assert_called_once()
    mock_connection.close.assert_called_once()


def test_get_database_status_closes_connection_if_query_fails():
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database query failed")

    with patch(
        "app.repositories.database_repository.get_connection",
        return_value=mock_connection,
    ):
        with pytest.raises(Exception, match="Database query failed"):
            DatabaseRepository.get_database_status()

    mock_connection.close.assert_called_once()
