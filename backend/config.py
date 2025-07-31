"""
Configuration module for the Habit Tracker application
Centralizes database and application settings
"""
import os
from pathlib import Path

# Database Configuration
DATABASE_CONFIG = {
    'server': 'localhost\\SQLEXPRESS',
    'database': 'HabitTrackerDB',
    'driver': 'ODBC Driver 17 for SQL Server',
    'use_windows_auth': True,
    'trust_server_certificate': True
}

# Application Configuration
APP_CONFIG = {
    'default_user': 'demo_user',
    'default_analysis_period_days': 28,
    'max_habits_per_user': 50,
    'supported_periods': ['daily', 'weekly']
}

# Path Configuration
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_ROOT = Path(__file__).parent
DB_SCRIPTS_PATH = PROJECT_ROOT / 'backend_and_DB_setup' / 'mssql-express' / 'scripts'

# CLI Configuration
CLI_CONFIG = {
    'console_width': 120,
    'table_min_width': 80,
    'enable_colors': True,
    'show_help_on_start': False
}

# Analytics Configuration
ANALYTICS_CONFIG = {
    'default_trend_weeks': 4,
    'min_data_points_for_trend': 3,
    'streak_bonus_threshold': 7,  # Days for streak bonus calculation
    'completion_rate_excellent_threshold': 90,
    'completion_rate_good_threshold': 70,
    'completion_rate_needs_improvement_threshold': 50
}

def get_database_connection_string() -> str:
    """Get the database connection string"""
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
    """Get the path to database scripts"""
    return DB_SCRIPTS_PATH

def is_development_mode() -> bool:
    """Check if running in development mode"""
    return os.getenv('HABIT_TRACKER_ENV', 'development').lower() == 'development'
