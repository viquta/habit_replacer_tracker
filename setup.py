#!/usr/bin/env python3
"""
Setup script for Habit Tracker Application
Installs dependencies and sets up the environment
"""

import subprocess # Think of it as a way to programmatically interact with your computer using Python instead of manually entering commands in the terminal. (from: geeksforgeeks)
import sys
import os
from pathlib import Path

def run_command(command, description): #command as in shell command, and description is for humans to read
    """This is a command runner wrapper that executes a shell command and handles errors
        Be sure to put shell=False in the future because it is a security risk --> shell injection attack
    """
    print(f"🔧 {description}...")
    try:
        #subprocess.run is used to execute the command
        #shell=True allows the command to be a string, which is useful for complex commands
        #check=True raises an error if the command fails
        #capture_output=True captures stdout and stderr for later use
        #text=True returns output as a string instead of bytes
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e: # Handle errors from subprocess.run
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}") #stdout is standard out
        if e.stderr:
            print(f"Error: {e.stderr}") #stderr is standard error
        return False

def check_python_version():
    """Check if Python version meets requirements"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 7: #pretty straightforward check
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("   Requires Python 3.7 or later")
        return False

def install_dependencies():
    """Install Python dependencies"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    # Use sys.executable to ensure we use the same Python interpreter's pip
    command = f'"{sys.executable}" -m pip install -r "{requirements_file}"'
    return run_command(command, "Installing Python dependencies")

def setup_database():
    """Set up the database"""
    print("\n📊 Database Setup")
    print("=" * 50)
    
    # Check if SQL Server is available
    print("ℹ️  Database setup requires:")
    print("   • SQL Server Express (LocalDB or instance) running")
    print("   • ODBC Driver 17 for SQL Server installed")
    print("   • Windows Authentication enabled")
    
    setup_db_script = Path(__file__).parent / "backend_and_DB_setup" / "mssql-express" / "scripts" / "setup_db.py"
    
    if setup_db_script.exists(): #basically, if it finds the setup_db.py script it executes it 
        choice = input("\n🔍 Run database setup script? [y/N]: ").lower()
        if choice == 'y':
            command = f'"{sys.executable}" "{setup_db_script}"'
            return run_command(command, "Setting up database")
    else:
        print("⚠️  Database setup script not found")
        print(f"   Expected: {setup_db_script}")
    
    return True

def test_setup():
    """Test the setup"""
    print("\n🧪 Testing Setup")
    print("=" * 50)
    
    # Test database connection
    try:
        # Add the database scripts path to sys.path
        db_scripts_path = str(Path(__file__).parent / "backend_and_DB_setup" / "mssql-express" / "scripts")
        if db_scripts_path not in sys.path:
            sys.path.insert(0, db_scripts_path)
        
        # Import and test database connection
        # Note: This import may show as unresolved in IDEs due to dynamic path manipulation
        import db_connection
        if db_connection.test_connection():
            print("✅ Database connection test passed")
        else:
            print("❌ Database connection test failed")
            return False
    except ImportError as e:
        print(f"⚠️  Could not import database module: {e}")
        print("   Database functionality may not work")
    except Exception as e:
        print(f"⚠️  Database test error: {e}")
        print("   This is expected if the database is not set up yet")
    
    # Test backend imports
    try:
        # Add the current directory to sys.path to ensure backend can be imported
        project_root = str(Path(__file__).parent)
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
            
        from backend.services import SystemService
        system_service = SystemService()
        status = system_service.get_system_status()
        if status['system_initialized']:
            print("✅ Backend services test passed")
        else:
            print("❌ Backend services test failed")
            return False
    except ImportError as e:
        print(f"❌ Backend import failed: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Backend test error: {e}")
        print("   This may be expected if the database is not fully configured")
    
    return True

def main():
    """Main setup function"""
    print("🌟 Habit Tracker Application Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print("\n📦 Installing Dependencies")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup database
    setup_database()
    
    # Test setup
    if test_setup():
        print("\n🎉 Setup completed successfully!")
        print("\n📖 Next steps:")
        print("   1. Ensure SQL Server Express is running")
        print("   2. Run the database setup script if not done already")
        print("   3. Start the application with: python CLI.py")
        print("\n💡 For help, run: python CLI.py --help")
    else:
        print("\n⚠️  Setup completed with warnings")
        print("   Some features may not work properly")
        print("   Check the error messages above for details")

if __name__ == "__main__":
    main()
