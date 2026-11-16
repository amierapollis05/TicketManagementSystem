/*
=========================================================
 SupportDesk Pro
 Database Schema
 Database: SupportDeskProDB
 SQL Server: Amier\SQLEXPRESS
=========================================================
*/
USE SupportDeskProDB;


GO
/*=======================================================
  1. USERS
=======================================================*/
CREATE TABLE dbo.Users (
    UserId       INT            IDENTITY (1, 1) PRIMARY KEY,
    FullName     NVARCHAR (100) NOT NULL,
    Email        NVARCHAR (254) NOT NULL UNIQUE,
    PasswordHash NVARCHAR (255) NOT NULL,
    Role         NVARCHAR (20)  NOT NULL,
    IsActive     BIT            CONSTRAINT DF_Users_IsActive DEFAULT 1 NOT NULL,
    CONSTRAINT CK_Users_Role CHECK (Role IN ('User', 'Technician', 'Administrator', 'Supervisor'))
);


GO
/*=======================================================
  2. CATEGORIES
=======================================================*/
CREATE TABLE dbo.Categories (
    CategoryId  INT            IDENTITY (1, 1) PRIMARY KEY,
    Name        NVARCHAR (50)  NOT NULL UNIQUE,
    Description NVARCHAR (250) NOT NULL
);


GO
/*=======================================================
  3. INCIDENTS
=======================================================*/
CREATE TABLE dbo.Incidents (
    IncidentId        INT             IDENTITY (1, 1) PRIMARY KEY,
    IncidentReference NVARCHAR (20)   NOT NULL UNIQUE,
    UserId            INT             NOT NULL,
    TechnicianId      INT             NULL,
    CategoryId        INT             NOT NULL,
    Title             NVARCHAR (150)  NOT NULL,
    Description       NVARCHAR (4000) NOT NULL,
    Priority          NVARCHAR (10)   NOT NULL,
    Status            NVARCHAR (30)   CONSTRAINT DF_Incidents_Status DEFAULT 'Open' NOT NULL,
    CreatedAt         DATETIME2 (7)   CONSTRAINT DF_Incidents_CreatedAt DEFAULT SYSUTCDATETIME() NOT NULL,
    ClosedAt          DATETIME2 (7)   NULL,
    CONSTRAINT FK_Incidents_Users FOREIGN KEY (UserId) REFERENCES dbo.Users (UserId),
    CONSTRAINT FK_Incidents_Technicians FOREIGN KEY (TechnicianId) REFERENCES dbo.Users (UserId),
    CONSTRAINT FK_Incidents_Categories FOREIGN KEY (CategoryId) REFERENCES dbo.Categories (CategoryId),
    CONSTRAINT CK_Incidents_Priority CHECK (Priority IN ('Low', 'Medium', 'High')),
    CONSTRAINT CK_Incidents_Status CHECK (Status IN ('Open', 'In Progress', 'Awaiting User Confirmation', 'Reopened', 'Closed')),
    CONSTRAINT CK_Incidents_ClosedAt CHECK ((Status = 'Closed'
                                             AND ClosedAt IS NOT NULL)
                                            OR (Status <> 'Closed'
                                                AND ClosedAt IS NULL))
);


GO
/*=======================================================
  4. TROUBLESHOOTING RECORDS
=======================================================*/
CREATE TABLE dbo.TroubleshootingRecords (
    RecordId     INT             IDENTITY (1, 1) PRIMARY KEY,
    IncidentId   INT             NOT NULL,
    TechnicianId INT             NOT NULL,
    ActionTaken  NVARCHAR (2000) NOT NULL,
    CreatedAt    DATETIME2 (7)   CONSTRAINT DF_Troubleshooting_CreatedAt DEFAULT SYSUTCDATETIME() NOT NULL,
    CONSTRAINT FK_Troubleshooting_Incidents FOREIGN KEY (IncidentId) REFERENCES dbo.Incidents (IncidentId),
    CONSTRAINT FK_Troubleshooting_Technicians FOREIGN KEY (TechnicianId) REFERENCES dbo.Users (UserId)
);


