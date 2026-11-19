class DashboardService:
    """Provides dashboard configuration based on user roles."""

    DASHBOARDS = {
        "User": {
            "title": "My Support Dashboard",
            "description": "Report incidents and track their progress.",
        },
        "Technician": {
            "title": "Technician Workspace",
            "description": "Investigate and resolve assigned incidents.",
        },
        "Administrator": {
            "title": "Administration Dashboard",
            "description": "Manage users and incident assignments.",
        },
        "Supervisor": {
            "title": "Supervisor Dashboard",
            "description": "Monitor incidents and review reports.",
        },
    }

    @staticmethod
    def get_dashboard(role: str):
        return DashboardService.DASHBOARDS.get(role)
