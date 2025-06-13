#!/usr/bin/env python3
"""
Simple test script to verify the TDS Virtual TA works
"""

import os
import sys

# Get API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("❌ Error: OPENAI_API_KEY environment variable not set")
    print("Please set it using: $env:OPENAI_API_KEY='your_api_key_here'")
    sys.exit(1)

try:
    # Test imports
    print("Testing imports...")
    from src.processor import QuestionProcessor
    from src.responder import VirtualTAResponder
    print("✅ Imports successful!")
    
    # Test processor
    print("\nTesting question processor...")
    processor = QuestionProcessor()
    question_data = processor.process_question("Should I use gpt-4o-mini or gpt-3.5-turbo?")
    print(f"✅ Question processed: {question_data['question_type']}")
    
    # Test responder
    print("\nTesting responder...")
    responder = VirtualTAResponder()
    response = responder.generate_response(question_data)
    print(f"✅ Response generated!")
    print(f"Answer: {response['answer'][:100]}...")
    print(f"Links: {len(response['links'])} links found")
    
    print("\n🎉 All components working correctly!")
    print("\nSample API response:")
    import json
    print(json.dumps(response, indent=2))
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 