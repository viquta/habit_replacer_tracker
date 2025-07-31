-- ============================================
-- Habit Tracker Database Initialization Script
-- Following Microsoft Security Best Practices
-- ============================================

-- Create the database
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'HabitTrackerDB')
BEGIN
    CREATE DATABASE HabitTrackerDB;
END
GO

USE HabitTrackerDB;
GO

--using windows authentication for the application role so i dont need to make a user

-- Add user to the application role
ALTER ROLE habit_app_role ADD MEMBER habit_app_user;
GO

-- Create tables
-- Users table (will only have one user, but I'm planning for future scalability //victor)
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(50) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(255) NOT NULL,
    Email NVARCHAR(100) NOT NULL UNIQUE,
    CreatedAt DATETIME2 DEFAULT SYSDATETIME()
);
GO

CREATE TABLE Habits (
    HabitID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    HabitName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500),
    Period NVARCHAR(20) NOT NULL CHECK (Period IN ('daily', 'weekly')),
    CreatedDate DATE NOT NULL DEFAULT CAST(SYSDATETIME() AS DATE),
    IsActive BIT DEFAULT 1,
    CreatedAt DATETIME2 DEFAULT SYSDATETIME(),
    CONSTRAINT FK_Habits_Users FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
GO

CREATE TABLE HabitCompletions (
    CompletionID INT PRIMARY KEY IDENTITY(1,1),
    HabitID INT NOT NULL,
    CompletionDate DATE NOT NULL,
    Notes NVARCHAR(500),
    CreatedAt DATETIME2 DEFAULT SYSDATETIME(),
    CONSTRAINT FK_HabitCompletions_Habits FOREIGN KEY (HabitID) REFERENCES Habits(HabitID) ON DELETE CASCADE,
    CONSTRAINT UK_HabitCompletions_HabitDate UNIQUE (HabitID, CompletionDate)
);
GO

CREATE TABLE UserSettings (
    SettingID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    SettingKey NVARCHAR(50) NOT NULL,
    SettingValue NVARCHAR(500),
    UpdatedAt DATETIME2 DEFAULT SYSDATETIME(),
    CONSTRAINT FK_UserSettings_Users FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    CONSTRAINT UK_UserSettings_UserKey UNIQUE (UserID, SettingKey)
);
GO

-- Create indexes for better performance
CREATE INDEX IX_Habits_UserID ON Habits(UserID);
CREATE INDEX IX_Habits_IsActive ON Habits(IsActive);
CREATE INDEX IX_HabitCompletions_HabitID ON HabitCompletions(HabitID);
CREATE INDEX IX_HabitCompletions_CompletionDate ON HabitCompletions(CompletionDate);
CREATE INDEX IX_UserSettings_UserID ON UserSettings(UserID);
GO

-- Grant appropriate permissions to the application role
-- SELECT permissions
GRANT SELECT ON Users TO habit_app_role;
GRANT SELECT ON Habits TO habit_app_role;
GRANT SELECT ON HabitCompletions TO habit_app_role;
GRANT SELECT ON UserSettings TO habit_app_role;

-- INSERT permissions
GRANT INSERT ON Users TO habit_app_role;
GRANT INSERT ON Habits TO habit_app_role;
GRANT INSERT ON HabitCompletions TO habit_app_role;
GRANT INSERT ON UserSettings TO habit_app_role;

-- UPDATE permissions
GRANT UPDATE ON Users TO habit_app_role;
GRANT UPDATE ON Habits TO habit_app_role;
GRANT UPDATE ON HabitCompletions TO habit_app_role;
GRANT UPDATE ON UserSettings TO habit_app_role;

-- DELETE permissions (restricted - only soft deletes recommended)
GRANT DELETE ON HabitCompletions TO habit_app_role;
GRANT DELETE ON UserSettings TO habit_app_role;
-- Note: No DELETE permission on Users and Habits - use IsActive flag instead

GO

-- Insert some sample data for testing
INSERT INTO Users (Username, PasswordHash, Email) VALUES 
('demo_user', 'hashed_password_here', 'demo@example.com');
GO

DECLARE @UserID INT = SCOPE_IDENTITY();

