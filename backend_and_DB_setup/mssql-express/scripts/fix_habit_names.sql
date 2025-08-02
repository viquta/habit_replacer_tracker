-- Script to remove emoji symbols from existing habit names
-- Run this if you want to keep your existing data and just fix the habit names

USE HabitTrackerDB;
GO

-- Update habit names to remove emoji symbols
UPDATE Habits 
SET HabitName = 'Drink 8 glasses of water'
WHERE HabitName LIKE '%Drink 8 glasses of water%';

UPDATE Habits 
SET HabitName = 'Read for 30 minutes'
WHERE HabitName LIKE '%Read for 30 minutes%';

UPDATE Habits 
SET HabitName = 'Exercise'
WHERE HabitName LIKE '%Exercise%' AND HabitName NOT IN ('Read for 30 minutes', 'Drink 8 glasses of water', 'Meditation', 'Clean house');

UPDATE Habits 
SET HabitName = 'Meditation'
WHERE HabitName LIKE '%Meditation%';

UPDATE Habits 
SET HabitName = 'Clean house'
WHERE HabitName LIKE '%Clean house%';

-- Display updated habits to verify changes
SELECT HabitID, HabitName, Description, Period, CreatedDate 
FROM Habits 
ORDER BY HabitID;

PRINT '✅ Habit names updated successfully!';
