#!/usr/bin/env python3
"""
TDS Virtual TA - Main Flask Application
Provides an API endpoint to answer student questions based on course content and Discourse posts.
"""

import os
import json
import base64
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from src.responder import VirtualTAResponder
from src.processor import QuestionProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize components
question_processor = QuestionProcessor()
responder = VirtualTAResponder()

@app.route('/api/', methods=['POST'])
def handle_question():
    """
    Handle student questions and return AI-generated responses with relevant links.
    
    Expected JSON payload:
    {
        "question": "Student question",
        "image": "base64_encoded_image (optional)"
    }
    
    Returns:
    {
        "answer": "Generated answer",
        "links": [
            {
                "url": "relevant_url",
                "text": "link_description"
            }
        ]
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({"error": "Question is required"}), 400
        
        question = data['question']
        image_data = data.get('image')
        
        logger.info(f"Received question: {question[:100]}...")
        
        # Process the question
        processed_question = question_processor.process_question(question, image_data)
        
        # Generate response
        response = responder.generate_response(processed_question)
        
        logger.info(f"Generated response with {len(response.get('links', []))} links")
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": "Failed to process question"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information"""
    return jsonify({
        "name": "TDS Virtual TA",
        "description": "Virtual Teaching Assistant for IIT Madras Tools in Data Science course",
        "endpoints": {
            "POST /api/": "Submit questions for AI responses",
            "GET /health": "Health check",
            "GET /": "This information"
        },
        "usage": {
            "method": "POST",
            "url": "/api/",
            "content_type": "application/json",
            "body": {
                "question": "Your question here",
                "image": "base64_encoded_image (optional)"
            }
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting TDS Virtual TA on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug) 