INSERT INTO Habits (UserID, HabitName, Description, Period) VALUES 
(@UserID, '💧 Drink 8 glasses of water', 'Stay hydrated throughout the day', 'daily'),
(@UserID, '📖 Read for 30 minutes', 'Read books or articles for personal growth', 'daily'),
(@UserID, '🏃‍♂️ Exercise', 'Physical activity for health', 'daily'),
(@UserID, '🧘 Meditation', '10 minutes of mindfulness', 'daily'),
(@UserID, '🏠 Clean house', 'Weekly house cleaning routine', 'weekly');
GO

-- Insert comprehensive sample completions (4-week period for testing)
DECLARE @HabitID1 INT = (SELECT TOP 1 HabitID FROM Habits WHERE HabitName LIKE '%water%');
DECLARE @HabitID2 INT = (SELECT TOP 1 HabitID FROM Habits WHERE HabitName LIKE '%Read%');
DECLARE @HabitID3 INT = (SELECT TOP 1 HabitID FROM Habits WHERE HabitName LIKE '%Exercise%');
DECLARE @HabitID4 INT = (SELECT TOP 1 HabitID FROM Habits WHERE HabitName LIKE '%Meditation%');
DECLARE @HabitID5 INT = (SELECT TOP 1 HabitID FROM Habits WHERE HabitName LIKE '%Clean%');

-- Water habit (daily) - Very consistent (26/28 days)
INSERT INTO HabitCompletions (HabitID, CompletionDate, Notes) VALUES 
-- Week 1
(@HabitID1, DATEADD(DAY, -27, CAST(SYSDATETIME() AS DATE)), '8 glasses completed'),
(@HabitID1, DATEADD(DAY, -26, CAST(SYSDATETIME() AS DATE)), 'Feeling more hydrated'),
(@HabitID1, DATEADD(DAY, -25, CAST(SYSDATETIME() AS DATE)), 'Easy day'),
(@HabitID1, DATEADD(DAY, -24, CAST(SYSDATETIME() AS DATE)), 'Almost forgot but completed'),
(@HabitID1, DATEADD(DAY, -23, CAST(SYSDATETIME() AS DATE)), 'Great habit'),
(@HabitID1, DATEADD(DAY, -22, CAST(SYSDATETIME() AS DATE)), 'Weekend motivation'),
(@HabitID1, DATEADD(DAY, -21, CAST(SYSDATETIME() AS DATE)), 'Week 1 complete'),
-- Week 2
(@HabitID1, DATEADD(DAY, -20, CAST(SYSDATETIME() AS DATE)), 'Starting strong'),
(@HabitID1, DATEADD(DAY, -19, CAST(SYSDATETIME() AS DATE)), 'Consistent'),
(@HabitID1, DATEADD(DAY, -18, CAST(SYSDATETIME() AS DATE)), 'Feeling good'),
(@HabitID1, DATEADD(DAY, -17, CAST(SYSDATETIME() AS DATE)), 'Midweek success'),
-- Skip day -16 (missed one day)
(@HabitID1, DATEADD(DAY, -15, CAST(SYSDATETIME() AS DATE)), 'Back on track'),
(@HabitID1, DATEADD(DAY, -14, CAST(SYSDATETIME() AS DATE)), 'Weekend hydration'),
-- Week 3
(@HabitID1, DATEADD(DAY, -13, CAST(SYSDATETIME() AS DATE)), 'Week 3 start'),
(@HabitID1, DATEADD(DAY, -12, CAST(SYSDATETIME() AS DATE)), 'Steady progress'),
(@HabitID1, DATEADD(DAY, -11, CAST(SYSDATETIME() AS DATE)), 'Feeling energized'),
(@HabitID1, DATEADD(DAY, -10, CAST(SYSDATETIME() AS DATE)), 'Habit forming'),
(@HabitID1, DATEADD(DAY, -9, CAST(SYSDATETIME() AS DATE)), 'Almost automatic'),
(@HabitID1, DATEADD(DAY, -8, CAST(SYSDATETIME() AS DATE)), 'Weekend consistency'),
(@HabitID1, DATEADD(DAY, -7, CAST(SYSDATETIME() AS DATE)), 'Week 3 done'),
-- Week 4
(@HabitID1, DATEADD(DAY, -6, CAST(SYSDATETIME() AS DATE)), 'Final week'),
(@HabitID1, DATEADD(DAY, -5, CAST(SYSDATETIME() AS DATE)), 'Strong finish'),
(@HabitID1, DATEADD(DAY, -4, CAST(SYSDATETIME() AS DATE)), 'Maintaining momentum'),
(@HabitID1, DATEADD(DAY, -3, CAST(SYSDATETIME() AS DATE)), 'Nearly there'),
(@HabitID1, DATEADD(DAY, -2, CAST(SYSDATETIME() AS DATE)), 'Penultimate day'),
-- Skip day -1 (missed another day)
(@HabitID1, DATEADD(DAY, 0, CAST(SYSDATETIME() AS DATE)), 'Today completed');

