#!/usr/bin/env python
"""
Development server runner for Django API Gateway
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run the Django development server with proper setup"""
    
    # Set the Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # Add the current directory to Python path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    try:
        from django.core.management import execute_from_command_line
        from django.core.management.commands.runserver import Command as RunServerCommand
        
        # Check if migrations need to be run
        print("🔍 Checking database status...")
        try:
            execute_from_command_line(['manage.py', 'check', '--deploy'])
            print("✅ Database check passed")
        except SystemExit:
            print("⚠️  Running migrations...")
            execute_from_command_line(['manage.py', 'migrate'])
        
        # Print startup information
        print("\n" + "="*50)
        print("🚀 Django API Gateway Starting...")
        print("="*50)
        print("📱 Gateway URL: http://localhost:8000")
        print("📊 Admin Panel: http://localhost:8000/admin")
        print("🔍 Status Check: http://localhost:8000/status")
        print("📖 Health Check: http://localhost:8000/health")
        print("="*50)
        print("🎯 Sentiment Analysis Endpoints:")
        print("   POST /sentiment/predict/ - Basic sentiment")
        print("   POST /sentiment/analyze/ - Advanced emotion analysis")
        print("   POST /sentiment/analyze-light/ - Lightweight analysis")
        print("   POST /sentiment/moodify/ - Text transformation")
        print("="*50)
        print("💡 Press Ctrl+C to stop the server")
        print("="*50 + "\n")
        
        # Start the development server
        execute_from_command_line(['manage.py', 'runserver', '8000'])
        
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

if __name__ == '__main__':
    main()
