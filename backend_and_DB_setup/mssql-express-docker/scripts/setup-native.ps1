# ============================================
# Habit Tracker Database Setup Script - Native SQL Server Express
# Windows PowerShell - No Docker Required
# ============================================

Write-Host "🚀 Starting Habit Tracker database setup on native SQL Server Express..." -ForegroundColor Green

# Configuration
$ServerInstance = "localhost\SQLEXPRESS"  # Default SQL Express instance
$InitScriptPath = Join-Path $PSScriptRoot "init-db.sql"

# Check if SQL Server is running
Write-Host "🔍 Checking SQL Server Express connection..." -ForegroundColor Cyan
try {
    $testQuery = "SELECT @@VERSION"
    $result = Invoke-Sqlcmd -ServerInstance $ServerInstance -Query $testQuery -TrustServerCertificate
    Write-Host "✅ Connected to SQL Server Express successfully!" -ForegroundColor Green
    Write-Host "   Version: $($result.Column1.Split("`n")[0])" -ForegroundColor Gray
} catch {
    Write-Host "❌ Cannot connect to SQL Server Express at $ServerInstance" -ForegroundColor Red
    Write-Host "   Make sure SQL Server Express is installed and running" -ForegroundColor Yellow
    Write-Host "   You can start it with: 'net start MSSQL`$SQLEXPRESS'" -ForegroundColor Yellow
    exit 1
}

# Check if init script exists
if (-not (Test-Path $InitScriptPath)) {
    Write-Host "❌ Cannot find init-db.sql script at: $InitScriptPath" -ForegroundColor Red
    exit 1
}

# Run the initialization script
Write-Host "📝 Running database initialization script..." -ForegroundColor Cyan
try {
    Invoke-Sqlcmd -ServerInstance $ServerInstance -InputFile $InitScriptPath -TrustServerCertificate -Verbose
    Write-Host "✅ Database initialization completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Database initialization failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test the application user connection
Write-Host "🔐 Testing application user connection..." -ForegroundColor Cyan
try {
    $testQuery = "SELECT COUNT(*) as HabitCount FROM Habits"
    $result = Invoke-Sqlcmd -ServerInstance $ServerInstance -Database "HabitTrackerDB" -Username "habit_app_user" -Password "HabitApp!Secure2025" -Query $testQuery -TrustServerCertificate
    Write-Host "✅ Application user connection successful!" -ForegroundColor Green
    Write-Host "   Sample data loaded: $($result.HabitCount) habits found" -ForegroundColor Gray
} catch {
    Write-Host "⚠️  Application user test failed, but database may still be created" -ForegroundColor Yellow
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📊 Database Details:" -ForegroundColor White
Write-Host "   - Server Instance: $ServerInstance" -ForegroundColor Gray
Write-Host "   - Database Name: HabitTrackerDB" -ForegroundColor Gray
Write-Host "   - Application User: habit_app_user" -ForegroundColor Gray
Write-Host "   - Application Password: HabitApp!Secure2025" -ForegroundColor Gray
Write-Host "   - Connection String: Server=$ServerInstance;Database=HabitTrackerDB;User Id=habit_app_user;Password=HabitApp!Secure2025;TrustServerCertificate=true;" -ForegroundColor Gray
Write-Host ""
Write-Host "🔧 Management Tools:" -ForegroundColor White
Write-Host "   - SQL Server Management Studio (SSMS)" -ForegroundColor Gray
Write-Host "   - Connect to: $ServerInstance" -ForegroundColor Gray
Write-Host ""
Write-Host "🔐 Security Notes:" -ForegroundColor White
Write-Host "   - Use Windows Authentication for admin tasks" -ForegroundColor Gray
Write-Host "   - Use 'habit_app_user' for application connections" -ForegroundColor Gray
Write-Host "   - Application user has minimal required permissions" -ForegroundColor Gray
Write-Host ""
Write-Host "🎉 Setup complete! Your Habit Tracker database is ready on native SQL Server Express." -ForegroundColor Green