-- Reading habit (daily) - Moderately consistent (18/28 days)
INSERT INTO HabitCompletions (HabitID, CompletionDate, Notes) VALUES 
-- Week 1 (5/7 days)
(@HabitID2, DATEADD(DAY, -27, CAST(SYSDATETIME() AS DATE)), 'Started new book'),
(@HabitID2, DATEADD(DAY, -26, CAST(SYSDATETIME() AS DATE)), 'Enjoying the story'),
(@HabitID2, DATEADD(DAY, -24, CAST(SYSDATETIME() AS DATE)), 'Caught up'),
(@HabitID2, DATEADD(DAY, -23, CAST(SYSDATETIME() AS DATE)), 'Good chapter'),
(@HabitID2, DATEADD(DAY, -21, CAST(SYSDATETIME() AS DATE)), 'Weekend reading'),
-- Week 2 (4/7 days)
(@HabitID2, DATEADD(DAY, -19, CAST(SYSDATETIME() AS DATE)), 'Back to reading'),
(@HabitID2, DATEADD(DAY, -17, CAST(SYSDATETIME() AS DATE)), 'Interesting plot'),
(@HabitID2, DATEADD(DAY, -15, CAST(SYSDATETIME() AS DATE)), 'Making progress'),
(@HabitID2, DATEADD(DAY, -14, CAST(SYSDATETIME() AS DATE)), 'Weekend catch-up'),
-- Week 3 (5/7 days)
(@HabitID2, DATEADD(DAY, -13, CAST(SYSDATETIME() AS DATE)), 'New week motivation'),
(@HabitID2, DATEADD(DAY, -11, CAST(SYSDATETIME() AS DATE)), 'Great insights'),
(@HabitID2, DATEADD(DAY, -10, CAST(SYSDATETIME() AS DATE)), 'Learning a lot'),
(@HabitID2, DATEADD(DAY, -8, CAST(SYSDATETIME() AS DATE)), 'Weekend session'),
(@HabitID2, DATEADD(DAY, -7, CAST(SYSDATETIME() AS DATE)), 'Finished chapter'),
-- Week 4 (4/7 days)
(@HabitID2, DATEADD(DAY, -5, CAST(SYSDATETIME() AS DATE)), 'Final push'),
(@HabitID2, DATEADD(DAY, -3, CAST(SYSDATETIME() AS DATE)), 'Getting close'),
(@HabitID2, DATEADD(DAY, -2, CAST(SYSDATETIME() AS DATE)), 'Almost done'),
(@HabitID2, DATEADD(DAY, 0, CAST(SYSDATETIME() AS DATE)), 'Finished the book!');

-- Exercise habit (daily) - Struggling but improving (14/28 days)
INSERT INTO HabitCompletions (HabitID, CompletionDate, Notes) VALUES 
-- Week 1 (2/7 days)
(@HabitID3, DATEADD(DAY, -26, CAST(SYSDATETIME() AS DATE)), 'Started exercising'),
(@HabitID3, DATEADD(DAY, -21, CAST(SYSDATETIME() AS DATE)), 'Weekend workout'),
-- Week 2 (3/7 days)
(@HabitID3, DATEADD(DAY, -20, CAST(SYSDATETIME() AS DATE)), 'Trying to be consistent'),
(@HabitID3, DATEADD(DAY, -17, CAST(SYSDATETIME() AS DATE)), 'Short workout'),
(@HabitID3, DATEADD(DAY, -14, CAST(SYSDATETIME() AS DATE)), 'Weekend motivation'),
-- Week 3 (4/7 days)
(@HabitID3, DATEADD(DAY, -13, CAST(SYSDATETIME() AS DATE)), 'Building momentum'),
(@HabitID3, DATEADD(DAY, -11, CAST(SYSDATETIME() AS DATE)), 'Feeling stronger'),
(@HabitID3, DATEADD(DAY, -9, CAST(SYSDATETIME() AS DATE)), 'Good workout'),
(@HabitID3, DATEADD(DAY, -7, CAST(SYSDATETIME() AS DATE)), 'Week 3 progress'),
-- Week 4 (5/7 days) - showing improvement
(@HabitID3, DATEADD(DAY, -6, CAST(SYSDATETIME() AS DATE)), 'Getting better'),
(@HabitID3, DATEADD(DAY, -5, CAST(SYSDATETIME() AS DATE)), 'Consistent now'),
(@HabitID3, DATEADD(DAY, -3, CAST(SYSDATETIME() AS DATE)), 'Feeling great'),
(@HabitID3, DATEADD(DAY, -2, CAST(SYSDATETIME() AS DATE)), 'Almost daily now'),
(@HabitID3, DATEADD(DAY, 0, CAST(SYSDATETIME() AS DATE)), 'Best week yet!');

