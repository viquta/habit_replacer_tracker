# Habit Tracker Application

A Python-based CLI habit tracking application with database integration, designed to help users track and replace bad habits with good ones.

## 🚀 Quick Start

**For the impatient** - Get up and running in minutes:

1. **Prerequisites**: Windows + SQL Server Express + Python 3.8+
2. **Clone**: `git clone https://github.com/viquta/habit_replacer_tracker.git` and `cd habit_replacer_tracker`
3. **Virtual Environment** (optional but recommended):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
4. **Install Dependencies**: `pip install -r requirements.txt`
5. **Database**: Create `HabitTrackerDB` in SQL Server (SSMS or sqlcmd), then run:
   ```powershell
   python backend_and_DB_setup/mssql-express/scripts/setup_db.py
   ```
6. **Launch**: `python CLI_simple.py`

For detailed instructions, see the [Installation](#installation) section below.

## 🌟 Project Philosophy (NOT ESSENTIAL FOR COURSE CRITERIA SO I TOOK AWAY THIS FOR NOW)

**"Assume the user is performing the habit unless they log that they have not performed the routine."**

For now: a basic habit tracker

## Table of Contents

- [Quick Start](#-quick-start)
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Code Documentation](#code-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

Habit Replacer Tracker is a tool to help users track and (not yet) replace unwanted habits with positive ones. Built with Python, it showcases both OOP and functional programming techniques.  
The project is designed for educational purposes but can be adapted for personal use.

**⚠️ Platform Compatibility**: This application is designed for **Windows users** and requires SQL Server Express.

## Features

- Add, view, and remove habits
- Track progress in replacing bad habits  
- Data persistence using SQL Server Express database
- Simple and intuitive CLI interface
- Extensible and modular code structure (OOP + Functional programming)
- Rich visual interface with tables and progress tracking
- Habit completion history and streak tracking
- Analytics and progress reports

## Installation

> **📋 Self-Contained Setup**: This application requires **Windows** with SQL Server Express. All dependencies and setup steps are provided below - no external configuration files or additional downloads needed beyond what's specified.

> **⚠️ Platform Note**: Not compatible with macOS or Linux natively (though could potentially work with Docker SQL Server).

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
# or download the zip file and open it with an IDE of your choice
```

#### 2. Install Python Dependencies
```powershell
# (Optional but recommended) Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

**Note:** If you get execution policy errors when activating, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Alternative Python Commands:** If `python` doesn't work, try:
- `python3 -m venv .venv`
- `py -m venv .venv` (if Python Launcher is available)
- Install Python from [python.org](https://www.python.org/downloads/) and ensure "Add to PATH" is checked

This will install all required packages including:
- `pyodbc` - Database connectivity
- `rich` - Enhanced CLI interface
- `python-dotenv` - Environment variable management
- `python-dateutil` - Date handling utilities

#### 3. Database Setup

**Step 3.1: Create the Database**

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

**Step 3.2: Initialize Database Tables and Sample Data**
```powershell
# Activate virtual environment first (if you created one)
.\.venv\Scripts\Activate.ps1

# Run the setup script to create tables and insert sample data
python backend_and_DB_setup/mssql-express/scripts/setup_db.py
```

This script will:
- Create all necessary tables (Users, Habits, HabitCompletions)
- Set up database relationships and constraints
- Insert sample data for testing (sample users and habits)
- Configure database permissions (may show warnings - this is normal)

**Expected Output:** You should see:
- ✅ Connected to HabitTrackerDB!
- ✅ Tables and users created successfully!
- Some ⚠️ warnings about roles/users (normal for fresh installations)
- 🎉 Database setup complete!

**Note:** The application uses **Windows Authentication** by default, which is more secure and doesn't require separate SQL Server user accounts.

#### 4. Launch the Application
```powershell
# Activate virtual environment first (if you created one)
.\.venv\Scripts\Activate.ps1

# Launch the application
python CLI_simple.py
```

### Verification
If everything is set up correctly, you should see:
- A colorful welcome screen with the Habit Tracker logo
- Main menu with options to manage habits
- No error messages about database connectivity

**What This Setup Provides:**
- ✅ Complete application with all dependencies
- ✅ Sample data for immediate testing
- ✅ No additional configuration files needed
- ✅ Self-contained database setup
- ✅ Ready-to-use habit tracking functionality

**Common Setup Issues:**
- If you see database connection errors, ensure SQL Server Express is running
- If you get "python not recognized" errors, make sure Python is in your PATH or use `py` instead of `python`
- Role/user warnings during setup are normal and don't affect functionality

## Usage

### Starting the Application

```powershell
# Activate virtual environment (if you created one)
.\.venv\Scripts\Activate.ps1

# Launch the application
python CLI_simple.py
```

The application will launch with a colorful CLI interface powered by the Rich library.

### Main Menu Options

When you launch the application, you'll see:

```
╭─────────────────────────────────────────────────────────────────────────────╮
│ 🎯 Simple Habit Tracker                                                     │
│ Track your daily and weekly habits                                          │
╰─────────────────────────────────────────────────────────────────────────────╯

==================================================
📋 MAIN MENU
==================================================
1. 🆕 Create New Habit
2. ✏️  Edit Habit
3. 🗑️  Delete Habit
4. ✅ Mark Habit Complete
5. 📊 View Analytics
6. 📋 List All Habits
7. 📅 View Completion History
8. ❌ Exit
==================================================
💡 Tip: Press Enter to list your habits (default option)
💡 Press Ctrl+C anytime to exit

🎯 Choose an option [1/2/3/4/5/6/7/8] (6):
```

**Menu Options Explained:**

1. **🆕 Create New Habit** - Add a new habit to track (daily, weekly, etc.)
2. **✏️ Edit Habit** - Modify existing habit details
3. **🗑️ Delete Habit** - Remove a habit from tracking
4. **✅ Mark Habit Complete** - Log completion of a habit for today
5. **📊 View Analytics** - See progress statistics and trends
6. **📋 List All Habits** - Display all your current habits
7. **📅 View Completion History** - See detailed completion history for any habit
8. **❌ Exit** - Close the application




### Example Workflow

**Example: Viewing Completion History**

Let's say you want to view completion history for a habit. You would press `7` from the main menu:

```
                                   Your Habits                                 
╭─────┬──────────────────────┬────────────┬──────────────┬─────────────────────╮
│ #   │ Habit Name           │ Period     │ Created      │ Description         │
├─────┼──────────────────────┼────────────┼──────────────┼─────────────────────┤
│ 1   │ Drink 8 glasses of   │ daily      │ 2025-08-02   │ Stay hydrated       │
│     │ water                │            │              │ throughout the day  │
│ 2   │ Read for 30 minutes  │ daily      │ 2025-08-02   │ Read books or       │
│     │                      │            │              │ articles for        │
│     │                      │            │              │ personal growth     │
│ 3   │ Exercise             │ daily      │ 2025-08-02   │ Physical activity   │
│     │                      │            │              │ for health          │
│ 4   │ Meditation           │ daily      │ 2025-08-02   │ 10 minutes of       │
│     │                      │            │              │ mindfulness         │
│ 5   │ Clean house          │ weekly     │ 2025-08-02   │ Weekly house        │
│     │                      │            │              │ cleaning routine    │
╰─────┴──────────────────────┴────────────┴──────────────┴─────────────────────╯
Enter habit number to view history (1):
```

If you choose habit #3 (Exercise):

```
📅 COMPLETION HISTORY: Exercise
Created: 2025-08-02
--------------------------------------------------
                Recent Completions (14 shown)                 
╭──────────────┬────────────┬────────────────────────────────╮
│ Date         │ Time       │ Notes                          │
├──────────────┼────────────┼────────────────────────────────┤
│ 2025-08-02   │ 12:14:52   │ Best week yet!                 │
│ 2025-07-31   │ 12:14:52   │ Almost daily now               │
│ 2025-07-30   │ 12:14:52   │ Feeling great                  │
│ 2025-07-28   │ 12:14:52   │ Consistent now                 │
│ 2025-07-27   │ 12:14:52   │ Getting better                 │
│ 2025-07-26   │ 12:14:52   │ Week 3 progress                │
│ 2025-07-24   │ 12:14:52   │ Good workout                   │
│ 2025-07-22   │ 12:14:52   │ Feeling stronger               │
│ 2025-07-20   │ 12:14:52   │ Building momentum              │
│ 2025-07-19   │ 12:14:52   │ Weekend motivation             │
│ 2025-07-16   │ 12:14:52   │ Short workout                  │
│ 2025-07-13   │ 12:14:52   │ Trying to be consistent        │
│ 2025-07-12   │ 12:14:52   │ Weekend workout                │
│ 2025-07-07   │ 12:14:52   │ Started exercising             │
╰──────────────┴────────────┴────────────────────────────────╯

🔥 Current streak: 1 days

Press Enter to continue...
```

### Tips for Success

- **Be Consistent**: Log your habits daily for accurate tracking
- **Use Notes**: Add context when marking habits complete or missed
- **Review Analytics**: Regular check-ins help maintain motivation
- **Start Small**: Begin with 1-2 habits before adding more
- **Be Honest**: The app works best when you're truthful about completions

## Code Documentation

This project follows Python best practices with comprehensive documentation:

- **Python Docstrings**: All classes, methods, and functions are documented with detailed docstrings following PEP 257 conventions
- **Type Hints**: Modern Python type annotations for better code clarity and IDE support
- **Inline Comments**: Complex logic is explained with clear inline comments
- **Modular Architecture**: Code is organized into logical modules (`backend/`, `models.py`, `services.py`, etc.)

**Key Documentation Locations:**
- `backend/models.py` - Database models and data structures
- `backend/services.py` - Business logic and habit management
- `backend/database.py` - Database connection and operations
- `backend/analytics.py` - Statistics and reporting functions
- `CLI_simple.py` - Main application interface

To explore the code documentation, open any Python file in the project - all public methods include comprehensive docstrings explaining parameters, return values, and usage examples.

## Troubleshooting

### Common Windows Database Issues

#### Problem: "SQL Server service not running"
**Solution:**
1. Open Services (Windows + R, type `services.msc`)
2. Find "SQL Server (SQLEXPRESS)"
3. Right-click → Start
4. Set Startup type to "Automatic" for future use

#### Problem: "Cannot connect to localhost\SQLEXPRESS"
**Solutions:**
1. **Check SQL Server Configuration Manager:**
   - Enable TCP/IP and Named Pipes protocols
   - Restart SQL Server service

2. **Try alternative connection strings:**
   ```powershell
   # Try with just server name
   .\SQLEXPRESS
   
   # Or with full computer name
   COMPUTERNAME\SQLEXPRESS
   ```

#### Problem: "Database 'HabitTrackerDB' already exists but setup fails"
**Solution:**
```sql
-- In SQL Server Management Studio:
USE master;
GO
ALTER DATABASE HabitTrackerDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
GO
DROP DATABASE HabitTrackerDB;
GO
CREATE DATABASE HabitTrackerDB;
GO
```
Then re-run: `python backend_and_DB_setup/mssql-express/scripts/setup_db.py`

#### Problem: "python: The term 'python' is not recognized"
**Solutions:**
1. Use `py` instead of `python`:
   ```powershell
   py CLI_simple.py
   ```
2. Or add Python to PATH during installation
3. Or use full path to Python executable

#### Problem: Role/Permission warnings during setup
These warnings are **normal** and don't affect functionality:
```
⚠️ Warning: Cannot alter role 'habit_app_role' because it does not exist
⚠️ Warning: Cannot find user 'habit_app_user'
```
The app uses Windows Authentication by default, so these SQL Server users aren't needed.



### Getting Help

If you continue experiencing issues:

1. **Check Error Messages**: The application provides detailed error messages
2. **Verify Prerequisites**: Ensure all requirements are properly installed
3. **Database Logs**: Check SQL Server logs for connection issues
4. **Test Connection**: Try connecting to SQL Server with SSMS first
5. **GitHub Issues**: Report bugs on the project repository


## Contributing (I won't accept any contributions until I get my grade for this course.)
...

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact

Created by [viquta](https://github.com/viquta) for International University.  
For questions or suggestions, open an issue or contact me via GitHub.

