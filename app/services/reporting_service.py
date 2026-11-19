from datetime import date, timedelta

from app.repositories.reporting_repository import ReportingRepository


class ReportingService:
    """Prepares reporting and analytics data for supervisors."""

    PRESETS = {
        "today": "Today",
        "7": "Last 7 Days",
        "30": "Last 30 Days",
        "90": "Last 90 Days",
        "custom": "Custom Range",
    }

    @staticmethod
    def get_reporting_data(start_date=None, end_date=None, period="30"):

        today = date.today()

        # Determine the reporting period.
        if period == "today":
            start_date = today
            end_date = today

        elif period in ("7", "30", "90"):
            days = int(period)
            end_date = today
            start_date = today - timedelta(days=days - 1)

        elif period == "custom":
            if not start_date or not end_date:
                raise ValueError(
                    "Both start and end dates are required for a custom range."
                )

            if start_date > end_date:
                raise ValueError("The start date cannot be after the end date.")

            if end_date > today:
                raise ValueError("The end date cannot be in the future.")

        else:
            period = "30"
            end_date = today
            start_date = today - timedelta(days=29)

        # Retrieve reporting data.
        total_incidents = ReportingRepository.get_total_incidents()

        trends = ReportingRepository.get_incident_trends(
            start_date,
            end_date,
        )

        categories = ReportingRepository.get_category_breakdown(
            start_date,
            end_date,
        )

        priorities = ReportingRepository.get_priority_breakdown(
            start_date,
            end_date,
        )

        technicians = ReportingRepository.get_technician_performance(
            start_date,
            end_date,
        )

        resolutions = ReportingRepository.get_resolution_performance(
            start_date,
            end_date,
        )

        resolution_time = ReportingRepository.get_average_resolution_time(
            start_date,
            end_date,
        )

        # Calculate incidents within the selected period.
        incidents_in_period = sum(item["count"] for item in categories)

        # Calculate category percentages.
        category_percentages = []

        for item in categories:
            percentage = (
                round(
                    (item["count"] / incidents_in_period) * 100,
                    1,
                )
                if incidents_in_period > 0
                else 0
            )

            category_percentages.append(
                {
                    **item,
                    "percentage": percentage,
                }
            )

        # Calculate priority percentages.
        priority_percentages = []

        for item in priorities:
            percentage = (
                round(
                    (item["count"] / incidents_in_period) * 100,
                    1,
                )
                if incidents_in_period > 0
                else 0
            )

            priority_percentages.append(
                {
                    **item,
                    "percentage": percentage,
                }
            )

        # Format trend dates for the chart.
        for item in trends:
            item["date_label"] = item["date"].strftime("%d %b %Y")

        # Calculate technician closed shares.
        for item in technicians:
            closed = item["closed"]
            assigned = item["total_assigned"]

            item["completion_rate"] = (
                round((closed / assigned) * 100, 1) if assigned > 0 else 0
            )

        return {
            "summary": {
                "total_incidents": total_incidents,
                "incidents_in_period": incidents_in_period,
                "average_resolution_hours": resolution_time["average_hours"],
                "closed_incidents_used_for_average": resolution_time["closed_count"],
            },
            "filters": {
                "period": period,
                "period_label": ReportingService.PRESETS[period],
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
            "incident_trends": trends,
            "category_breakdown": category_percentages,
            "priority_breakdown": priority_percentages,
            "technician_performance": technicians,
            "resolution_performance": resolutions,
            "resolution_time": resolution_time,
        }
