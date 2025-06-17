#!/usr/bin/env python3
"""
Test script to verify the Flask app integration with new system.
"""

import json
from app import app

def test_api_endpoints():
    """Test the API endpoints directly without starting server."""
    
    print("Testing Flask App Integration")
    print("=" * 50)
    
    # Test the main API endpoint
    test_questions = [
        "Should I use gpt-4o-mini or gpt-3.5-turbo for TDS?",
        "How to use podman on Windows?",
        "What are the course prerequisites?",
        "When is the exam?",
        "How to score bonus marks in GA4?"
    ]
    
    with app.test_client() as client:
        for i, question in enumerate(test_questions, 1):
            print(f"\n{i}. Testing: {question}")
            print("-" * 30)
            
            response = client.post('/api/', 
                                 json={"question": question},
                                 content_type='application/json')
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.get_json()
                answer = data.get('answer', 'No answer')
                links = data.get('links', [])
                
                print(f"Answer: {answer[:100]}...")
                print(f"Links: {len(links)} found")
                
                if links:
                    top_link = links[0]
                    print(f"Top Link: {top_link.get('title', 'No title')[:40]}...")
            else:
                print(f"Error: {response.get_json()}")
    
    print("\nFlask App Integration Test Complete!")

def test_health_endpoint():
    """Test health endpoint."""
    
    with app.test_client() as client:
        response = client.get('/health')
        print(f"\nHealth Check: {response.status_code}")
        if response.status_code == 200:
            print(f"Health Data: {response.get_json()}")

def test_home_endpoint():
    """Test home endpoint."""
    
    with app.test_client() as client:
        # Test GET request
        response = client.get('/')
        print(f"\nHome GET: {response.status_code}")
        
        # Test POST request
        response = client.post('/', json={"test": "data"})
        print(f"Home POST: {response.status_code}")
        if response.status_code == 200:
            print(f"Home POST Response: {response.get_json()}")

if __name__ == "__main__":
    test_health_endpoint()
    test_home_endpoint()
    test_api_endpoints() 