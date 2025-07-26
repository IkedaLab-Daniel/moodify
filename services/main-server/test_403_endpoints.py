#!/usr/bin/env python3
"""
Test script to verify that 403 Forbidden errors are resolved
"""

import requests
import json
import sys

def test_endpoint(url, method='GET', data=None, description=""):
    """Test a single endpoint and report results"""
    try:
        if method.upper() == 'GET':
            response = requests.get(url, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'}, timeout=10)
        else:
            print(f"   ❌ Unsupported method: {method}")
            return False
            
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ {description} - SUCCESS")
            try:
                resp_data = response.json()
                print(f"   Response: {json.dumps(resp_data, indent=2)[:200]}...")
            except:
                print(f"   Response: {response.text[:200]}...")
            return True
        elif response.status_code == 403:
            print(f"   ❌ {description} - STILL GETTING 403 FORBIDDEN")
            print(f"   Response: {response.text}")
            return False
        elif response.status_code == 503:
            print(f"   ⚠️  {description} - Service unavailable (Flask not running)")
            return True  # This is expected if Flask is down
        else:
            print(f"   ⚠️  {description} - Unexpected status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ {description} - Cannot connect to Django server")
        return False
    except Exception as e:
        print(f"   ❌ {description} - Error: {e}")
        return False

def main():
    """Test all endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Moodify API Endpoints for 403 Fix")
    print("=" * 60)
    
    tests = [
        # Basic Django functionality
        (f"{base_url}/", "GET", None, "Root endpoint"),
        
        # Simple Django view (non-DRF)
        (f"{base_url}/api/simple-health/", "GET", None, "Simple Django health check"),
        
        # DRF endpoints
        (f"{base_url}/api/health/", "GET", None, "DRF health check"),
        (f"{base_url}/api/test/", "GET", None, "DRF test endpoint (GET)"),
        (f"{base_url}/api/test/", "POST", {"test": "data"}, "DRF test endpoint (POST)"),
        
        # Flask proxy endpoints
        (f"{base_url}/api/flask-health/", "GET", None, "Flask health proxy"),
        (f"{base_url}/api/sentiment/", "POST", {"text": "I am happy"}, "Sentiment analysis"),
        (f"{base_url}/api/predict/", "POST", {"text": "I am happy"}, "Predict endpoint"),
    ]
    
    success_count = 0
    total_tests = len(tests)
    
    for i, (url, method, data, description) in enumerate(tests, 1):
        print(f"\n{i}. Testing {description}...")
        print(f"   URL: {method} {url}")
        if test_endpoint(url, method, data, description):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 All tests passed! 403 errors are resolved.")
    elif success_count > 0:
        print("⚠️  Some tests passed, but issues remain.")
    else:
        print("❌ All tests failed. Check Django server and configuration.")
    
    print("\n🔧 Quick manual test commands:")
    print(f"curl -X GET {base_url}/api/simple-health/")
    print(f"curl -X GET {base_url}/api/health/")
    print(f"curl -X GET {base_url}/api/flask-health/")
    
    return success_count == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
