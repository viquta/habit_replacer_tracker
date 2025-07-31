# Habit Tracker Application

A Python-based CLI habit tracking application with database integration, designed to help users track and replace bad habits with good ones.

## 🌟 Project Philosophy

**"Assume the user is performing the habit unless they log that they have not performed the routine."**

This application follows a positive reinforcement approach, making it smooth and encouraging for users to maintain their habits.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
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
2. **SQL Server Express** - Download from [Microsoft](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
   - Make sure SQL Server Express is running on your system
   - Default instance name should be `SQLEXPRESS`

### Database Setup

1. **Create the database manually** using SQL Server Management Studio (SSMS) or command line:
   ```sql
   CREATE DATABASE HabitTrackerDB;
   ```
   
2. **Install Python dependencies**:
   ```bash
   pip install pyodbc
   ```

3. **Run the database setup script**:
   ```bash
   python backend_and_DB_setup/mssql-express-docker/scripts/setup_db.py
   ```
   
   This will create all necessary tables, users, and sample data.

### Application Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/viquta/habit_replacer_tracker.git
   cd habit_replacer_tracker
   ```

2. **Run the application**:
   ```bash
   python CLI.py
   ```

## Usage


...

## Contributing (I won't accept any contributions until I get my grade for this course.)
...

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact

Created by [viquta](https://github.com/viquta) for International University.  
For questions or suggestions, open an issue or contact me via GitHub.

