# Habit Tracker Database Setup - Windows 11

## Prerequisites
- **Docker Desktop for Windows** (with WSL2 backend recommended)
- **PowerShell 5.1+** or **Windows Terminal**

## Quick Start

### Option 1: PowerShell (Recommended)
```powershell
cd scripts
.\setup.ps1
```

### Option 2: Command Prompt
```cmd
cd scripts
setup.bat
```

## What Gets Installed
- **SQL Server 2019 Express** in Docker container
- **HabitTrackerDB** database with:
  - Users, Habits, HabitCompletions, UserSettings tables
  - CurrentStreaks, LongestStreaks, WeeklyProgress views
  - Sample data for testing
  - Secure application user (`habit_app_user`)

## Connection Details
- **Server**: `localhost,1433`
- **Database**: `HabitTrackerDB`
- **App User**: `habit_app_user`
- **App Password**: `HabitApp!Secure2025`
- **Connection String**: 
  ```
  Server=localhost,1433;Database=HabitTrackerDB;User Id=habit_app_user;Password=HabitApp!Secure2025;TrustServerCertificate=true;
  ```

## Management Tools
You can connect using:
- **SQL Server Management Studio (SSMS)** - Free from Microsoft
- **Azure Data Studio** - Cross-platform, modern interface
- **VS Code** with SQL Server extension

## Troubleshooting
- Make sure Docker Desktop is running
- Check Windows Firewall isn't blocking port 1433
- Verify Docker has enough memory allocated (4GB+ recommended)

## Security Notes
- The SA password is set in `.env` file
- Use `habit_app_user` for application connections
- SA account should only be used for admin tasks
