from app.db.connection import get_connection


class SupervisorRepository:
    """Provides organisation-wide reporting data for supervisors."""

    @staticmethod
    def get_incident_statistics():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    COUNT(*) AS Total,
                    SUM(CASE WHEN Status = 'Open' THEN 1 ELSE 0 END) AS OpenCount,
                    SUM(CASE WHEN Status = 'In Progress' THEN 1 ELSE 0 END) AS InProgress,
                    SUM(CASE WHEN Status = 'Reopened' THEN 1 ELSE 0 END) AS Reopened,
                    SUM(
                        CASE
                            WHEN Status = 'Awaiting User Confirmation'
                            THEN 1 ELSE 0
                        END
                    ) AS AwaitingConfirmation,
                    SUM(CASE WHEN Status = 'Closed' THEN 1 ELSE 0 END) AS Closed,
                    SUM(
                        CASE
                            WHEN TechnicianId IS NULL
                             AND Status <> 'Closed'
                            THEN 1 ELSE 0
                        END
                    ) AS Unassigned
                FROM dbo.Incidents
            """)

            row = cursor.fetchone()

            return {
                "total": row.Total or 0,
                "open": row.OpenCount or 0,
                "in_progress": row.InProgress or 0,
                "reopened": row.Reopened or 0,
                "awaiting_confirmation": row.AwaitingConfirmation or 0,
                "closed": row.Closed or 0,
                "unassigned": row.Unassigned or 0,
            }

        finally:
            connection.close()

    @staticmethod
    def get_resolution_statistics():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    COUNT(r.ResolutionId) AS Total,
                    SUM(
                        CASE WHEN f.Decision = 'Accepted'
                        THEN 1 ELSE 0 END
                    ) AS Accepted,
                    SUM(
                        CASE WHEN f.Decision = 'Rejected'
                        THEN 1 ELSE 0 END
                    ) AS Rejected,
                    SUM(
                        CASE WHEN f.FeedbackId IS NULL
                        THEN 1 ELSE 0 END
                    ) AS Pending
                FROM dbo.Resolutions AS r
                LEFT JOIN dbo.UserFeedback AS f
                    ON r.ResolutionId = f.ResolutionId
            """)

            row = cursor.fetchone()

            return {
                "total": row.Total or 0,
                "accepted": row.Accepted or 0,
                "rejected": row.Rejected or 0,
                "pending": row.Pending or 0,
            }

        finally:
            connection.close()

    @staticmethod
    def get_technician_workloads():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    u.UserId,
                    u.FullName,
                    u.IsActive,

                    COUNT(i.IncidentId) AS TotalAssigned,

                    SUM(
                        CASE
                            WHEN i.Status IS NOT NULL
                             AND i.Status <> 'Closed'
                            THEN 1 ELSE 0
                        END
                    ) AS Outstanding,

                    SUM(
                        CASE
                            WHEN i.Status = 'In Progress'
                            THEN 1 ELSE 0
                        END
                    ) AS InProgress,

                    SUM(
                        CASE
                            WHEN i.Status = 'Awaiting User Confirmation'
                            THEN 1 ELSE 0
                        END
                    ) AS AwaitingConfirmation,

                    SUM(
                        CASE
                            WHEN i.Status = 'Reopened'
                            THEN 1 ELSE 0
                        END
                    ) AS Reopened

                FROM dbo.Users AS u

                LEFT JOIN dbo.Incidents AS i
                    ON u.UserId = i.TechnicianId

                WHERE u.Role = 'Technician'

                GROUP BY
                    u.UserId,
                    u.FullName,
                    u.IsActive

                ORDER BY
                    Outstanding DESC,
                    u.FullName ASC
            """)

            rows = cursor.fetchall()

            return [
                {
                    "user_id": row.UserId,
                    "full_name": row.FullName,
                    "is_active": bool(row.IsActive),
                    "total_assigned": row.TotalAssigned or 0,
                    "outstanding": row.Outstanding or 0,
                    "in_progress": row.InProgress or 0,
                    "awaiting_confirmation": row.AwaitingConfirmation or 0,
                    "reopened": row.Reopened or 0,
                }
                for row in rows
            ]

        finally:
            connection.close()

    @staticmethod
    def get_recent_incidents(limit=10):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT TOP (?)
                    i.IncidentId,
                    i.IncidentReference,
                    i.Title,
                    i.Priority,
                    i.Status,
                    i.CreatedAt,
                    c.Name AS CategoryName,
                    reporter.FullName AS ReporterName,
                    technician.FullName AS TechnicianName

                FROM dbo.Incidents AS i

                INNER JOIN dbo.Categories AS c
                    ON i.CategoryId = c.CategoryId

                INNER JOIN dbo.Users AS reporter
                    ON i.UserId = reporter.UserId

                LEFT JOIN dbo.Users AS technician
                    ON i.TechnicianId = technician.UserId

                ORDER BY i.CreatedAt DESC, i.IncidentId DESC
                """,
                (limit,),
            )

            rows = cursor.fetchall()

            return [
                {
                    "incident_id": row.IncidentId,
                    "reference": row.IncidentReference,
                    "title": row.Title,
                    "priority": row.Priority,
                    "status": row.Status,
                    "created_at": row.CreatedAt,
                    "category": row.CategoryName,
                    "reporter": row.ReporterName,
                    "technician": row.TechnicianName or "Unassigned",
                }
                for row in rows
            ]

        finally:
            connection.close()

    @staticmethod
    def get_recent_activity(limit=12):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT TOP (?)
                    a.AuditLogId,
                    a.Action,
                    a.FromStatus,
                    a.ToStatus,
                    a.Details,
                    a.CreatedAt,
                    u.FullName AS PerformedBy,
                    i.IncidentReference

                FROM dbo.AuditLogs AS a

                LEFT JOIN dbo.Users AS u
                    ON a.UserId = u.UserId

                LEFT JOIN dbo.Incidents AS i
                    ON a.IncidentId = i.IncidentId

                ORDER BY a.CreatedAt DESC, a.AuditLogId DESC
                """,
                (limit,),
            )

            rows = cursor.fetchall()

            return [
                {
                    "audit_log_id": row.AuditLogId,
                    "action": row.Action,
                    "from_status": row.FromStatus,
                    "to_status": row.ToStatus,
                    "details": row.Details,
                    "created_at": row.CreatedAt,
                    "performed_by": row.PerformedBy or "System",
                    "incident_reference": row.IncidentReference or "Account/System",
                }
                for row in rows
            ]

        finally:
            connection.close()
