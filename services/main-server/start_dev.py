#!/usr/bin/env python
"""
Start both Django API Gateway and Flask microservice for development
"""
import subprocess
import time
import sys
import os
from pathlib import Path

# Get project paths
main_server_path = Path(__file__).resolve().parent
flask_service_path = main_server_path.parent.parent / "flask-microservice"

def start_flask_service():
    """Start the Flask microservice"""
    print("🚀 Starting Flask microservice...")
    os.chdir(flask_service_path)
    
    # Try to start Flask with lightweight models only
    env = os.environ.copy()
    env['LIGHTWEIGHT_ONLY'] = 'true'
    
    flask_process = subprocess.Popen([
        sys.executable, "start_lightweight.py"
    ], env=env)
    
    print(f"📡 Flask service started (PID: {flask_process.pid})")
    return flask_process

def start_django_gateway():
    """Start the Django API gateway"""
    print("🚀 Starting Django API Gateway...")
    os.chdir(main_server_path)
    
    # Activate virtual environment and start Django
    venv_python = main_server_path / "venv" / "bin" / "python"
    
    django_process = subprocess.Popen([
        str(venv_python), "manage.py", "runserver", "8000"
    ])
    
    print(f"🌐 Django API Gateway started (PID: {django_process.pid})")
    return django_process

def main():
    """Start both services"""
    print("🎭 Starting Moodify Development Environment")
    print("=" * 50)
    
    try:
        # Start Flask first
        flask_process = start_flask_service()
        time.sleep(3)  # Give Flask time to start
        
        # Start Django
        django_process = start_django_gateway()
        time.sleep(2)  # Give Django time to start
        
        print("\n✅ Both services started successfully!")
        print("\n📍 Available endpoints:")
        print("   🌐 Django API Gateway: http://localhost:8000")
        print("   📡 Flask Microservice:  http://localhost:5000")
        print("\n🧪 Test endpoints:")
        print("   GET  http://localhost:8000/")
        print("   GET  http://localhost:8000/api/health/")
        print("   POST http://localhost:8000/api/sentiment/")
        print("   GET  http://localhost:8000/api/flask-health/")
        print("   GET  http://localhost:8000/api/core/info/")
        
        print("\n⚠️  Press Ctrl+C to stop both services")
        
        # Wait for user to stop
        try:
            flask_process.wait()
            django_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping services...")
            flask_process.terminate()
            django_process.terminate()
            flask_process.wait()
            django_process.wait()
            print("✅ Services stopped")
            
    except Exception as e:
        print(f"❌ Error starting services: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
