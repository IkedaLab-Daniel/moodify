#!/usr/bin/env python3
"""
Test script to verify the 403 Forbidden issue is fixed
Run this after restartin    print()
    print("🎯 Quick Test Commands:")
    print(f"""
# Test with curl:
curl -X GET {base_url}/api/health/

# Test simple endpoint first:
curl -X POST {base_url}/api/test/ \\
  -H "Content-Type: application/json" \\
  -d '{{"test": "data"}}'

# Test sentiment analysis:
curl -X POST {base_url}/api/sentiment/ \\
  -H "Content-Type: application/json" \\
  -d '{{"text": "This is amazing!"}}'

# Test with httpie (if installed):
http GET {base_url}/api/health/
http POST {base_url}/api/test/ test=data
http POST {base_url}/api/sentiment/ text="This is wonderful!"
""")
    
    print("🔧 If you're still getting 403 errors:")
    print("1. Restart your Django server: python manage.py runserver 8000")
    print("2. Try the /api/test/ endpoint first - it should definitely work")
    print("3. Check Django logs for specific error messages")erver
"""

import requests
import json

def test_endpoints():
    """Test the API endpoints that were giving 403 errors"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Moodify API Gateway Endpoints")
    print("=" * 50)
    
    # Test 1: Health check (GET)
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/api/health/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Health check passed")
        else:
            print(f"   ❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    print()
    
    # Test 2: Simple test endpoint (POST)
    print("2. Testing simple test endpoint...")
    try:
        data = {"test": "data"}
        response = requests.post(
            f"{base_url}/api/test/",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Test endpoint passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Test endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    print()
    
    # Test 3: Sentiment analysis (POST)
    print("3. Testing sentiment analysis...")
    try:
        data = {"text": "I love this API gateway!"}
        response = requests.post(
            f"{base_url}/api/sentiment/",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Sentiment analysis passed")
            print(f"   Response: {response.json()}")
        elif response.status_code == 503:
            print("   ⚠️  Flask service not running (expected if Flask is down)")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Sentiment analysis failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    print()
    
    # Test 4: Alternative sentiment endpoint
    print("4. Testing alternative sentiment endpoint (/api/predict/)...")
    try:
        data = {"text": "This is a test message"}
        response = requests.post(
            f"{base_url}/api/predict/",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Alternative endpoint passed")
        elif response.status_code == 503:
            print("   ⚠️  Flask service not running (expected if Flask is down)")
        else:
            print(f"   ❌ Alternative endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    print()
    
    # Test 5: Root endpoint
    print("5. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Root endpoint passed")
        else:
            print(f"   ❌ Root endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    print()
    print("🎯 Quick Test Commands:")
    print(f"""
# Test with curl:
curl -X GET {base_url}/api/health/

curl -X POST {base_url}/api/sentiment/ \\
  -H "Content-Type: application/json" \\
  -d '{{"text": "I am so happy today!"}}'

# Test with httpie (if installed):
http GET {base_url}/api/health/
http POST {base_url}/api/sentiment/ text="This is wonderful!"
""")

if __name__ == "__main__":
    test_endpoints()
