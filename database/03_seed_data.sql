USE SupportDeskProDB;


GO
-- =============================================
-- SUPPORTDESK PRO - INITIAL SEED DATA
-- =============================================
-- 1. Insert incident categories
IF NOT EXISTS (SELECT 1
               FROM   dbo.Categories
               WHERE  Name = 'Hardware')
    BEGIN
        INSERT  INTO dbo.Categories (
            Name,
            Description
        )
        VALUES                      ('Hardware', 'Physical computer equipment and peripherals.');
    END

IF NOT EXISTS (SELECT 1
               FROM   dbo.Categories
               WHERE  Name = 'Software')
    BEGIN
        INSERT  INTO dbo.Categories (
            Name,
            Description
        )
        VALUES                      ('Software', 'Applications, operating systems and software errors.');
    END

IF NOT EXISTS (SELECT 1
               FROM   dbo.Categories
               WHERE  Name = 'Network')
    BEGIN
        INSERT  INTO dbo.Categories (
            Name,
            Description
        )
        VALUES                      ('Network', 'Connectivity, internet and network-related problems.');
    END

IF NOT EXISTS (SELECT 1
               FROM   dbo.Categories
               WHERE  Name = 'Access Issues')
    BEGIN
        INSERT  INTO dbo.Categories (
            Name,
            Description
        )
        VALUES                      ('Access Issues', 'Login problems, permissions and account access.');
    END


GO
-- 2. Insert synthetic test accounts
-- These accounts are for development testing only.
-- PasswordHash values are temporary placeholders.
-- We will replace them with securely generated password hashes
-- when implementing authentication.
IF NOT EXISTS (SELECT 1
               FROM   dbo.Users
               WHERE  Email = 'user@supportdesk.local')
    BEGIN
        INSERT  INTO dbo.Users (
            FullName,
            Email,
            PasswordHash,
            Role,
            IsActive
        )
        VALUES                 ('Test User', 'user@supportdesk.local', 'TEMPORARY_HASH', 'User', 1);
    END

IF NOT EXISTS (SELECT 1
               FROM   dbo.Users
               WHERE  Email = 'technician@supportdesk.local')
    BEGIN
        INSERT  INTO dbo.Users (
            FullName,
            Email,
            PasswordHash,
            Role,
            IsActive
        )
        VALUES                 ('Test Technician', 'technician@supportdesk.local', 'TEMPORARY_HASH', 'Technician', 1);
    END

IF NOT EXISTS (SELECT 1
               FROM   dbo.Users
               WHERE  Email = 'admin@supportdesk.local')
    BEGIN
        INSERT  INTO dbo.Users (
            FullName,
            Email,
            PasswordHash,
            Role,
            IsActive
        )
        VALUES                 ('Test Administrator', 'admin@supportdesk.local', 'TEMPORARY_HASH', 'Administrator', 1);
    END

IF NOT EXISTS (SELECT 1
               FROM   dbo.Users
               WHERE  Email = 'supervisor@supportdesk.local')
    BEGIN
        INSERT  INTO dbo.Users (
            FullName,
            Email,
            PasswordHash,
            Role,
            IsActive
        )
        VALUES                 ('Test Supervisor', 'supervisor@supportdesk.local', 'TEMPORARY_HASH', 'Supervisor', 1);
    END


GO
-- 3. Verify inserted categories
SELECT   *
FROM     dbo.Categories
ORDER BY CategoryId;

-- 4. Verify inserted test accounts
SELECT   UserId,
         FullName,
         Email,
         Role,
         IsActive
FROM     dbo.Users
ORDER BY UserId;