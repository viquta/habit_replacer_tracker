# Habit Tracker Database Setup - Native SQL Server Express

## Prerequisites
- **SQL Server Express** (already installed ✅)
- **PowerShell 5.1+** with SqlServer module
- **SQL Server Management Studio (SSMS)** (recommended)

## Install SqlServer PowerShell Module
```powershell
# Run as Administrator
Install-Module -Name SqlServer -Force
```

## Quick Start

### Run the Native Setup (No Docker)
```powershell
cd scripts
.\setup-native.ps1
```

## What This Does
- ✅ Connects to your existing SQL Server Express instance
- ✅ Creates **HabitTrackerDB** database
- ✅ Sets up all tables, views, and sample data
- ✅ Creates secure application user
- ✅ Tests the connection

## Connection Details
- **Server**: `localhost\SQLEXPRESS`
- **Database**: `HabitTrackerDB`
- **App User**: `habit_app_user`
- **App Password**: `HabitApp!Secure2025`
- **Connection String**: 
  ```
  Server=localhost\SQLEXPRESS;Database=HabitTrackerDB;User Id=habit_app_user;Password=HabitApp!Secure2025;TrustServerCertificate=true;
  ```

## Advantages of Native Setup
- 🚀 **Faster performance** - No container overhead
- 🔧 **Easy management** - Use SSMS directly
- 💾 **Better integration** - Windows services, backup tools
- 🔒 **Windows Authentication** - Use your Windows login for admin
- 📊 **SQL Server Profiler** - Advanced debugging tools

## Managing Your Database

### Start/Stop SQL Server Express
```cmd
# Start the service
net start MSSQL$SQLEXPRESS

# Stop the service  
net stop MSSQL$SQLEXPRESS
```

### Connect with SSMS
1. Open **SQL Server Management Studio**
2. Server name: `localhost\SQLEXPRESS`
3. Authentication: **Windows Authentication**
4. Connect to manage your database

## Troubleshooting
- Make sure SQL Server Express service is running
- Check Windows Firewall (usually not needed for localhost)
- Verify you have the SqlServer PowerShell module installed
- Run PowerShell as Administrator if needed

## When to Use Docker vs Native
- **Use Native** (this setup): You have SQL Express installed, want best performance
- **Use Docker**: You want isolated environments, easy cleanup, or don't want to install SQL Server