GO
/*=======================================================
  5. RESOLUTIONS
=======================================================*/
CREATE TABLE dbo.Resolutions (
    ResolutionId   INT             IDENTITY (1, 1) PRIMARY KEY,
    IncidentId     INT             NOT NULL,
    TechnicianId   INT             NOT NULL,
    ResolutionText NVARCHAR (2000) NOT NULL,
    SubmittedAt    DATETIME2 (7)   CONSTRAINT DF_Resolutions_SubmittedAt DEFAULT SYSUTCDATETIME() NOT NULL,
    CONSTRAINT FK_Resolutions_Incidents FOREIGN KEY (IncidentId) REFERENCES dbo.Incidents (IncidentId),
    CONSTRAINT FK_Resolutions_Technicians FOREIGN KEY (TechnicianId) REFERENCES dbo.Users (UserId)
);


GO
/*=======================================================
  6. USER FEEDBACK
=======================================================*/
CREATE TABLE dbo.UserFeedback (
    FeedbackId   INT             IDENTITY (1, 1) PRIMARY KEY,
    IncidentId   INT             NOT NULL,
    ResolutionId INT             NOT NULL,
    UserId       INT             NOT NULL,
    Decision     NVARCHAR (10)   NOT NULL,
    Comments     NVARCHAR (1000) NULL,
    SubmittedAt  DATETIME2 (7)   CONSTRAINT DF_UserFeedback_SubmittedAt DEFAULT SYSUTCDATETIME() NOT NULL,
    CONSTRAINT FK_UserFeedback_Incidents FOREIGN KEY (IncidentId) REFERENCES dbo.Incidents (IncidentId),
    CONSTRAINT FK_UserFeedback_Resolutions FOREIGN KEY (ResolutionId) REFERENCES dbo.Resolutions (ResolutionId),
    CONSTRAINT FK_UserFeedback_Users FOREIGN KEY (UserId) REFERENCES dbo.Users (UserId),
    CONSTRAINT UQ_UserFeedback_Resolution UNIQUE (ResolutionId),
    CONSTRAINT CK_UserFeedback_Decision CHECK (Decision IN ('Accepted', 'Rejected')),
    CONSTRAINT CK_UserFeedback_RejectionReason CHECK (Decision <> 'Rejected'
                                                      OR LEN(LTRIM(RTRIM(ISNULL(Comments, '')))) > 0)
);


GO
/*=======================================================
  7. AUDIT LOGS
=======================================================*/
CREATE TABLE dbo.AuditLogs (
    AuditLogId INT            IDENTITY (1, 1) PRIMARY KEY,
    IncidentId INT            NULL,
    UserId     INT            NULL,
    Action     NVARCHAR (50)  NOT NULL,
    FromStatus NVARCHAR (30)  NULL,
    ToStatus   NVARCHAR (30)  NULL,
    Details    NVARCHAR (500) NULL,
    CreatedAt  DATETIME2 (7)  CONSTRAINT DF_AuditLogs_CreatedAt DEFAULT SYSUTCDATETIME() NOT NULL,
    CONSTRAINT FK_AuditLogs_Incidents FOREIGN KEY (IncidentId) REFERENCES dbo.Incidents (IncidentId),
    CONSTRAINT FK_AuditLogs_Users FOREIGN KEY (UserId) REFERENCES dbo.Users (UserId)
);


GO
/*=======================================================
  8. INDEXES
=======================================================*/
CREATE INDEX IX_Incidents_UserId
    ON dbo.Incidents(UserId);

CREATE INDEX IX_Incidents_TechnicianId
    ON dbo.Incidents(TechnicianId);

CREATE INDEX IX_Incidents_CategoryId
    ON dbo.Incidents(CategoryId);

CREATE INDEX IX_Incidents_Status
    ON dbo.Incidents(Status);

CREATE INDEX IX_TroubleshootingRecords_IncidentId
    ON dbo.TroubleshootingRecords(IncidentId);

CREATE INDEX IX_Resolutions_IncidentId
    ON dbo.Resolutions(IncidentId);

CREATE INDEX IX_UserFeedback_IncidentId
    ON dbo.UserFeedback(IncidentId);

CREATE INDEX IX_AuditLogs_IncidentId
    ON dbo.AuditLogs(IncidentId);


GO
PRINT 'SupportDesk Pro database schema created successfully.';