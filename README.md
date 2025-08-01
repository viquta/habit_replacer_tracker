# Habit Tracker Application

A Python-based CLI habit tracking application with database integration, designed to help users track and replace bad habits with good ones.

## 🌟 Project Philosophy

**"Assume the user is performing the habit unless they log that they have not performed the routine."**

This application follows a positive reinforcement approach, making it smooth and encouraging for users to maintain their habits.

## 🚀 Quick Start

**For the impatient** - Get up and running in a few minutes:

1. **Prerequisites**: Windows + SQL Server Express + ODBC Driver 17 + Python 3.8+
2. **Clone**: `git clone https://github.com/viquta/habit_replacer_tracker.git` and `cd habit_replacer_tracker`
3. **Virtual Environment** (optional but recommended):
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```
4. **Install Dependencies**: `pip install -r requirements.txt`
5. **Database**: Create `HabitTrackerDB` in SQL Server (SSMS or sqlcmd), then run:
   ```powershell
   python backend_and_DB_setup/mssql-express/scripts/setup_db.py
   ```
6. **Launch**: `python CLI.py`

For detailed instructions, see the [Installation](#installation) section below.

## Table of Contents

- [Quick Start](#-quick-start)
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

Habit Replacer Tracker is a tool to help users track and replace unwanted habits with positive ones. Built with Python, it showcases both OOP and functional programming techniques.  
The project is designed for educational purposes but can be adapted for personal use.

**⚠️ Platform Compatibility**: This application is designed for **Windows users** and requires SQL Server Express. It is **not compatible with macOS** due to SQL Server Express dependencies.

## Features

- Add, view, and remove habits
- Track progress in replacing bad habits
- Data persistence using SQL Server Express database
- Simple and intuitive CLI 
- Extensible and modular code structure (OOP + Functional programming)

## Installation

> **📋 Requirements**: This application requires **Windows** with SQL Server Express. Not compatible with macOS or Linux (yet).

### Prerequisites

1. **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
   - Make sure Python is added to your system PATH during installation
   - Verify installation: `python --version`

2. **SQL Server Express** - Download from [Microsoft](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
   - Install with default settings
   - **Important**: Instance name should be `SQLEXPRESS` (default)
   - Enable SQL Server Browser service
   - Make sure SQL Server Express service is running

3. **ODBC Driver 17 for SQL Server** - Usually installed with SQL Server Express
   - If needed, download from [Microsoft](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

### Step-by-Step Installation

#### 1. Clone the Repository
```powershell
git clone https://github.com/viquta/habit_replacer_tracker.git
cd habit_replacer_tracker
```

#### 2. Install Python Dependencies
```powershell
# (Optional) Create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

This will install all required packages including:
- `pyodbc` - Database connectivity
- `rich` - Enhanced CLI interface
- `python-dotenv` - Environment variable management
- `python-dateutil` - Date handling utilities

#### 3. Database Setup

**Option A: Using SQL Server Management Studio (SSMS) - Recommended**
1. Open SQL Server Management Studio
2. Connect to `localhost\SQLEXPRESS` (Windows Authentication)
3. Right-click "Databases" → "New Database..."
4. Name it `HabitTrackerDB`
5. Click "OK"

**Option B: Using Command Line**
```powershell
# Connect to SQL Server using sqlcmd (if available)
sqlcmd -S localhost\SQLEXPRESS -E -Q "CREATE DATABASE HabitTrackerDB;"
```

#### 4. Initialize Database Tables
```powershell
# Ensure HabitTrackerDB exists, then initialize tables and users
python backend_and_DB_setup/mssql-express/scripts/setup_db.py
```

This script will:
- Create all necessary tables (Users, Habits, HabitCompletions)
- Set up database relationships and constraints
- Insert sample data for testing
- Configure database permissions

#### 5. Launch the Application
```powershell
python CLI.py
```

### Verification
If everything is set up correctly, you should see:
- A colorful welcome screen
- Main menu with options to manage habits
- No error messages about database connectivity

## Usage

### Starting the Application

```powershell
python CLI.py
```

The application will launch with a colorful CLI interface powered by the Rich library.

### Main Menu Options

When you start the application, you'll see the main menu with these options:

1. **➕ Add New Habit** - Create a new habit to track
2. **📋 View All Habits** - Display all your habits and their status
3. **✅ Mark Habit as Complete** - Log completion for today
4. **❌ Mark Habit as Not Done** - Log that you didn't perform the habit
5. **📊 View Analytics** - See detailed progress and statistics
6. **🗑️ Delete Habit** - Remove a habit permanently
7. **ℹ️ View Habit Details** - See detailed information about a specific habit
8. **❌ Exit** - Close the application

### Creating Your First Habit

1. Select option **1** (Add New Habit)
2. Enter a descriptive name (e.g., "Morning Exercise", "Read for 30 minutes")
3. Add a description that includes:
   - **Trigger** (when/where): "After morning coffee", "Before bed", "When I arrive at office"
   - **Reward** (why/benefit): "to stay healthy", "to grow knowledge", "to reduce stress"
   - **Example**: "After morning coffee (trigger), read for 30 minutes to grow knowledge (reward)"
