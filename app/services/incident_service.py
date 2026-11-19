import secrets
from datetime import datetime

from app.repositories.incident_repository import IncidentRepository
from app.repositories.user_repository import UserRepository


class IncidentService:
    """Handles incident business logic and validation."""

    VALID_PRIORITIES = ("Low", "Medium", "High")

    @staticmethod
    def generate_incident_reference():
        timestamp = datetime.now().strftime("%Y%m%d")
        random_code = secrets.token_hex(3).upper()

        return f"SD-{timestamp}-{random_code}"

    @staticmethod
    def get_categories():
        return IncidentRepository.get_categories()

    @staticmethod
    def create_incident(
        user_id: int,
        category_id: int,
        title: str,
        description: str,
        priority: str,
    ):
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid reporting user.")

        if not isinstance(category_id, int) or category_id <= 0:
            raise ValueError("Please select a valid category.")

        if not isinstance(title, str) or not title.strip():
            raise ValueError("Incident title is required.")

        if not isinstance(description, str) or not description.strip():
            raise ValueError("Incident description is required.")

        title = title.strip()
        description = description.strip()

        if len(title) > 150:
            raise ValueError("Incident title cannot exceed 150 characters.")

        if len(description) > 4000:
            raise ValueError("Incident description cannot exceed 4000 characters.")

        if priority not in IncidentService.VALID_PRIORITIES:
            raise ValueError("Please select a valid priority.")

        categories = IncidentRepository.get_categories()

        valid_category_ids = {category["category_id"] for category in categories}

        if category_id not in valid_category_ids:
            raise ValueError("The selected category does not exist.")

        incident_reference = IncidentService.generate_incident_reference()

        incident_id = IncidentRepository.create_incident(
            incident_reference=incident_reference,
            user_id=user_id,
            category_id=category_id,
            title=title,
            description=description,
            priority=priority,
        )

        return {
            "incident_id": incident_id,
            "incident_reference": incident_reference,
        }

    @staticmethod
    def get_incident(incident_reference: str):
        if not isinstance(incident_reference, str) or not incident_reference.strip():
            raise ValueError("A valid incident reference is required.")

        return IncidentRepository.get_by_reference(incident_reference.strip())

    @staticmethod
    def get_user_incidents(user_id: int):
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user account.")

        return IncidentRepository.get_by_user(user_id)

    @staticmethod
    def _validate_incident_filters(
        search_term: str = "",
        status: str = "",
        priority: str = "",
        category_id: int | None = None,
    ):
        """Validate incident search and filter inputs."""

        valid_statuses = (
            "Open",
            "In Progress",
            "Awaiting User Confirmation",
            "Reopened",
            "Closed",
        )

        if not isinstance(search_term, str):
            raise ValueError("Invalid search term.")

        search_term = search_term.strip()

        if len(search_term) > 100:
            raise ValueError("Search cannot exceed 100 characters.")

        if status not in ("", *valid_statuses):
            raise ValueError("Invalid incident status selected.")

        if priority not in ("", *IncidentService.VALID_PRIORITIES):
            raise ValueError("Invalid priority selected.")

        if category_id is not None:
            if not isinstance(category_id, int) or category_id <= 0:
                raise ValueError("Invalid category selected.")

            categories = IncidentRepository.get_categories()
            valid_ids = {category["category_id"] for category in categories}

            if category_id not in valid_ids:
                raise ValueError("The selected category does not exist.")

        return search_term

    @staticmethod
    def search_all_incidents(
        search_term: str = "",
        status: str = "",
        priority: str = "",
        category_id: int | None = None,
    ):
        search_term = IncidentService._validate_incident_filters(
            search_term, status, priority, category_id
        )

        return IncidentRepository.search_all_incidents(
            search_term, status, priority, category_id
        )

    @staticmethod
    def search_user_incidents(
        user_id: int,
        search_term: str = "",
        status: str = "",
        priority: str = "",
        category_id: int | None = None,
    ):
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user account.")

        search_term = IncidentService._validate_incident_filters(
            search_term, status, priority, category_id
        )

        return IncidentRepository.search_user_incidents(
            user_id, search_term, status, priority, category_id
        )

    @staticmethod
    def search_technician_incidents(
        technician_id: int,
        search_term: str = "",
        status: str = "",
        priority: str = "",
        category_id: int | None = None,
    ):
        if not isinstance(technician_id, int) or technician_id <= 0:
            raise ValueError("Invalid technician account.")

        search_term = IncidentService._validate_incident_filters(
            search_term, status, priority, category_id
        )

        return IncidentRepository.search_technician_incidents(
            technician_id, search_term, status, priority, category_id
        )

    @staticmethod
    def get_active_technicians():
        return UserRepository.get_active_technicians()

    @staticmethod
    def assign_technician(
        incident_id: int,
        technician_id: int,
        assigned_by_user_id: int,
    ):
        """Validate and assign a technician to an incident."""

        if not isinstance(incident_id, int) or incident_id <= 0:
            raise ValueError("Invalid incident selected.")

        if not isinstance(technician_id, int) or technician_id <= 0:
            raise ValueError("Please select a valid technician.")

        if not isinstance(assigned_by_user_id, int) or assigned_by_user_id <= 0:
            raise ValueError("Invalid administrator account.")

        return IncidentRepository.assign_technician(
            incident_id=incident_id,
            technician_id=technician_id,
            assigned_by_user_id=assigned_by_user_id,
        )

    @staticmethod
    def claim_incident(incident_id: int, technician_id: int):
        """Validate and claim an unassigned incident."""

        if not isinstance(incident_id, int) or incident_id <= 0:
            raise ValueError("Invalid incident selected.")

        if not isinstance(technician_id, int) or technician_id <= 0:
            raise ValueError("Invalid technician account.")

        return IncidentRepository.claim_incident(
            incident_id=incident_id,
            technician_id=technician_id,
        )

    @staticmethod
    def get_technician_incidents(technician_id: int):
        """Retrieve incidents assigned to a technician."""

        if not isinstance(technician_id, int) or technician_id <= 0:
            raise ValueError("Invalid technician account.")

        return IncidentRepository.get_assigned_to_technician(technician_id)

    @staticmethod
    def get_technician_incident_details(
        incident_id: int,
        technician_id: int,
    ):
        """Retrieve an incident assigned to a specific technician."""

        if not isinstance(incident_id, int) or incident_id <= 0:
            raise ValueError("Invalid incident selected.")

        if not isinstance(technician_id, int) or technician_id <= 0:
            raise ValueError("Invalid technician account.")

        return IncidentRepository.get_assigned_incident_details(
            incident_id=incident_id,
            technician_id=technician_id,
        )

    @staticmethod
    def get_unassigned_incidents():
        """Retrieve incidents available for technicians to claim."""
        return IncidentRepository.get_unassigned_incidents()

    @staticmethod
    def add_troubleshooting_record(
        incident_id: int,
        technician_id: int,
        action_taken: str,
    ):
        """Validate and save a technician's troubleshooting action."""

        if not isinstance(incident_id, int) or incident_id <= 0:
            raise ValueError("Invalid incident selected.")

        if not isinstance(technician_id, int) or technician_id <= 0:
            raise ValueError("Invalid technician account.")

        if not isinstance(action_taken, str) or not action_taken.strip():
            raise ValueError("Please describe the troubleshooting action.")

        action_taken = action_taken.strip()

        if len(action_taken) > 2000:
            raise ValueError("Troubleshooting notes cannot exceed 2000 characters.")

        return IncidentRepository.add_troubleshooting_record(
            incident_id=incident_id,
            technician_id=technician_id,
            action_taken=action_taken,
        )

    @staticmethod
    def get_troubleshooting_records(incident_id: int):
        """Retrieve troubleshooting history for an incident."""

        if not isinstance(incident_id, int) or incident_id <= 0:
            raise ValueError("Invalid incident selected.")

        return IncidentRepository.get_troubleshooting_records(incident_id)

    @staticmethod
    def get_resolution_history(incident_id: int):
        """Retrieve all resolution attempts and decisions for an incident."""

        if not isinstance(incident_id, int) or incident_id <= 0:
            raise ValueError("Invalid incident selected.")

        return IncidentRepository.get_resolution_history(incident_id)

    @staticmethod
    def submit_resolution(
        incident_id: int,
        technician_id: int,
        resolution_text: str,
    ):
        """Validate and submit a proposed incident resolution."""

        if not isinstance(incident_id, int) or incident_id <= 0:
            raise ValueError("Invalid incident selected.")

        if not isinstance(technician_id, int) or technician_id <= 0:
            raise ValueError("Invalid technician account.")

        if not isinstance(resolution_text, str) or not resolution_text.strip():
            raise ValueError("Please describe the proposed resolution.")

        resolution_text = resolution_text.strip()

        if len(resolution_text) > 2000:
            raise ValueError("The proposed resolution cannot exceed 2000 characters.")

        return IncidentRepository.submit_resolution(
            incident_id=incident_id,
            technician_id=technician_id,
            resolution_text=resolution_text,
        )

    @staticmethod
    def get_resolution_for_review(
        resolution_id: int,
        incident_id: int,
        user_id: int,
    ):
        """Retrieve a pending resolution for the intended user."""

        if any(
            not isinstance(value, int) or value <= 0
            for value in (resolution_id, incident_id, user_id)
        ):
            raise ValueError("Invalid resolution review request.")

        return IncidentRepository.get_resolution_for_review(
            resolution_id=resolution_id,
            incident_id=incident_id,
            user_id=user_id,
        )

    @staticmethod
    def submit_resolution_feedback(
        resolution_id: int,
        incident_id: int,
        user_id: int,
        decision: str,
        comments: str,
    ):
        """Validate and save the reporting user's decision."""

        if any(
            not isinstance(value, int) or value <= 0
            for value in (resolution_id, incident_id, user_id)
        ):
            raise ValueError("Invalid resolution review request.")

        if decision not in ("Accepted", "Rejected"):
            raise ValueError("Please select Accept or Reject.")

        if not isinstance(comments, str):
            raise ValueError("Invalid feedback.")

        comments = comments.strip()

        if decision == "Rejected" and not comments:
            raise ValueError("Please explain why you are rejecting this resolution.")

        if len(comments) > 1000:
            raise ValueError("Feedback cannot exceed 1000 characters.")

        return IncidentRepository.submit_resolution_feedback(
            resolution_id=resolution_id,
            incident_id=incident_id,
            user_id=user_id,
            decision=decision,
            comments=comments,
        )

    @staticmethod
    def get_latest_pending_resolution(
        incident_id: int,
        technician_id: int,
    ):
        """Retrieve the latest pending resolution for the technician."""

        if any(
            not isinstance(value, int) or value <= 0
            for value in (incident_id, technician_id)
        ):
            raise ValueError("Invalid resolution request.")

        return IncidentRepository.get_latest_pending_resolution(
            incident_id=incident_id,
            technician_id=technician_id,
        )

    @staticmethod
    def get_pending_resolution_for_resend(
        incident_id: int,
        technician_id: int,
        resolution_id: int,
    ):
        """Validate and retrieve an existing pending resolution for resending."""

        if any(
            not isinstance(value, int) or value <= 0
            for value in (incident_id, technician_id, resolution_id)
        ):
            raise ValueError("Invalid resolution notification request.")

        result = IncidentRepository.get_pending_resolution_for_resend(
            incident_id=incident_id,
            technician_id=technician_id,
            resolution_id=resolution_id,
        )

        if result is None:
            raise ValueError(
                "This resolution is not available for resending. "
                "It may already have been reviewed."
            )

        if not result["reporter_email"]:
            raise ValueError("The reporting user does not have an email address.")

        return result

    @staticmethod
    def record_resolution_email_resent(
        incident_id: int,
        technician_id: int,
        resolution_id: int,
    ):
        """Record a successfully resent resolution notification."""

        if any(
            not isinstance(value, int) or value <= 0
            for value in (incident_id, technician_id, resolution_id)
        ):
            raise ValueError("Invalid resolution notification request.")

        return IncidentRepository.record_resolution_email_resent(
            incident_id=incident_id,
            technician_id=technician_id,
            resolution_id=resolution_id,
        )
