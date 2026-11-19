from app.db.connection import get_connection


class ReportingRepository:
    """Retrieves organisation-wide reporting and analytics data."""

    @staticmethod
    def get_total_incidents():
        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT COUNT(*) AS Total
                FROM dbo.Incidents
            """)

            return cursor.fetchone().Total or 0

        finally:
            connection.close()

    @staticmethod
    def get_incident_trends(start_date, end_date):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    CAST(CreatedAt AS DATE) AS ReportDate,
                    COUNT(*) AS IncidentCount
                FROM dbo.Incidents
                WHERE CreatedAt >= ?
                  AND CreatedAt < DATEADD(DAY, 1, ?)
                GROUP BY CAST(CreatedAt AS DATE)
                ORDER BY ReportDate ASC
            """,
                (start_date, end_date),
            )

            return [
                {
                    "date": row.ReportDate,
                    "count": row.IncidentCount,
                }
                for row in cursor.fetchall()
            ]

        finally:
            connection.close()

    @staticmethod
    def get_category_breakdown(start_date, end_date):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    c.CategoryId,
                    c.Name AS CategoryName,
                    COUNT(i.IncidentId) AS IncidentCount
                FROM dbo.Categories AS c

                LEFT JOIN dbo.Incidents AS i
                    ON c.CategoryId = i.CategoryId
                    AND i.CreatedAt >= ?
                    AND i.CreatedAt < DATEADD(DAY, 1, ?)

                GROUP BY c.CategoryId, c.Name
                ORDER BY IncidentCount DESC, c.Name ASC
            """,
                (start_date, end_date),
            )

            return [
                {
                    "category_id": row.CategoryId,
                    "category": row.CategoryName,
                    "count": row.IncidentCount,
                }
                for row in cursor.fetchall()
            ]

        finally:
            connection.close()

    @staticmethod
    def get_priority_breakdown(start_date, end_date):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    Priority,
                    COUNT(*) AS IncidentCount
                FROM dbo.Incidents
                WHERE CreatedAt >= ?
                  AND CreatedAt < DATEADD(DAY, 1, ?)
                GROUP BY Priority
                ORDER BY
                    CASE Priority
                        WHEN 'High' THEN 1
                        WHEN 'Medium' THEN 2
                        WHEN 'Low' THEN 3
                        ELSE 4
                    END
            """,
                (start_date, end_date),
            )

            return [
                {
                    "priority": row.Priority,
                    "count": row.IncidentCount,
                }
                for row in cursor.fetchall()
            ]

        finally:
            connection.close()

    @staticmethod
    def get_technician_performance(start_date, end_date):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    u.UserId,
                    u.FullName,
                    u.IsActive,

                    COUNT(i.IncidentId) AS TotalAssigned,

                    SUM(
                        CASE
                            WHEN i.Status = 'Closed'
                            THEN 1 ELSE 0
                        END
                    ) AS ClosedIncidents,

                    SUM(
                        CASE
                            WHEN i.IncidentId IS NOT NULL
                             AND i.Status <> 'Closed'
                            THEN 1 ELSE 0
                        END
                    ) AS Outstanding,

                    AVG(
                        CASE
                            WHEN i.Status = 'Closed'
                             AND i.ClosedAt IS NOT NULL
                             AND i.ClosedAt >= i.CreatedAt
                            THEN CAST(
                                DATEDIFF(
                                    MINUTE,
                                    i.CreatedAt,
                                    i.ClosedAt
                                ) AS FLOAT
                            ) / 60.0
                            ELSE NULL
                        END
                    ) AS AverageResolutionHours

                FROM dbo.Users AS u

                LEFT JOIN dbo.Incidents AS i
                    ON u.UserId = i.TechnicianId
                    AND i.CreatedAt >= ?
                    AND i.CreatedAt < DATEADD(DAY, 1, ?)

                WHERE u.Role = 'Technician'

                GROUP BY
                    u.UserId,
                    u.FullName,
                    u.IsActive

                ORDER BY
                    ClosedIncidents DESC,
                    u.FullName ASC
            """,
                (start_date, end_date),
            )

            return [
                {
                    "user_id": row.UserId,
                    "technician": row.FullName,
                    "is_active": bool(row.IsActive),
                    "total_assigned": row.TotalAssigned or 0,
                    "closed": row.ClosedIncidents or 0,
                    "outstanding": row.Outstanding or 0,
                    "average_resolution_hours": (
                        round(row.AverageResolutionHours, 2)
                        if row.AverageResolutionHours is not None
                        else None
                    ),
                }
                for row in cursor.fetchall()
            ]

        finally:
            connection.close()

    @staticmethod
    def get_resolution_performance(start_date, end_date):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    COUNT(r.ResolutionId) AS Total,

                    SUM(
                        CASE
                            WHEN f.Decision = 'Accepted'
                            THEN 1 ELSE 0
                        END
                    ) AS Accepted,

                    SUM(
                        CASE
                            WHEN f.Decision = 'Rejected'
                            THEN 1 ELSE 0
                        END
                    ) AS Rejected,

                    SUM(
                        CASE
                            WHEN f.FeedbackId IS NULL
                            THEN 1 ELSE 0
                        END
                    ) AS Pending

                FROM dbo.Resolutions AS r

                LEFT JOIN dbo.UserFeedback AS f
                    ON r.ResolutionId = f.ResolutionId

                WHERE r.SubmittedAt >= ?
                  AND r.SubmittedAt < DATEADD(DAY, 1, ?)
            """,
                (start_date, end_date),
            )

            row = cursor.fetchone()

            accepted = row.Accepted or 0
            rejected = row.Rejected or 0
            reviewed = accepted + rejected

            return {
                "total": row.Total or 0,
                "accepted": accepted,
                "rejected": rejected,
                "pending": row.Pending or 0,
                "acceptance_rate": (
                    round((accepted / reviewed) * 100, 1) if reviewed else 0
                ),
            }

        finally:
            connection.close()

    @staticmethod
    def get_average_resolution_time(start_date, end_date):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    COUNT(*) AS ClosedCount,

                    AVG(
                        CAST(
                            DATEDIFF(
                                MINUTE,
                                CreatedAt,
                                ClosedAt
                            ) AS FLOAT
                        )
                    ) AS AverageMinutes

                FROM dbo.Incidents

                WHERE Status = 'Closed'
                  AND ClosedAt IS NOT NULL
                  AND ClosedAt >= CreatedAt
                  AND ClosedAt >= ?
                  AND ClosedAt < DATEADD(DAY, 1, ?)
            """,
                (start_date, end_date),
            )

            row = cursor.fetchone()

            average_minutes = row.AverageMinutes

            return {
                "closed_count": row.ClosedCount or 0,
                "average_minutes": (
                    round(average_minutes, 2) if average_minutes is not None else None
                ),
                "average_hours": (
                    round(average_minutes / 60, 2)
                    if average_minutes is not None
                    else None
                ),
            }

        finally:
            connection.close()
