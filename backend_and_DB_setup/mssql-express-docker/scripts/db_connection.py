"""
Database connection module for Habit Tracker app
"""
import pyodbc
import os

def get_connection():
    """Get a connection to the HabitTracker database using Windows Authentication"""
    
    # Connection parameters
    server = "localhost\\SQLEXPRESS"
    database = "HabitTrackerDB"
    
    # Use Windows Authentication (more reliable for local development)
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate=yes"
    )
    
    try:
        connection = pyodbc.connect(connection_string)
        return connection
    except pyodbc.Error as e:
        print(f"Database connection failed: {e}")
        raise

def test_connection():
    """Test the database connection"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT COUNT(*) as table_count FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
        result = cursor.fetchone()
        table_count = result[0]
        
        print(f"✅ Database connection successful!")
        print(f"📊 Found {table_count} tables in HabitTrackerDB")
        
        # Test a simple query on the Habits table
        try:
            cursor.execute("SELECT COUNT(*) FROM Habits")
            habit_count = cursor.fetchone()[0]
            print(f"🎯 Habits table has {habit_count} records")
        except pyodbc.Error:
            print("⚠️ Habits table not accessible (this might be expected if setup hasn't run)")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
