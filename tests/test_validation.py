import pytest
from unittest.mock import patch

from app.services.incident_service import IncidentService

# --------------------------------------------------
# INCIDENT CREATION VALIDATION
# --------------------------------------------------


@pytest.mark.parametrize("user_id", [0, -1, None, "1"])
def test_create_incident_rejects_invalid_user_id(user_id):
    with pytest.raises(ValueError, match="Invalid reporting user"):
        IncidentService.create_incident(
            user_id, 1, "Test incident", "Description", "Medium"
        )


@pytest.mark.parametrize("category_id", [0, -1, None, "1"])
def test_create_incident_rejects_invalid_category_id(category_id):
    with pytest.raises(ValueError, match="valid category"):
        IncidentService.create_incident(
            1, category_id, "Test incident", "Description", "Medium"
        )


@pytest.mark.parametrize("title", ["", "   ", None, 123])
def test_create_incident_rejects_invalid_title(title):
    with pytest.raises(ValueError, match="title is required"):
        IncidentService.create_incident(1, 1, title, "Description", "Medium")


@pytest.mark.parametrize("description", ["", "   ", None, 123])
def test_create_incident_rejects_invalid_description(description):
    with pytest.raises(ValueError, match="description is required"):
        IncidentService.create_incident(1, 1, "Test incident", description, "Medium")


def test_create_incident_rejects_title_over_150_characters():
    with pytest.raises(ValueError, match="150 characters"):
        IncidentService.create_incident(1, 1, "A" * 151, "Description", "Medium")


def test_create_incident_rejects_description_over_4000_characters():
    with pytest.raises(ValueError, match="4000 characters"):
        IncidentService.create_incident(1, 1, "Test incident", "A" * 4001, "Medium")


@pytest.mark.parametrize("priority", ["Urgent", "Critical", "", None])
def test_create_incident_rejects_invalid_priority(priority):
    with pytest.raises(ValueError, match="valid priority"):
        IncidentService.create_incident(1, 1, "Test incident", "Description", priority)


def test_create_incident_rejects_nonexistent_category():
    with patch(
        "app.services.incident_service.IncidentRepository.get_categories",
        return_value=[{"category_id": 1}],
    ):
        with pytest.raises(ValueError, match="category does not exist"):
            IncidentService.create_incident(
                1, 2, "Test incident", "Description", "Medium"
            )


def test_create_incident_trims_input_and_saves_valid_incident():
    with patch.object(
        IncidentService,
        "get_categories",
        return_value=[{"category_id": 1}],
    ), patch.object(
        IncidentService,
        "generate_incident_reference",
        return_value="SD-20261119-ABC123",
    ), patch(
        "app.services.incident_service.IncidentRepository.create_incident",
        return_value=42,
    ) as create_mock:

        result = IncidentService.create_incident(
            1,
            1,
            "  Laptop problem  ",
            "  Cannot connect to Wi-Fi  ",
            "Medium",
        )

    assert result["incident_id"] == 42
    assert result["incident_reference"] == "SD-20261119-ABC123"

    create_mock.assert_called_once_with(
        incident_reference="SD-20261119-ABC123",
        user_id=1,
        category_id=1,
        title="Laptop problem",
        description="Cannot connect to Wi-Fi",
        priority="Medium",
    )


# --------------------------------------------------
# INCIDENT SEARCH AND FILTER VALIDATION
# --------------------------------------------------


def test_search_filters_trim_search_term():
    result = IncidentService._validate_incident_filters(search_term="  Wi-Fi problem  ")

    assert result == "Wi-Fi problem"


def test_search_filters_reject_non_string_search_term():
    with pytest.raises(ValueError, match="Invalid search term"):
        IncidentService._validate_incident_filters(search_term=123)


def test_search_filters_reject_search_term_over_100_characters():
    with pytest.raises(ValueError, match="100 characters"):
        IncidentService._validate_incident_filters(search_term="A" * 101)


@pytest.mark.parametrize(
    "status",
    ["Invalid", "Pending", "Deleted", "Closed Incident"],
)
def test_search_filters_reject_invalid_status(status):
    with pytest.raises(ValueError, match="Invalid incident status"):
        IncidentService._validate_incident_filters(status=status)


@pytest.mark.parametrize(
    "status",
    ["", "Open", "In Progress", "Awaiting User Confirmation", "Reopened", "Closed"],
)
def test_search_filters_accept_valid_status(status):
    result = IncidentService._validate_incident_filters(status=status)

    assert result == ""


@pytest.mark.parametrize("priority", ["Urgent", "Critical", "Normal"])
def test_search_filters_reject_invalid_priority(priority):
    with pytest.raises(ValueError, match="Invalid priority"):
        IncidentService._validate_incident_filters(priority=priority)


@pytest.mark.parametrize("priority", ["", "Low", "Medium", "High"])
def test_search_filters_accept_valid_priority(priority):
    result = IncidentService._validate_incident_filters(priority=priority)

    assert result == ""


