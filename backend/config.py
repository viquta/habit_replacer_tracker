"""
Configuration module for the Habit Tracker application
Centralizes database and application settings
"""
import os
from pathlib import Path

# Database Configuration
"""
Database connection settings for SQL Server Express.
- server: SQL Server instance (localhost\SQLEXPRESS for local development)
- database: Target database name
- driver: ODBC driver for SQL Server connectivity
- use_windows_auth: Use Windows Authentication instead of SQL Server auth
- trust_server_certificate: Trust self-signed certificates (needed for local dev)
"""
DATABASE_CONFIG = {
    'server': 'localhost\\SQLEXPRESS',
    'database': 'HabitTrackerDB',
    'driver': 'ODBC Driver 17 for SQL Server',
    'use_windows_auth': True,
    'trust_server_certificate': True
}

# Application Configuration
"""
Core application settings and business rules.
- default_user: Default username for demo/testing purposes
- default_analysis_period_days: Default time period for analytics (28 days = 4 weeks)
- max_habits_per_user: Maximum number of habits a user can track simultaneously
- supported_periods: Valid habit tracking frequencies
"""
APP_CONFIG = {
    'default_user': 'demo_user',
    'default_analysis_period_days': 28,
    'max_habits_per_user': 50,
    'supported_periods': ['daily', 'weekly']
}

# Path Configuration
"""
Dynamic path configuration for project structure.
Paths are calculated relative to this config file to ensure portability.
"""
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_ROOT = Path(__file__).parent
DB_SCRIPTS_PATH = PROJECT_ROOT / 'backend_and_DB_setup' / 'mssql-express' / 'scripts'

# CLI Configuration
"""
Command-line interface presentation settings.
- console_width: Maximum width for CLI output formatting
- table_min_width: Minimum width for table displays
- enable_colors: Whether to use colored output in terminal
- show_help_on_start: Display help message when CLI starts
"""
CLI_CONFIG = {
    'console_width': 120,
    'table_min_width': 80,
    'enable_colors': True,
    'show_help_on_start': False
}

# Analytics Configuration
"""
Settings for habit analytics and progress calculations.
- default_trend_weeks: Number of weeks to analyze for trend calculations
- min_data_points_for_trend: Minimum entries needed to calculate meaningful trends
- streak_bonus_threshold: Days needed for streak bonuses (7 = weekly streaks)
- completion_rate_*_threshold: Percentage thresholds for categorizing performance:
  * excellent: 90%+ completion rate
  * good: 70-89% completion rate  
  * needs_improvement: 50-69% completion rate
  * below 50% is considered poor performance
"""
ANALYTICS_CONFIG = {
    'default_trend_weeks': 4,
    'min_data_points_for_trend': 3,
    'streak_bonus_threshold': 7,  # Days for streak bonus calculation
    'completion_rate_excellent_threshold': 90,
    'completion_rate_good_threshold': 70,
    'completion_rate_needs_improvement_threshold': 50
}

def get_database_connection_string() -> str:
    """
    Constructs a SQL Server ODBC connection string from DATABASE_CONFIG.
    
    Builds the connection string with driver, server, and database information.
    Conditionally adds Windows Authentication and certificate trust settings
    based on the configuration flags.
    
    Returns:
        str: Complete ODBC connection string ready for use with pyodbc
        
    Example:
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;
         DATABASE=HabitTrackerDB;Trusted_Connection=yes;TrustServerCertificate=yes;"
    """
    config = DATABASE_CONFIG
    
    connection_string = (
        f"DRIVER={{{config['driver']}}};"
        f"SERVER={config['server']};"
        f"DATABASE={config['database']};"
    )
    
    if config['use_windows_auth']:
        connection_string += "Trusted_Connection=yes;"
    
    if config['trust_server_certificate']:
        connection_string += "TrustServerCertificate=yes;"
    
    return connection_string

def get_db_scripts_path() -> Path:
    """
    Returns the path to database initialization and setup scripts.
    
    This path points to the directory containing SQL scripts for database
    creation, table setup, and initial data population.
    
    Returns:
        Path: Absolute path to the database scripts directory
    """
    return DB_SCRIPTS_PATH

def is_development_mode() -> bool:
    """
    Determines if the application is running in development mode.
    
    Checks the HABIT_TRACKER_ENV environment variable. Defaults to 'development'
    if the environment variable is not set. This can be used to enable/disable
    debug features, verbose logging, or development-specific behavior.
    
    Returns:
        bool: True if running in development mode, False otherwise
        
    Environment Variables:
        HABIT_TRACKER_ENV: Set to 'production' to disable development mode
    """
    return os.getenv('HABIT_TRACKER_ENV', 'development').lower() == 'development'
