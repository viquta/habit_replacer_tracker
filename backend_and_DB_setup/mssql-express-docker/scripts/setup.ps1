# ============================================
# Habit Tracker Database Setup Script - Windows PowerShell
# ============================================

Write-Host "🚀 Starting SQL Server Express setup for Habit Tracker..." -ForegroundColor Green

# Load environment variables from .env file
$envFile = Join-Path $PSScriptRoot "..\\.env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "^([^#].*)=(.*)$") {
            [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
        }
    }
}

# Navigate to the directory containing the docker-compose file
$dockerDir = Join-Path $PSScriptRoot "..\\docker"
Set-Location $dockerDir

# Start the Docker containers
Write-Host "🐳 Starting Docker containers..." -ForegroundColor Cyan
docker-compose up -d

# Wait for SQL Server to start
Write-Host "⏳ Waiting for SQL Server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Wait for the container to be healthy
Write-Host "🏥 Checking SQL Server health..." -ForegroundColor Yellow
$timeout = 120
$counter = 0

while ($counter -lt $timeout) {
    $result = docker exec mssql-express /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'YourStrong!Passw0rd123!' -Q 'SELECT 1' 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ SQL Server is ready!" -ForegroundColor Green
        break
    }
    Write-Host "⏳ Still waiting for SQL Server... ($counter/$timeout)" -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    $counter += 5
}

if ($counter -ge $timeout) {
    Write-Host "❌ SQL Server failed to start within $timeout seconds" -ForegroundColor Red
    exit 1
}

# Run the initialization script
Write-Host "📝 Initializing the database with security best practices..." -ForegroundColor Cyan
$result = docker exec -i mssql-express /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'YourStrong!Passw0rd123!' -d master -i /tmp/init-db.sql

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database initialization completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Database Details:" -ForegroundColor White
    Write-Host "   - Database Name: HabitTrackerDB" -ForegroundColor Gray
    Write-Host "   - Application User: habit_app_user" -ForegroundColor Gray
    Write-Host "   - Application Password: HabitApp!Secure2025" -ForegroundColor Gray
    Write-Host "   - Connection String: Server=localhost,1433;Database=HabitTrackerDB;User Id=habit_app_user;Password=HabitApp!Secure2025;TrustServerCertificate=true;" -ForegroundColor Gray
    Write-Host ""
    Write-Host "🔐 Security Notes:" -ForegroundColor White
    Write-Host "   - SA account should only be used for admin tasks" -ForegroundColor Gray
    Write-Host "   - Use 'habit_app_user' for application connections" -ForegroundColor Gray
    Write-Host "   - Application user has minimal required permissions" -ForegroundColor Gray
    Write-Host ""
    Write-Host "🎉 Setup complete! Your Habit Tracker database is ready." -ForegroundColor Green
} else {
    Write-Host "❌ Database initialization failed!" -ForegroundColor Red
    exit 1
}
