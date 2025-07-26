#!/usr/bin/env python
"""
Test script to verify Django API Gateway setup
"""
import os
import sys
import requests
import subprocess
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

def test_django_setup():
    """Test if Django is properly set up"""
    try:
        from django.core.management import execute_from_command_line
        print("✅ Django setup successful")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def test_apps_import():
    """Test if all apps can be imported"""
    try:
        from apps.authentication.models import User, UserProfile
        from apps.api.views import health_check
        from apps.core.views import status_view
        print("✅ All apps imported successfully")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def test_database():
    """Test database connection"""
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_user_model():
    """Test custom user model"""
    try:
        from apps.authentication.models import User
        user_count = User.objects.count()
        print(f"✅ User model working - {user_count} users in database")
        return True
    except Exception as e:
        print(f"❌ User model test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Django API Gateway Setup")
    print("=" * 50)
    
    tests = [
        test_django_setup,
        test_apps_import, 
        test_database,
        test_user_model,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Django API Gateway is ready.")
        print("\nNext steps:")
        print("1. Start the server: python manage.py runserver")
        print("2. Visit http://localhost:8000/api/core/status/")
        print("3. Test authentication at http://localhost:8000/api/auth/")
    else:
        print("❌ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
