from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.repositories.incident_repository import IncidentRepository


def create_mock_database(fetchone_results=None, rowcount=1):
    """Create a mocked database connection and cursor."""

    connection = MagicMock()
    cursor = MagicMock()

    connection.cursor.return_value = cursor
    cursor.rowcount = rowcount
    cursor.fetchone.side_effect = fetchone_results or []

    return connection, cursor


# --------------------------------------------------
# TECHNICIAN ASSIGNMENT
# --------------------------------------------------


@patch("app.repositories.incident_repository.get_connection")
def test_assign_technician_successfully(mock_get_connection):
    connection, cursor = create_mock_database(
        [
            SimpleNamespace(Status="Open", TechnicianId=None),
            SimpleNamespace(FullName="Test Technician"),
        ]
    )

    mock_get_connection.return_value = connection

    result = IncidentRepository.assign_technician(
        incident_id=10,
        technician_id=2,
        assigned_by_user_id=1,
    )

    assert result["incident_id"] == 10
    assert result["technician_id"] == 2
    assert result["technician_name"] == "Test Technician"
    assert result["previous_status"] == "Open"
    assert result["new_status"] == "Open"
    assert result["action"] == "Technician Assigned"

    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    connection.close.assert_called_once()


@patch("app.repositories.incident_repository.get_connection")
def test_assign_technician_rejects_closed_incident(mock_get_connection):
    connection, cursor = create_mock_database(
        [
            SimpleNamespace(Status="Closed", TechnicianId=None),
        ]
    )

    mock_get_connection.return_value = connection

    with pytest.raises(ValueError, match="Closed incidents"):
        IncidentRepository.assign_technician(10, 2, 1)

    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()

    # No technician lookup should happen after the closed-status check.
    assert cursor.fetchone.call_count == 1


# --------------------------------------------------
# TECHNICIAN CLAIM
# --------------------------------------------------


@patch("app.repositories.incident_repository.get_connection")
def test_claim_incident_successfully(mock_get_connection):
    connection, cursor = create_mock_database(
        [
            SimpleNamespace(Status="Open", TechnicianId=None),
            SimpleNamespace(FullName="Test Technician"),
        ]
    )

    mock_get_connection.return_value = connection

    result = IncidentRepository.claim_incident(
        incident_id=15,
        technician_id=2,
    )

    assert result["incident_id"] == 15
    assert result["technician_id"] == 2
    assert result["technician_name"] == "Test Technician"
    assert result["previous_status"] == "Open"
    assert result["new_status"] == "Open"
    assert result["action"] == "Technician Claimed"

    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    connection.close.assert_called_once()


@patch("app.repositories.incident_repository.get_connection")
def test_claim_incident_rolls_back_if_another_technician_claimed_it(
    mock_get_connection,
):
    connection, cursor = create_mock_database(
        [
            SimpleNamespace(Status="Open", TechnicianId=None),
            SimpleNamespace(FullName="Test Technician"),
        ],
        rowcount=0,
    )

    mock_get_connection.return_value = connection

    with pytest.raises(ValueError, match="could not be claimed"):
        IncidentRepository.claim_incident(15, 2)

    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()


# --------------------------------------------------
# TROUBLESHOOTING RECORDS
# --------------------------------------------------


@patch("app.repositories.incident_repository.get_connection")
def test_add_troubleshooting_record_saves_record_and_audit(
    mock_get_connection,
):
    connection, cursor = create_mock_database(
        [
            SimpleNamespace(Status="In Progress"),
            SimpleNamespace(RecordId=25),
        ]
    )

    mock_get_connection.return_value = connection

    result = IncidentRepository.add_troubleshooting_record(
        incident_id=10,
        technician_id=2,
        action_taken="Restarted the network adapter.",
    )

    assert result == 25

    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    connection.close.assert_called_once()

    # Verify that both the troubleshooting record and audit log are inserted.
    executed_sql = [call.args[0] for call in cursor.execute.call_args_list]

    assert any("INSERT INTO dbo.TroubleshootingRecords" in sql for sql in executed_sql)

    assert any("INSERT INTO dbo.AuditLogs" in sql for sql in executed_sql)


# --------------------------------------------------
# RESOLUTION SUBMISSION
# --------------------------------------------------


@patch("app.repositories.incident_repository.get_connection")
def test_submit_resolution_rejects_incident_without_troubleshooting(
    mock_get_connection,
):
    connection, cursor = create_mock_database(
        [
            SimpleNamespace(
                Status="In Progress",
                IncidentReference="SD-20261119-ABC123",
                Title="Laptop problem",
                UserId=3,
                ReporterName="Test User",
                ReporterEmail="test@example.com",
            ),
            (0,),
        ]
    )

    mock_get_connection.return_value = connection

    with pytest.raises(ValueError, match="at least one troubleshooting"):
        IncidentRepository.submit_resolution(
            incident_id=10,
            technician_id=2,
            resolution_text="Reinstalled the network driver.",
        )

    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()

    # A resolution must not be inserted when troubleshooting is missing.
    executed_sql = [call.args[0] for call in cursor.execute.call_args_list]

    assert not any("INSERT INTO dbo.Resolutions" in sql for sql in executed_sql)


# --------------------------------------------------
# USER RESOLUTION FEEDBACK
# --------------------------------------------------


@patch("app.repositories.incident_repository.get_connection")
def test_accepting_resolution_closes_incident(mock_get_connection):
    connection, cursor = create_mock_database(
        [
            SimpleNamespace(
                Status="Awaiting User Confirmation",
                IncidentReference="SD-20261119-ABC123",
            ),
        ]
    )

    mock_get_connection.return_value = connection

    result = IncidentRepository.submit_resolution_feedback(
        resolution_id=5,
        incident_id=10,
        user_id=3,
        decision="Accepted",
        comments="The issue is resolved.",
    )

    assert result["incident_id"] == 10
    assert result["incident_reference"] == "SD-20261119-ABC123"
    assert result["decision"] == "Accepted"
    assert result["new_status"] == "Closed"

    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    connection.close.assert_called_once()

    executed_sql = [call.args[0] for call in cursor.execute.call_args_list]

    assert any("INSERT INTO dbo.UserFeedback" in sql for sql in executed_sql)

    assert any("UPDATE dbo.Incidents" in sql for sql in executed_sql)

    assert any("INSERT INTO dbo.AuditLogs" in sql for sql in executed_sql)


@patch("app.repositories.incident_repository.get_connection")
def test_rejecting_resolution_without_reason_rolls_back(
    mock_get_connection,
):
    connection, cursor = create_mock_database(
        [
            SimpleNamespace(
                Status="Awaiting User Confirmation",
                IncidentReference="SD-20261119-ABC123",
            ),
        ]
    )

    mock_get_connection.return_value = connection

    with pytest.raises(ValueError, match="reason"):
        IncidentRepository.submit_resolution_feedback(
            resolution_id=5,
            incident_id=10,
            user_id=3,
            decision="Rejected",
            comments="   ",
        )

    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()


@patch("app.repositories.incident_repository.get_connection")
def test_feedback_rejects_incident_not_awaiting_confirmation(
    mock_get_connection,
):
    connection, cursor = create_mock_database(
        [
            SimpleNamespace(
                Status="In Progress",
                IncidentReference="SD-20261119-ABC123",
            ),
        ]
    )

    mock_get_connection.return_value = connection

    with pytest.raises(ValueError, match="no longer awaiting confirmation"):
        IncidentRepository.submit_resolution_feedback(
            resolution_id=5,
            incident_id=10,
            user_id=3,
            decision="Accepted",
            comments="Resolved.",
        )

    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()
