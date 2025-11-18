"""
Setup script for Hotel Booking and Room Management System
Helps initialize the database and create an admin user
"""
import os
import sys

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import mysql.connector
        print("✓ mysql-connector-python is installed")
    except ImportError:
        print("✗ mysql-connector-python is not installed")
        print("  Run: pip install -r requirements.txt")
        return False
    
    try:
        import pytest
        print("✓ pytest is installed")
    except ImportError:
        print("✗ pytest is not installed")
        print("  Run: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("⚠ .env file not found")
        print("  Copy .env.example to .env and configure your database settings")
        return False
    print("✓ .env file exists")
    return True

def test_database_connection():
    """Test database connection"""
    try:
        from app.services.db import get_connection
        with get_connection() as conn:
            print("✓ Database connection successful")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("  Make sure MySQL is running and credentials are correct")
        return False

def create_tables():
    """Create database tables"""
    try:
        from app.models.user import User
        User.create_table()
        print("✓ Database tables created successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to create tables: {e}")
        return False

def create_admin_user():
    """Create an admin user"""
    try:
        from app.services.auth import AuthService
        from app.models.user import User
        
        # Check if admin already exists
        admin = User.get_by_username('admin')
        if admin:
            print("⚠ Admin user already exists")
            return True
        
        # Create admin user
        AuthService.register('admin', 'admin123', 'Administrator')
        print("✓ Admin user created (username: admin, password: admin123)")
        print("  ⚠ Please change the admin password after first login!")
        return True
    except Exception as e:
        print(f"✗ Failed to create admin user: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("Hotel Booking System - Setup")
    print("=" * 60)
    print()
    
    print("Checking dependencies...")
    if not check_dependencies():
        print("\nSetup incomplete. Please install dependencies first.")
        sys.exit(1)
    
    print("\nChecking environment configuration...")
    if not check_env_file():
        print("\nSetup incomplete. Please configure .env file.")
        sys.exit(1)
    
    print("\nTesting database connection...")
    if not test_database_connection():
        print("\nSetup incomplete. Please check database configuration.")
        sys.exit(1)
    
    print("\nCreating database tables...")
    if not create_tables():
        print("\nSetup incomplete. Please check database permissions.")
        sys.exit(1)
    
    print("\nCreating admin user...")
    create_admin_user()
    
    print("\n" + "=" * 60)
    print("Setup completed successfully!")
    print("=" * 60)
    print("\nYou can now run the application with:")
    print("  python -m app.main")
    print()

if __name__ == '__main__':
    main()