@pytest.mark.parametrize("category_id", [0, -1, "1"])
def test_search_filters_reject_invalid_category_id(category_id):
    with pytest.raises(ValueError, match="Invalid category"):
        IncidentService._validate_incident_filters(category_id=category_id)


def test_search_filters_reject_nonexistent_category():
    with patch(
        "app.services.incident_service.IncidentRepository.get_categories",
        return_value=[{"category_id": 1}],
    ):
        with pytest.raises(ValueError, match="category does not exist"):
            IncidentService._validate_incident_filters(category_id=2)


def test_search_all_incidents_rejects_invalid_status_before_repository_call():
    with patch(
        "app.services.incident_service.IncidentRepository.search_all_incidents"
    ) as search_mock:

        with pytest.raises(ValueError):
            IncidentService.search_all_incidents(status="Invalid")

        search_mock.assert_not_called()


# --------------------------------------------------
# TECHNICIAN AND ADMINISTRATOR VALIDATION
# --------------------------------------------------


@pytest.mark.parametrize("technician_id", [0, -1, None, "2"])
def test_claim_incident_rejects_invalid_technician_id(technician_id):
    with pytest.raises(ValueError, match="technician account"):
        IncidentService.claim_incident(1, technician_id)


@pytest.mark.parametrize("incident_id", [0, -1, None, "1"])
def test_claim_incident_rejects_invalid_incident_id(incident_id):
    with pytest.raises(ValueError, match="Invalid incident"):
        IncidentService.claim_incident(incident_id, 2)


def test_assign_technician_rejects_invalid_administrator_id():
    with pytest.raises(ValueError, match="administrator account"):
        IncidentService.assign_technician(1, 2, 0)


# --------------------------------------------------
# TROUBLESHOOTING VALIDATION
# --------------------------------------------------


@pytest.mark.parametrize("action", ["", "   ", None, 123])
def test_troubleshooting_rejects_empty_or_invalid_action(action):
    with pytest.raises(ValueError, match="troubleshooting action"):
        IncidentService.add_troubleshooting_record(1, 2, action)


def test_troubleshooting_rejects_action_over_2000_characters():
    with pytest.raises(ValueError, match="2000 characters"):
        IncidentService.add_troubleshooting_record(1, 2, "A" * 2001)


def test_troubleshooting_trims_action_before_saving():
    with patch(
        "app.services.incident_service.IncidentRepository.add_troubleshooting_record",
        return_value=15,
    ) as repository_mock:

        result = IncidentService.add_troubleshooting_record(
            1, 2, "  Restarted the network adapter  "
        )

    assert result == 15

    repository_mock.assert_called_once_with(
        incident_id=1,
        technician_id=2,
        action_taken="Restarted the network adapter",
    )


# --------------------------------------------------
# RESOLUTION VALIDATION
# --------------------------------------------------


@pytest.mark.parametrize("resolution_text", ["", "   ", None, 123])
def test_submit_resolution_rejects_invalid_text(resolution_text):
    with pytest.raises(ValueError, match="proposed resolution"):
        IncidentService.submit_resolution(1, 2, resolution_text)


def test_submit_resolution_rejects_text_over_2000_characters():
    with pytest.raises(ValueError, match="2000 characters"):
        IncidentService.submit_resolution(1, 2, "A" * 2001)


@pytest.mark.parametrize("decision", ["Pending", "Cancelled", "", None])
def test_feedback_rejects_invalid_decision(decision):
    with pytest.raises(ValueError, match="Accept or Reject"):
        IncidentService.submit_resolution_feedback(1, 1, 1, decision, "Some comments")


def test_feedback_rejects_rejection_without_reason():
    with pytest.raises(ValueError, match="rejecting this resolution"):
        IncidentService.submit_resolution_feedback(1, 1, 1, "Rejected", "   ")


def test_feedback_rejects_comments_over_1000_characters():
    with pytest.raises(ValueError, match="1000 characters"):
        IncidentService.submit_resolution_feedback(1, 1, 1, "Accepted", "A" * 1001)


def test_feedback_rejects_non_string_comments():
    with pytest.raises(ValueError, match="Invalid feedback"):
        IncidentService.submit_resolution_feedback(1, 1, 1, "Accepted", None)


def test_feedback_trims_rejection_reason_before_saving():
    with patch(
        "app.services.incident_service.IncidentRepository.submit_resolution_feedback",
        return_value={"decision": "Rejected", "new_status": "Reopened"},
    ) as repository_mock:

        result = IncidentService.submit_resolution_feedback(
            1, 2, 3, "Rejected", "  The issue is still happening.  "
        )

    assert result["decision"] == "Rejected"

    repository_mock.assert_called_once_with(
        resolution_id=1,
        incident_id=2,
        user_id=3,
        decision="Rejected",
        comments="The issue is still happening.",
    )
