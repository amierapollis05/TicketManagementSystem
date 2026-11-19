from app.repositories.supervisor_repository import SupervisorRepository


class SupervisorService:
    """Combines organisation-wide reporting data for the supervisor dashboard."""

    @staticmethod
    def get_dashboard_data():
        incident_statistics = SupervisorRepository.get_incident_statistics()
        resolution_statistics = SupervisorRepository.get_resolution_statistics()
        technician_workloads = SupervisorRepository.get_technician_workloads()
        recent_incidents = SupervisorRepository.get_recent_incidents(limit=10)
        recent_activity = SupervisorRepository.get_recent_activity(limit=12)

        accepted = resolution_statistics["accepted"]
        rejected = resolution_statistics["rejected"]
        reviewed = accepted + rejected

        acceptance_rate = round((accepted / reviewed) * 100, 1) if reviewed > 0 else 0

        return {
            "incident_statistics": incident_statistics,
            "resolution_statistics": resolution_statistics,
            "technician_workloads": technician_workloads,
            "recent_incidents": recent_incidents,
            "recent_activity": recent_activity,
            "acceptance_rate": acceptance_rate,
        }
