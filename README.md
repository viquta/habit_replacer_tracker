# Habit Tracker Application

A Python-based CLI habit tracking application with database integration, designed to help users track and replace bad habits with good ones.

## 🌟 Project Philosophy (NOT ESSENTIAL FOR COURSE CRITERIA SO I TOOK AWAY THIS FOR NOW)

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
6. **Launch**: `python CLI_simple.py`

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
python CLI_simple.py
```

### Advanced Configuration

The database connection settings can be found in `backend/config.py`:
- **Server**: `localhost\SQLEXPRESS` (default SQL Server Express instance)
- **Database**: `HabitTrackerDB`
- **Authentication**: Windows Authentication (recommended)
- **Driver**: ODBC Driver 17 for SQL Server

If you need to use a different SQL Server instance or authentication method, modify the `DATABASE_CONFIG` in `backend/config.py`.

## Usage
If everything is set up correctly, you should see:
- A colorful welcome screen with the Habit Tracker logo
- Main menu with options to manage habits
- No error messages about database connectivity

**Common Setup Issues:**
- If you see database connection errors, ensure SQL Server Express is running
- If you get "python not recognized" errors, make sure Python is in your PATH or use `py` instead of `python`
- Role/user warnings during setup are normal and don't affect functionality

## Usage

### Starting the Application

```powershell
python CLI_simple.py
```

The application will launch with a colorful CLI interface powered by the Rich library.

### Main Menu Options


### Example Workflow


### Tips for Success

- **Be Consistent**: Log your habits daily for accurate tracking
- **Use Notes**: Add context when marking habits complete or missed
- **Review Analytics**: Regular check-ins help maintain motivation
- **Start Small**: Begin with 1-2 habits before adding more
- **Be Honest**: The app works best when you're truthful about completions



## Troubleshooting



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