-- Meditation habit (daily) - Very sporadic (8/28 days)
INSERT INTO HabitCompletions (HabitID, CompletionDate, Notes) VALUES 
-- Week 1 (1/7 days)
(@HabitID4, DATEADD(DAY, -25, CAST(SYSDATETIME() AS DATE)), 'First meditation'),
-- Week 2 (2/7 days)
(@HabitID4, DATEADD(DAY, -18, CAST(SYSDATETIME() AS DATE)), 'Trying again'),
(@HabitID4, DATEADD(DAY, -15, CAST(SYSDATETIME() AS DATE)), 'Relaxing session'),
-- Week 3 (3/7 days)
(@HabitID4, DATEADD(DAY, -12, CAST(SYSDATETIME() AS DATE)), 'Feeling centered'),
(@HabitID4, DATEADD(DAY, -10, CAST(SYSDATETIME() AS DATE)), 'Peaceful moment'),
(@HabitID4, DATEADD(DAY, -8, CAST(SYSDATETIME() AS DATE)), 'Weekend mindfulness'),
-- Week 4 (2/7 days)
(@HabitID4, DATEADD(DAY, -4, CAST(SYSDATETIME() AS DATE)), 'Back to it'),
(@HabitID4, DATEADD(DAY, -1, CAST(SYSDATETIME() AS DATE)), 'Yesterday''s peace');

-- House cleaning habit (weekly) - Perfect consistency (4/4 weeks)
INSERT INTO HabitCompletions (HabitID, CompletionDate, Notes) VALUES 
(@HabitID5, DATEADD(DAY, -21, CAST(SYSDATETIME() AS DATE)), 'Deep clean - Week 1'),
(@HabitID5, DATEADD(DAY, -14, CAST(SYSDATETIME() AS DATE)), 'Thorough cleaning - Week 2'),
(@HabitID5, DATEADD(DAY, -7, CAST(SYSDATETIME() AS DATE)), 'Weekly maintenance - Week 3'),
(@HabitID5, DATEADD(DAY, 0, CAST(SYSDATETIME() AS DATE)), 'Fresh and clean - Week 4');
GO

-- ============================================
-- Analytics Views for Enhanced Reporting
-- ============================================

-- View: Current Streaks Calculation
CREATE VIEW CurrentStreaks AS
WITH StreakData AS (
    SELECT 
        h.HabitID,
        h.HabitName,
        h.Period,
        hc.CompletionDate,
        -- Calculate date differences based on habit period
        CASE 
            WHEN h.Period = 'daily' THEN 
                ROW_NUMBER() OVER (PARTITION BY h.HabitID ORDER BY hc.CompletionDate DESC) - 1
            WHEN h.Period = 'weekly' THEN 
                ROW_NUMBER() OVER (PARTITION BY h.HabitID ORDER BY hc.CompletionDate DESC) - 1
        END as RowNum,
        CASE 
            WHEN h.Period = 'daily' THEN 
                DATEDIFF(DAY, hc.CompletionDate, CAST(SYSDATETIME() AS DATE))
            WHEN h.Period = 'weekly' THEN 
                DATEDIFF(WEEK, hc.CompletionDate, CAST(SYSDATETIME() AS DATE))
        END as PeriodDiff
    FROM Habits h
    INNER JOIN HabitCompletions hc ON h.HabitID = hc.HabitID
    WHERE h.IsActive = 1
),
ConsecutiveStreaks AS (
    SELECT 
        HabitID,
        HabitName,
        Period,
        CompletionDate,
        RowNum,
        PeriodDiff,
        -- Check if this completion is part of current streak
        CASE 
            WHEN PeriodDiff = RowNum THEN 1
            ELSE 0
        END as IsConsecutive
    FROM StreakData
)
SELECT 
    HabitID,
    HabitName,
    Period,
    COALESCE(MAX(CASE WHEN IsConsecutive = 1 THEN RowNum + 1 ELSE 0 END), 0) as CurrentStreak
