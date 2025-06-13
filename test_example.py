#!/usr/bin/env python3
"""
Example script to test the TDS Virtual TA API
"""

import requests
import json
import base64

def test_api_local():
    """Test the API running locally"""
    url = "http://localhost:5000/api/"
    
    # Test basic question
    test_data = {
        "question": "Should I use gpt-4o-mini which AI proxy supports, or gpt-3.5-turbo?"
    }
    
    try:
        response = requests.post(url, json=test_data, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.RequestException as e:
        print(f"Error testing API: {e}")

def test_api_remote(api_url):
    """Test the API running on a remote server"""
    url = f"{api_url}/api/"
    
    # Test question with sample base64 image (1x1 pixel PNG)
    sample_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    test_data = {
        "question": "Should I use gpt-4o-mini which AI proxy supports, or gpt-3.5-turbo?",
        "image": sample_image
    }
    
    try:
        response = requests.post(url, json=test_data, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.RequestException as e:
        print(f"Error testing API: {e}")

def test_health_check(api_url="http://localhost:5000"):
    """Test health check endpoint"""
    url = f"{api_url}/health"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Health Check Status: {response.status_code}")
        print(f"Health Response: {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.RequestException as e:
        print(f"Error checking health: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        api_url = sys.argv[1]
        print(f"Testing remote API at: {api_url}")
        test_health_check(api_url)
        test_api_remote(api_url)
    else:
        print("Testing local API at: http://localhost:5000")
        test_health_check()
        test_api_local()
    
    print("\nExample curl command:")
    print('curl "http://localhost:5000/api/" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"question": "Should I use gpt-4o-mini or gpt-3.5-turbo?"}\'') 