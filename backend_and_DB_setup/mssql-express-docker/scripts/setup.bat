@echo off
REM ============================================
REM Habit Tracker Database Setup Script - Windows Batch
REM ============================================

echo 🚀 Starting SQL Server Express setup for Habit Tracker...

REM Navigate to the directory containing the docker-compose file
cd /d "%~dp0..\docker"

REM Start the Docker containers
echo 🐳 Starting Docker containers...
docker-compose up -d

REM Wait for SQL Server to start
echo ⏳ Waiting for SQL Server to start...
timeout /t 30 /nobreak > nul

REM Wait for the container to be healthy
echo 🏥 Checking SQL Server health...
set /a timeout=120
set /a counter=0

:healthcheck
if %counter% geq %timeout% (
    echo ❌ SQL Server failed to start within %timeout% seconds
    exit /b 1
)

docker exec mssql-express /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "YourStrong!Passw0rd123!" -Q "SELECT 1" > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ SQL Server is ready!
    goto :init_db
)

echo ⏳ Still waiting for SQL Server... (%counter%/%timeout%)
timeout /t 5 /nobreak > nul
set /a counter+=5
goto :healthcheck

:init_db
REM Run the initialization script
echo 📝 Initializing the database with security best practices...
docker exec -i mssql-express /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "YourStrong!Passw0rd123!" -d master -i /tmp/init-db.sql

if %errorlevel% equ 0 (
    echo ✅ Database initialization completed successfully!
    echo.
    echo 📊 Database Details:
    echo    - Database Name: HabitTrackerDB
    echo    - Application User: habit_app_user
    echo    - Application Password: HabitApp!Secure2025
    echo    - Connection String: Server=localhost,1433;Database=HabitTrackerDB;User Id=habit_app_user;Password=HabitApp!Secure2025;TrustServerCertificate=true;
    echo.
    echo 🔐 Security Notes:
    echo    - SA account should only be used for admin tasks
    echo    - Use 'habit_app_user' for application connections
    echo    - Application user has minimal required permissions
    echo.
    echo 🎉 Setup complete! Your Habit Tracker database is ready.
) else (
    echo ❌ Database initialization failed!
    exit /b 1
)