4. Choose the frequency:
   - **Daily**: Habit performed every day
   - **Weekly**: Habit performed once per week
5. The habit will be created and added to your tracking list

### Tracking Habits

#### Marking Habits Complete ✅
- Select option **3** (Mark Habit as Complete)
- Choose the habit from the list
- Add optional notes about your experience:
  - What triggered the habit?
  - How did it feel during/after?
  - What reward or benefit did you notice?
- The completion will be logged for today's date

#### Viewing Your Notes 📝
- In the completion menu, select **'n'** to view recent notes
- Choose a habit to see your past completion notes
- Review your triggers, experiences, and rewards over time
- Select specific dates to view full notes if truncated

#### Logging Missed Days ❌
- Select option **4** (Mark Habit as Not Done)
- Choose the habit from the list
- Add optional notes explaining why you missed it
- This helps maintain accurate tracking

### Viewing Progress

#### All Habits Overview 📋
- Select option **2** to see all habits
- View current streak, completion rates, and recent activity
- Color-coded display shows habit status at a glance

#### Detailed Analytics 📊
- Select option **5** for comprehensive statistics
- See completion percentages, longest streaks, and trends
- Weekly and monthly summaries
- Visual progress indicators

#### Individual Habit Details ℹ️
- Select option **7** to focus on one habit
- View complete history and detailed statistics
- See notes from previous completions
- Track improvement over time

### Example Workflow

```
1. Start application: python CLI.py
2. Add habit: "Exercise for 30 minutes" (Daily)
3. Each day: Mark as complete or log if missed
4. Weekly: Check analytics to see progress
5. Adjust habits as needed for better success
```

### Tips for Success

- **Be Consistent**: Log your habits daily for accurate tracking
- **Use Notes**: Add context when marking habits complete or missed
- **Review Analytics**: Regular check-ins help maintain motivation
- **Start Small**: Begin with 1-2 habits before adding more
- **Be Honest**: The app works best when you're truthful about completions

### Command Examples

```powershell
# (Optional) Activate the virtual environment
venv\Scripts\Activate.ps1

# Start the application
python CLI.py

# If you get import errors, make sure dependencies are installed
pip install -r requirements.txt

# Check if your Python environment is correct
python --version
```

## Troubleshooting

### Common Issues and Solutions

#### Database Connection Issues

**Error**: `❌ Failed to connect to HabitTrackerDB`

**Solutions**:
1. **Check SQL Server Service**:
   ```powershell
   # Open Services (services.msc) and ensure these are running:
   # - SQL Server (SQLEXPRESS)
   # - SQL Server Browser
   ```

2. **Verify Database Exists**:
   - Open SQL Server Management Studio
   - Connect to `localhost\SQLEXPRESS`
   - Check if `HabitTrackerDB` database exists

3. **Check Instance Name**:
   - Default should be `SQLEXPRESS`
   - If different, update connection strings in backend configuration

#### Python Import Errors

**Error**: `⚠️ Backend not available: ImportError`

**Solutions**:
1. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

2. **Check Python Version**:
   ```powershell
   python --version  # Should be 3.8 or higher
   ```

3. **Virtual Environment** (recommended):
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

#### ODBC Driver Issues

**Error**: `Microsoft ODBC Driver not found`

**Solutions**:
1. **Install ODBC Driver 17**:
   - Download from [Microsoft](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
   - Run installer with default settings

2. **Check Available Drivers**:
   ```powershell
   # In Python:
   import pyodbc
   print(pyodbc.drivers())
   # Should show "ODBC Driver 17 for SQL Server"
   ```

#### Application Crashes

**Error**: Application exits unexpectedly

**Solutions**:
1. **Run with Debug Info**:
   ```powershell
   python -u CLI.py  # Shows all output immediately
   ```

2. **Check Dependencies**:
   ```powershell
   pip list  # Verify all packages are installed
   ```

3. **Database Setup**:
   - Re-run database setup script:
   ```powershell
   python backend_and_DB_setup/mssql-express/scripts/setup_db.py
   ```

### Getting Help

If you continue experiencing issues:

1. **Check Error Messages**: The application provides detailed error messages
2. **Verify Prerequisites**: Ensure all requirements are properly installed
3. **Database Logs**: Check SQL Server logs for connection issues
4. **GitHub Issues**: Report bugs on the project repository

### System Requirements Reminder

- **OS**: Windows 10/11 (SQL Server Express requirement)
- **Python**: 3.8 or higher
- **Memory**: Minimum 4GB RAM
- **Disk**: 500MB free space (including SQL Server Express)
- **Network**: Not required (local database)

## Contributing (I won't accept any contributions until I get my grade for this course.)
...

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact

Created by [viquta](https://github.com/viquta) for International University.  
For questions or suggestions, open an issue or contact me via GitHub.

