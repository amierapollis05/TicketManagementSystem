from app.db.connection import get_connection


class IncidentRepository:
    """Handles database operations for incidents."""

    @staticmethod
    def get_categories():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT CategoryId, Name, Description
                FROM dbo.Categories
                ORDER BY Name
            """)

            rows = cursor.fetchall()

            return [
                {
                    "category_id": row.CategoryId,
                    "name": row.Name,
                    "description": row.Description,
                }
                for row in rows
            ]

        finally:
            connection.close()

    @staticmethod
    def create_incident(
        incident_reference: str,
        user_id: int,
        category_id: int,
        title: str,
        description: str,
        priority: str,
    ):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO dbo.Incidents (
                    IncidentReference,
                    UserId,
                    CategoryId,
                    Title,
                    Description,
                    Priority,
                    Status
                )
                OUTPUT INSERTED.IncidentId
                VALUES (?, ?, ?, ?, ?, ?, 'Open')
                """,
                (
                    incident_reference,
                    user_id,
                    category_id,
                    title,
                    description,
                    priority,
                ),
            )

            incident_id = cursor.fetchone()[0]

            connection.commit()

            return incident_id

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def get_by_reference(incident_reference: str):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    i.IncidentId,
                    i.IncidentReference,
                    i.UserId,
                    i.TechnicianId,
                    i.CategoryId,
                    c.Name AS CategoryName,
                    i.Title,
                    i.Description,
                    i.Priority,
                    i.Status,
                    i.CreatedAt,
                    i.ClosedAt
                FROM dbo.Incidents AS i
                INNER JOIN dbo.Categories AS c
                    ON i.CategoryId = c.CategoryId
                WHERE i.IncidentReference = ?
                """,
                (incident_reference,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "incident_id": row.IncidentId,
                "incident_reference": row.IncidentReference,
                "user_id": row.UserId,
                "technician_id": row.TechnicianId,
                "category_id": row.CategoryId,
                "category_name": row.CategoryName,
                "title": row.Title,
                "description": row.Description,
                "priority": row.Priority,
                "status": row.Status,
                "created_at": row.CreatedAt,
                "closed_at": row.ClosedAt,
            }

        finally:
            connection.close()

    @staticmethod
    def get_by_user(user_id: int):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    i.IncidentId,
                    i.IncidentReference,
                    i.Title,
                    c.Name AS CategoryName,
                    i.Priority,
                    i.Status,
                    i.CreatedAt
                FROM dbo.Incidents AS i
                INNER JOIN dbo.Categories AS c
                    ON i.CategoryId = c.CategoryId
                WHERE i.UserId = ?
                ORDER BY i.CreatedAt DESC
                """,
                (user_id,),
            )

            rows = cursor.fetchall()

            return [
                {
                    "incident_id": row.IncidentId,
                    "incident_reference": row.IncidentReference,
                    "title": row.Title,
                    "category_name": row.CategoryName,
                    "priority": row.Priority,
                    "status": row.Status,
                    "created_at": row.CreatedAt,
                }
                for row in rows
            ]

        finally:
            connection.close()

    @staticmethod
    def get_all():
        """Retrieve all incidents for administrative management."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    i.IncidentId,
                    i.IncidentReference,
                    i.Title,
                    i.Priority,
                    i.Status,
                    i.CreatedAt,
                    i.TechnicianId,
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
                ORDER BY
                    CASE
                        WHEN i.Status = 'Open' THEN 1
                        WHEN i.Status = 'Reopened' THEN 2
                        WHEN i.Status = 'In Progress' THEN 3
                        WHEN i.Status = 'Awaiting User Confirmation' THEN 4
                        ELSE 5
                    END,
                    i.CreatedAt DESC
            """)

            rows = cursor.fetchall()

            return [
                {
                    "incident_id": row.IncidentId,
                    "incident_reference": row.IncidentReference,
                    "title": row.Title,
                    "priority": row.Priority,
                    "status": row.Status,
                    "created_at": row.CreatedAt,
                    "technician_id": row.TechnicianId,
                    "category_name": row.CategoryName,
                    "reporter_name": row.ReporterName,
                    "technician_name": row.TechnicianName,
                }
                for row in rows
            ]

        finally:
            connection.close()

    @staticmethod
    def assign_technician(
        incident_id: int,
        technician_id: int,
        assigned_by_user_id: int,
    ):
        """Assign or reassign a technician and record the action."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT Status, TechnicianId
                FROM dbo.Incidents WITH (UPDLOCK, HOLDLOCK)
                WHERE IncidentId = ?
                """,
                (incident_id,),
            )

            incident = cursor.fetchone()

            if incident is None:
                raise ValueError("The selected incident does not exist.")

            current_status = incident.Status
            previous_technician_id = incident.TechnicianId

            if current_status == "Closed":
                raise ValueError("Closed incidents cannot be assigned.")

            cursor.execute(
                """
                SELECT FullName
                FROM dbo.Users
                WHERE UserId = ?
                  AND Role = 'Technician'
                  AND IsActive = 1
                """,
                (technician_id,),
            )

            technician = cursor.fetchone()

            if technician is None:
                raise ValueError("The selected technician is invalid or inactive.")

            technician_name = technician.FullName

            if previous_technician_id == technician_id:
                raise ValueError("This technician is already assigned to the incident.")

            previous_technician_name = None

            if previous_technician_id is not None:
                cursor.execute(
                    """
                    SELECT FullName
                    FROM dbo.Users
                    WHERE UserId = ?
                    """,
                    (previous_technician_id,),
                )

                previous_technician = cursor.fetchone()

                if previous_technician:
                    previous_technician_name = previous_technician.FullName

            new_status = current_status

            if current_status in ("Open", "Reopened"):
                new_status = "In Progress"

            cursor.execute(
                """
                UPDATE dbo.Incidents
                SET
                    TechnicianId = ?,
                    Status = ?
                WHERE IncidentId = ?
                """,
                (
                    technician_id,
                    new_status,
                    incident_id,
                ),
            )

            action = (
                "Technician Assigned"
                if previous_technician_id is None
                else "Technician Reassigned"
            )

            if previous_technician_id is None:
                details = (
                    f"Assigned technician: {technician_name} "
                    f"(UserId: {technician_id})."
                )
            else:
                details = (
                    f"Reassigned from {previous_technician_name or 'Unknown'} "
                    f"(UserId: {previous_technician_id}) to "
                    f"{technician_name} (UserId: {technician_id})."
                )

            cursor.execute(
                """
                INSERT INTO dbo.AuditLogs (
                    IncidentId,
                    UserId,
                    Action,
                    FromStatus,
                    ToStatus,
                    Details
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    incident_id,
                    assigned_by_user_id,
                    action,
                    current_status,
                    new_status,
                    details,
                ),
            )

            connection.commit()

            return {
                "incident_id": incident_id,
                "technician_id": technician_id,
                "technician_name": technician_name,
                "previous_status": current_status,
                "new_status": new_status,
                "action": action,
            }

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def get_assigned_to_technician(technician_id: int):
        """Retrieve all incidents assigned to a specific technician."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    i.IncidentId,
                    i.IncidentReference,
                    i.Title,
                    i.Priority,
                    i.Status,
                    i.CreatedAt,
                    c.Name AS CategoryName,
                    reporter.FullName AS ReporterName,
                    reporter.Email AS ReporterEmail
                FROM dbo.Incidents AS i
                INNER JOIN dbo.Categories AS c
                    ON i.CategoryId = c.CategoryId
                INNER JOIN dbo.Users AS reporter
                    ON i.UserId = reporter.UserId
                WHERE i.TechnicianId = ?
                ORDER BY
                    CASE
                        WHEN i.Status = 'Reopened' THEN 1
                        WHEN i.Status = 'In Progress' THEN 2
                        WHEN i.Status = 'Awaiting User Confirmation' THEN 3
                        WHEN i.Status = 'Open' THEN 4
                        ELSE 5
                    END,
                    CASE
                        WHEN i.Priority = 'High' THEN 1
                        WHEN i.Priority = 'Medium' THEN 2
                        ELSE 3
                    END,
                    i.CreatedAt ASC
                """,
                (technician_id,),
            )

            rows = cursor.fetchall()

            return [
                {
                    "incident_id": row.IncidentId,
                    "incident_reference": row.IncidentReference,
                    "title": row.Title,
                    "priority": row.Priority,
                    "status": row.Status,
                    "created_at": row.CreatedAt,
                    "category_name": row.CategoryName,
                    "reporter_name": row.ReporterName,
                    "reporter_email": row.ReporterEmail,
                }
                for row in rows
            ]

        finally:
            connection.close()

    @staticmethod
    def get_assigned_incident_details(
        incident_id: int,
        technician_id: int,
    ):
        """Retrieve incident details only if assigned to this technician."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    i.IncidentId,
                    i.IncidentReference,
                    i.UserId,
                    i.TechnicianId,
                    i.Title,
                    i.Description,
                    i.Priority,
                    i.Status,
                    i.CreatedAt,
                    i.ClosedAt,
                    c.Name AS CategoryName,
                    reporter.FullName AS ReporterName,
                    reporter.Email AS ReporterEmail
                FROM dbo.Incidents AS i
                INNER JOIN dbo.Categories AS c
                    ON i.CategoryId = c.CategoryId
                INNER JOIN dbo.Users AS reporter
                    ON i.UserId = reporter.UserId
                WHERE i.IncidentId = ?
                  AND i.TechnicianId = ?
                """,
                (incident_id, technician_id),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "incident_id": row.IncidentId,
                "incident_reference": row.IncidentReference,
                "user_id": row.UserId,
                "technician_id": row.TechnicianId,
                "title": row.Title,
                "description": row.Description,
                "priority": row.Priority,
                "status": row.Status,
                "created_at": row.CreatedAt,
                "closed_at": row.ClosedAt,
                "category_name": row.CategoryName,
                "reporter_name": row.ReporterName,
                "reporter_email": row.ReporterEmail,
            }

        finally:
            connection.close()

    @staticmethod
    def add_troubleshooting_record(
        incident_id: int,
        technician_id: int,
        action_taken: str,
    ):
        """Save a troubleshooting action and record it in the audit log."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT Status
                FROM dbo.Incidents WITH (UPDLOCK, HOLDLOCK)
                WHERE IncidentId = ?
                  AND TechnicianId = ?
                """,
                (incident_id, technician_id),
            )

            incident = cursor.fetchone()

            if incident is None:
                raise ValueError(
                    "This incident does not exist or is not assigned to you."
                )

            if incident.Status not in ("In Progress", "Reopened"):
                raise ValueError(
                    "Troubleshooting records can only be added "
                    "to incidents that are in progress."
                )

            cursor.execute(
                """
                INSERT INTO dbo.TroubleshootingRecords (
                    IncidentId,
                    TechnicianId,
                    ActionTaken,
                    CreatedAt
                )
                OUTPUT INSERTED.RecordId
                VALUES (?, ?, ?, SYSUTCDATETIME())
                """,
                (incident_id, technician_id, action_taken),
            )

            record = cursor.fetchone()
            record_id = record.RecordId

            cursor.execute(
                """
                INSERT INTO dbo.AuditLogs (
                    IncidentId,
                    UserId,
                    Action,
                    FromStatus,
                    ToStatus,
                    Details
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    incident_id,
                    technician_id,
                    "Troubleshooting Recorded",
                    incident.Status,
                    incident.Status,
                    "A troubleshooting action was recorded.",
                ),
            )

            connection.commit()

            return record_id

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def get_troubleshooting_records(incident_id: int):
        """Retrieve the investigation history for an incident."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    tr.RecordId,
                    tr.IncidentId,
                    tr.TechnicianId,
                    tr.ActionTaken,
                    tr.CreatedAt,
                    u.FullName AS TechnicianName
                FROM dbo.TroubleshootingRecords AS tr
                INNER JOIN dbo.Users AS u
                    ON tr.TechnicianId = u.UserId
                WHERE tr.IncidentId = ?
                ORDER BY tr.CreatedAt ASC, tr.RecordId ASC
                """,
                (incident_id,),
            )

            rows = cursor.fetchall()

            return [
                {
                    "record_id": row.RecordId,
                    "incident_id": row.IncidentId,
                    "technician_id": row.TechnicianId,
                    "action_taken": row.ActionTaken,
                    "created_at": row.CreatedAt,
                    "technician_name": row.TechnicianName,
                }
                for row in rows
            ]

        finally:
            connection.close()

    @staticmethod
    def submit_resolution(
        incident_id: int,
        technician_id: int,
        resolution_text: str,
    ):
        """Save a proposed resolution and move the incident to confirmation."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    i.Status,
                    i.IncidentReference,
                    i.Title,
                    i.UserId,
                    reporter.FullName AS ReporterName,
                    reporter.Email AS ReporterEmail
                FROM dbo.Incidents AS i WITH (UPDLOCK, HOLDLOCK)
                INNER JOIN dbo.Users AS reporter
                    ON i.UserId = reporter.UserId
                WHERE i.IncidentId = ?
                  AND i.TechnicianId = ?
                """,
                (incident_id, technician_id),
            )

            incident = cursor.fetchone()

            if incident is None:
                raise ValueError(
                    "This incident does not exist or is not assigned to you."
                )

            if incident.Status not in ("In Progress", "Reopened"):
                raise ValueError(
                    "A resolution can only be submitted for an incident "
                    "that is In Progress or Reopened."
                )

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM dbo.TroubleshootingRecords
                WHERE IncidentId = ?
                """,
                (incident_id,),
            )

            troubleshooting_count = cursor.fetchone()[0]

            if troubleshooting_count == 0:
                raise ValueError(
                    "Record at least one troubleshooting action "
                    "before submitting a resolution."
                )

            cursor.execute(
                """
                INSERT INTO dbo.Resolutions (
                    IncidentId,
                    TechnicianId,
                    ResolutionText,
                    SubmittedAt
                )
                OUTPUT INSERTED.ResolutionId
                VALUES (?, ?, ?, SYSUTCDATETIME())
                """,
                (incident_id, technician_id, resolution_text),
            )

            resolution_id = cursor.fetchone().ResolutionId

            cursor.execute(
                """
                UPDATE dbo.Incidents
                SET
                    Status = 'Awaiting User Confirmation',
                    ClosedAt = NULL
                WHERE IncidentId = ?
                """,
                (incident_id,),
            )

            cursor.execute(
                """
                INSERT INTO dbo.AuditLogs (
                    IncidentId,
                    UserId,
                    Action,
                    FromStatus,
                    ToStatus,
                    Details
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    incident_id,
                    technician_id,
                    "Resolution Submitted",
                    incident.Status,
                    "Awaiting User Confirmation",
                    f"Resolution {resolution_id} submitted for user confirmation.",
                ),
            )

            connection.commit()

            return {
                "resolution_id": resolution_id,
                "incident_id": incident_id,
                "incident_reference": incident.IncidentReference,
                "incident_title": incident.Title,
                "user_id": incident.UserId,
                "reporter_name": incident.ReporterName,
                "reporter_email": incident.ReporterEmail,
                "resolution_text": resolution_text,
            }

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def get_resolution_for_review(
        resolution_id: int,
        incident_id: int,
        user_id: int,
    ):
        """Retrieve a pending resolution for its reporting user."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    r.ResolutionId,
                    r.IncidentId,
                    r.TechnicianId,
                    r.ResolutionText,
                    r.SubmittedAt,
                    i.IncidentReference,
                    i.Title,
                    i.Status,
                    u.FullName AS ReporterName
                FROM dbo.Resolutions AS r
                INNER JOIN dbo.Incidents AS i
                    ON r.IncidentId = i.IncidentId
                INNER JOIN dbo.Users AS u
                    ON i.UserId = u.UserId
                WHERE r.ResolutionId = ?
                  AND r.IncidentId = ?
                  AND i.UserId = ?
                  AND i.Status = 'Awaiting User Confirmation'
                  AND NOT EXISTS (
                      SELECT 1
                      FROM dbo.UserFeedback AS f
                      WHERE f.ResolutionId = r.ResolutionId
                  )
                """,
                (resolution_id, incident_id, user_id),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "resolution_id": row.ResolutionId,
                "incident_id": row.IncidentId,
                "technician_id": row.TechnicianId,
                "resolution_text": row.ResolutionText,
                "submitted_at": row.SubmittedAt,
                "incident_reference": row.IncidentReference,
                "incident_title": row.Title,
                "status": row.Status,
                "reporter_name": row.ReporterName,
            }

        finally:
            connection.close()

    @staticmethod
    def submit_resolution_feedback(
        resolution_id: int,
        incident_id: int,
        user_id: int,
        decision: str,
        comments: str,
    ):
        """Record the user's decision and update the incident."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    i.Status,
                    i.IncidentReference
                FROM dbo.Incidents AS i WITH (UPDLOCK, HOLDLOCK)
                INNER JOIN dbo.Resolutions AS r
                    ON i.IncidentId = r.IncidentId
                WHERE i.IncidentId = ?
                  AND r.ResolutionId = ?
                  AND i.UserId = ?
                """,
                (incident_id, resolution_id, user_id),
            )

            incident = cursor.fetchone()

            if incident is None:
                raise ValueError("This resolution could not be found.")

            if incident.Status != "Awaiting User Confirmation":
                raise ValueError("This incident is no longer awaiting confirmation.")

            if decision not in ("Accepted", "Rejected"):
                raise ValueError("Please select a valid decision.")

            if decision == "Rejected" and not comments.strip():
                raise ValueError(
                    "You must provide a reason when rejecting a resolution."
                )

            if len(comments) > 1000:
                raise ValueError("Feedback cannot exceed 1000 characters.")

            cursor.execute(
                """
                INSERT INTO dbo.UserFeedback (
                    IncidentId,
                    ResolutionId,
                    UserId,
                    Decision,
                    Comments,
                    SubmittedAt
                )
                VALUES (?, ?, ?, ?, ?, SYSUTCDATETIME())
                """,
                (
                    incident_id,
                    resolution_id,
                    user_id,
                    decision,
                    comments.strip() or None,
                ),
            )

            new_status = "Closed" if decision == "Accepted" else "Reopened"

            cursor.execute(
                """
                UPDATE dbo.Incidents
                SET
                    Status = ?,
                    ClosedAt = CASE
                        WHEN ? = 'Closed' THEN SYSUTCDATETIME()
                        ELSE NULL
                    END
                WHERE IncidentId = ?
                """,
                (new_status, new_status, incident_id),
            )

            action = (
                "Resolution Accepted"
                if decision == "Accepted"
                else "Resolution Rejected"
            )

            details = f"User {decision.lower()} the proposed resolution."

            cursor.execute(
                """
                INSERT INTO dbo.AuditLogs (
                    IncidentId,
                    UserId,
                    Action,
                    FromStatus,
                    ToStatus,
                    Details
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    incident_id,
                    user_id,
                    action,
                    incident.Status,
                    new_status,
                    details,
                ),
            )

            connection.commit()

            return {
                "incident_id": incident_id,
                "incident_reference": incident.IncidentReference,
                "decision": decision,
                "new_status": new_status,
            }

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def get_latest_pending_resolution(
        incident_id: int,
        technician_id: int,
    ):
        """Retrieve the latest unreviewed resolution for an assigned incident."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT TOP 1
                    r.ResolutionId,
                    r.IncidentId,
                    r.TechnicianId,
                    r.SubmittedAt
                FROM dbo.Resolutions AS r
                INNER JOIN dbo.Incidents AS i
                    ON r.IncidentId = i.IncidentId
                WHERE i.IncidentId = ?
                  AND i.TechnicianId = ?
                  AND r.TechnicianId = ?
                  AND i.Status = 'Awaiting User Confirmation'
                  AND NOT EXISTS (
                      SELECT 1
                      FROM dbo.UserFeedback AS f
                      WHERE f.ResolutionId = r.ResolutionId
                  )
                ORDER BY r.SubmittedAt DESC, r.ResolutionId DESC
                """,
                (incident_id, technician_id, technician_id),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "resolution_id": row.ResolutionId,
                "incident_id": row.IncidentId,
                "technician_id": row.TechnicianId,
                "submitted_at": row.SubmittedAt,
            }

        finally:
            connection.close()

    @staticmethod
    def get_pending_resolution_for_resend(
        incident_id: int,
        technician_id: int,
        resolution_id: int,
    ):
        """
        Retrieve an existing pending resolution for its assigned technician.

        The resolution must belong to the incident, the incident must
        still be assigned to this technician, and the user must not
        have already accepted or rejected the resolution.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    r.ResolutionId,
                    r.IncidentId,
                    r.ResolutionText,
                    i.IncidentReference,
                    i.Title AS IncidentTitle,
                    i.UserId,
                    reporter.FullName AS ReporterName,
                    reporter.Email AS ReporterEmail
                FROM dbo.Resolutions AS r
                INNER JOIN dbo.Incidents AS i
                    ON r.IncidentId = i.IncidentId
                INNER JOIN dbo.Users AS reporter
                    ON i.UserId = reporter.UserId
                WHERE r.ResolutionId = ?
                  AND r.IncidentId = ?
                  AND i.TechnicianId = ?
                  AND i.Status = 'Awaiting User Confirmation'
                  AND NOT EXISTS (
                      SELECT 1
                      FROM dbo.UserFeedback AS f
                      WHERE f.ResolutionId = r.ResolutionId
                  )
                """,
                (resolution_id, incident_id, technician_id),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "resolution_id": row.ResolutionId,
                "incident_id": row.IncidentId,
                "resolution_text": row.ResolutionText,
                "incident_reference": row.IncidentReference,
                "incident_title": row.IncidentTitle,
                "user_id": row.UserId,
                "reporter_name": row.ReporterName,
                "reporter_email": row.ReporterEmail,
            }

        finally:
            connection.close()

    @staticmethod
    def record_resolution_email_resent(
        incident_id: int,
        technician_id: int,
        resolution_id: int,
    ):
        """
        Record a successfully resent resolution notification.

        The incident and resolution are checked again before the
        audit entry is written.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT Status
                FROM dbo.Incidents WITH (UPDLOCK, HOLDLOCK)
                WHERE IncidentId = ?
                  AND TechnicianId = ?
                """,
                (incident_id, technician_id),
            )

            incident = cursor.fetchone()

            if incident is None:
                raise ValueError(
                    "This incident does not exist or is not assigned to you."
                )

            if incident.Status != "Awaiting User Confirmation":
                raise ValueError(
                    "The incident is no longer awaiting user confirmation."
                )

            cursor.execute(
                """
                SELECT r.ResolutionId
                FROM dbo.Resolutions AS r
                WHERE r.ResolutionId = ?
                  AND r.IncidentId = ?
                  AND NOT EXISTS (
                      SELECT 1
                      FROM dbo.UserFeedback AS f
                      WHERE f.ResolutionId = r.ResolutionId
                  )
                """,
                (resolution_id, incident_id),
            )

            resolution = cursor.fetchone()

            if resolution is None:
                raise ValueError(
                    "The resolution no longer exists or has already been reviewed."
                )

            cursor.execute(
                """
                INSERT INTO dbo.AuditLogs (
                    IncidentId,
                    UserId,
                    Action,
                    FromStatus,
                    ToStatus,
                    Details
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    incident_id,
                    technician_id,
                    "Resolution Email Resent",
                    incident.Status,
                    incident.Status,
                    f"Notification resent for resolution {resolution_id}.",
                ),
            )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()
