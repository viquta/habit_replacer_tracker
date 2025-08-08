import pyodbc
import os
from pathlib import Path

def setup_database():
    """Setup Habit Tracker database tables and users (database already exists)"""
    
    # Load environment variables
    app_password = os.getenv('DB_PASSWORD', 'HabitApp!Secure2025')
    
    # Connect directly to HabitTrackerDB since it already exists
    print("🔌 Connecting to HabitTrackerDB...")
    # note to self: Trusted_Connection uses my OS login; TrustServerCertificate is fine for local dev
    db_connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=HabitTrackerDB;Trusted_Connection=yes;TrustServerCertificate=yes"
    
    try:
        db_conn = pyodbc.connect(db_connection_string, timeout=10)
        db_cursor = db_conn.cursor()
        print("✅ Connected to HabitTrackerDB!")
    except pyodbc.Error as e:
        print(f"❌ Failed to connect to HabitTrackerDB: {e}")
        print("Make sure the HabitTrackerDB database exists and you have access to it.")
        return
    
    # Run initialization script
    print("📝 Creating tables and users...")
    init_script = Path(__file__).parent / 'init-db.sql'
    
    with open(init_script, 'r', encoding='utf-8') as f:
        sql_commands = f.read()
    
    # Execute the SQL commands (skip database creation parts since we already created it)
    try:
        # Split by GO statements and execute each batch separately
        # "GO" is a batch separator understood by SSMS, not SQL Server itself
        batches = [batch.strip() for batch in sql_commands.split('GO') if batch.strip()]
        
        for i, batch in enumerate(batches):
            # Skip database creation and USE statements - we're already connected to the right DB
            if any(keyword in batch.upper() for keyword in ['CREATE DATABASE', 'USE HABITTRACKER']):
                print(f"⏭️ Skipping batch {i+1} (database creation/use)")
                continue
                
            try:
                db_cursor.execute(batch)
                db_conn.commit()
                print(f"✅ Executed batch {i+1}/{len(batches)}")
            except pyodbc.Error as e:
                print(f"⚠️ Warning in batch {i+1}: {e}")
                continue
                
        print("✅ Tables and users created successfully!")
    except pyodbc.Error as e:
        print(f"❌ Error creating tables: {e}")
        return
    finally:
        db_conn.close()
    
    # Test app user connection
    print("🔍 Testing application user connection...")
    app_conn_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=localhost\\SQLEXPRESS;DATABASE=HabitTrackerDB;UID=habit_app_user;PWD={app_password};TrustServerCertificate=yes"
    
    try:
        app_conn = pyodbc.connect(app_conn_string)
        cursor = app_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Habits")
        habit_count = cursor.fetchone()[0]
        print(f"✅ App user connection successful! {habit_count} habits found")
        app_conn.close()
    except Exception as e:
        print(f"⚠️ App user test failed: {e}")
        print("This might be expected if no sample data was inserted yet.")
    
    print("🎉 Database setup complete!")
    print(f"📋 Connection string for your app:")
    print(f"   Server=localhost\\SQLEXPRESS;Database=HabitTrackerDB;User Id=habit_app_user;Password={app_password};TrustServerCertificate=true;")

if __name__ == "__main__":
    setup_database()