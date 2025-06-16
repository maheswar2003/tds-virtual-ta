#!/usr/bin/env python3
"""
Test script to verify evaluation compatibility
Run this to ensure all API endpoints work exactly as instructors expect
"""

import requests
import json

def test_api_endpoint(base_url):
    """Test the main /api/ endpoint"""
    print("🧪 Testing /api/ endpoint...")
    
    test_data = {
        "question": "Should I use gpt-4o-mini or gpt-3.5-turbo?"
    }
    
    try:
        response = requests.post(f"{base_url}/api/", 
                               json=test_data,
                               headers={"Content-Type": "application/json"},
                               timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ /api/ endpoint working correctly")
            print(f"Has 'answer' field: {'answer' in data}")
            print(f"Has 'links' field: {'links' in data}")
            print(f"Answer preview: {data.get('answer', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ /api/ endpoint failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ /api/ endpoint error: {e}")
        return False

def test_root_post(base_url):
    """Test POST to root (/) - evaluators might test this"""
    print("\n🧪 Testing POST to / (root)...")
    
    test_data = {
        "question": "Test question"
    }
    
    try:
        response = requests.post(f"{base_url}/", 
                               json=test_data,
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Root POST working correctly")
            print(f"Has 'answer' field: {'answer' in data}")
            print(f"Has 'status' field: {'status' in data}")
            return True
        else:
            print(f"❌ Root POST failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Root POST error: {e}")
        return False

def test_health_endpoint(base_url):
    """Test health check endpoint"""
    print("\n🧪 Testing /health endpoint...")
    
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working correctly")
            print(f"Status: {data.get('status', 'N/A')}")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_root_get(base_url):
    """Test GET to root (/) - should now return HTML"""
    print("\n🧪 Testing GET to / (root)...")
    
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content Type: {response.headers.get('content-type', 'N/A')}")
        
        if response.status_code == 200:
            if 'text/html' in response.headers.get('content-type', ''):
                print("✅ Root GET returns HTML (new beautiful interface)")
                print(f"Contains 'TDS Virtual TA': {'TDS Virtual TA' in response.text}")
                return True
            else:
                print("ℹ️ Root GET returns non-HTML (old JSON interface)")
                return True
        else:
            print(f"❌ Root GET failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Root GET error: {e}")
        return False

def main():
    print("🔍 TDS Virtual TA - Evaluation Compatibility Test")
    print("=" * 50)
    
    # Test with your Render URL when deployed
    base_url = input("Enter your app URL (e.g., https://your-app.onrender.com): ").strip()
    if not base_url:
        print("❌ No URL provided")
        return
    
    # Remove trailing slash
    base_url = base_url.rstrip('/')
    
    print(f"\n🎯 Testing: {base_url}")
    print("=" * 50)
    
    # Run all tests
    tests = [
        test_health_endpoint,
        test_api_endpoint, 
        test_root_post,
        test_root_get
    ]
    
    results = []
    for test in tests:
        results.append(test(base_url))
    
    print("\n📊 SUMMARY")
    print("=" * 50)
    
    critical_tests = results[:3]  # Health, API, Root POST
    if all(critical_tests):
        print("✅ ALL CRITICAL EVALUATION ENDPOINTS WORKING")
        print("✅ Instructors' automated testing will work perfectly")
        print("✅ Safe to deploy!")
    else:
        print("❌ SOME CRITICAL ENDPOINTS FAILED")
        print("❌ DO NOT DEPLOY - Fix issues first")
    
    if results[3]:  # Root GET
        print("✅ Beautiful web interface working")
    else:
        print("⚠️ Web interface has issues (but evaluation still works)")

if __name__ == "__main__":
    main() 