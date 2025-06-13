#!/usr/bin/env python3
"""
Tests for TDS Virtual TA API endpoints
"""

import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestTDSVirtualTAAPI(unittest.TestCase):
    """Test cases for TDS Virtual TA API"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_index_endpoint(self):
        """Test index endpoint"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('name', data)
        self.assertEqual(data['name'], 'TDS Virtual TA')
    
    def test_api_endpoint_valid_question(self):
        """Test API endpoint with valid question"""
        question_data = {
            "question": "Should I use gpt-4o-mini or gpt-3.5-turbo for the assignment?"
        }
        
        response = self.app.post('/api/', 
                                data=json.dumps(question_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('answer', data)
        self.assertIn('links', data)
        self.assertIsInstance(data['links'], list)
    
    def test_api_endpoint_missing_question(self):
        """Test API endpoint with missing question"""
        response = self.app.post('/api/', 
                                data=json.dumps({}),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_api_endpoint_invalid_json(self):
        """Test API endpoint with invalid JSON"""
        response = self.app.post('/api/', 
                                data='invalid json',
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_api_endpoint_with_image(self):
        """Test API endpoint with image data"""
        question_data = {
            "question": "What does this image show?",
            "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        }
        
        response = self.app.post('/api/', 
                                data=json.dumps(question_data),
                                content_type='application/json')
        
        # Should not fail even with image processing
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('answer', data)
        self.assertIn('links', data)

if __name__ == '__main__':
    unittest.main() 