FROM ConsecutiveStreaks
GROUP BY HabitID, HabitName, Period;
GO

-- View: Longest Streaks Ever
CREATE VIEW LongestStreaks AS
WITH ConsecutiveDates AS (
    SELECT 
        h.HabitID,
        h.HabitName,
        h.Period,
        hc.CompletionDate,
        -- Create groups of consecutive dates
        CASE 
            WHEN h.Period = 'daily' THEN
                DATEADD(DAY, -ROW_NUMBER() OVER (PARTITION BY h.HabitID ORDER BY hc.CompletionDate), hc.CompletionDate)
            WHEN h.Period = 'weekly' THEN
                DATEADD(WEEK, -ROW_NUMBER() OVER (PARTITION BY h.HabitID ORDER BY hc.CompletionDate), hc.CompletionDate)
        END as StreakGroup
    FROM Habits h
    INNER JOIN HabitCompletions hc ON h.HabitID = hc.HabitID
    WHERE h.IsActive = 1
),
StreakCounts AS (
    SELECT 
        HabitID,
        HabitName,
        Period,
        StreakGroup,
        COUNT(*) as StreakLength,
        MIN(CompletionDate) as StreakStart,
        MAX(CompletionDate) as StreakEnd
    FROM ConsecutiveDates
    GROUP BY HabitID, HabitName, Period, StreakGroup
)
SELECT 
    HabitID,
    HabitName,
    Period,
    MAX(StreakLength) as LongestStreak,
    -- Get the dates for the longest streak
    (SELECT TOP 1 StreakStart FROM StreakCounts sc2 
     WHERE sc2.HabitID = sc1.HabitID AND sc2.StreakLength = MAX(sc1.StreakLength)) as LongestStreakStart,
    (SELECT TOP 1 StreakEnd FROM StreakCounts sc2 
     WHERE sc2.HabitID = sc1.HabitID AND sc2.StreakLength = MAX(sc1.StreakLength)) as LongestStreakEnd
FROM StreakCounts sc1
GROUP BY HabitID, HabitName, Period;
GO

-- View: Weekly Progress Summary
CREATE VIEW WeeklyProgress AS
SELECT 
    h.HabitID,
    h.HabitName,
    h.Period,
    YEAR(hc.CompletionDate) as Year,
    DATEPART(WEEK, hc.CompletionDate) as WeekNumber,
    COUNT(hc.CompletionID) as CompletionsThisWeek,
    CASE 
        WHEN h.Period = 'daily' THEN 
            CAST(COUNT(hc.CompletionID) * 100.0 / 7.0 AS DECIMAL(5,2))
        WHEN h.Period = 'weekly' AND COUNT(hc.CompletionID) >= 1 THEN 100.0
        ELSE 0.0
    END as WeeklyCompletionRate,
    MIN(hc.CompletionDate) as FirstCompletionThisWeek,
    MAX(hc.CompletionDate) as LastCompletionThisWeek
FROM Habits h
LEFT JOIN HabitCompletions hc ON h.HabitID = hc.HabitID
WHERE h.IsActive = 1 AND hc.CompletionDate IS NOT NULL
GROUP BY h.HabitID, h.HabitName, h.Period, YEAR(hc.CompletionDate), DATEPART(WEEK, hc.CompletionDate);
GO

-- Grant SELECT permissions on views to application role
GRANT SELECT ON CurrentStreaks TO habit_app_role;
GRANT SELECT ON LongestStreaks TO habit_app_role;
GRANT SELECT ON WeeklyProgress TO habit_app_role;
GO

PRINT 'Database initialization completed successfully!';
PRINT 'Application user: habit_app_user';
PRINT 'Database: HabitTrackerDB';
PRINT 'Enhanced with 4-week test data and analytics views!';
GO