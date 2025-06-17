#!/usr/bin/env python3
"""
Test script for the new improved TDS Virtual TA system.
"""

import json
import os
from src.new_processor import SmartQuestionProcessor
from src.new_responder import SmartVirtualTAResponder

def test_new_system():
    """Test the new system with comprehensive questions."""
    
    # Initialize new components
    processor = SmartQuestionProcessor()
    responder = SmartVirtualTAResponder()
    
    # Comprehensive test questions
    test_questions = [
        # GPT/API questions
        "Should I use gpt-4o-mini or gpt-3.5-turbo for TDS?",
        "What model should I use for the TDS course?",
        "Which OpenAI API model is recommended?",
        
        # Container questions
        "How to use podman on Windows?",
        "What is the difference between Docker and Podman?",
        "How to install podman on Windows?",
        
        # GA4/Bonus questions
        "How to score bonus marks in GA4 dashboard?",
        "What is GA4 dashboard project?",
        "How to get bonus points?",
        
        # Exam questions
        "When is the exam?",
        "What is the exam schedule?",
        "When is the final exam?",
        
        # Course structure questions
        "What are the course prerequisites?",
        "What is the course structure?",
        "How is the grading done?",
        
        # Tools questions
        "How to use VS Code for data science?",
        "What is Unicode and why is it important?",
        "How to scrape data with Python?",
        "What development tools are covered?",
        
        # General questions
        "What is TDS course about?",
        "How difficult is the course?",
        "What programming languages are used?"
    ]
    
    print("Testing NEW TDS Virtual TA System")
    print("=" * 60)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        print("-" * 40)
        
        # Process question with new processor
        processed = processor.process_question(question)
        print(f"Category: {processed.get('category', 'unknown')}")
        print(f"Concepts: {list(processed.get('concepts', set()))}")
        
        # Get response from new responder
        response = responder.generate_response(processed)
        
        answer = response.get('answer', 'No answer')
        print(f"Answer: {answer}")
        
        links = response.get('links', [])
        print(f"Links: {len(links)} found")
        
        # Show links with scores
        for j, link in enumerate(links[:2], 1):
            title = link.get('title', 'No title')
            score = link.get('score', 0)
            url = link.get('url', 'No URL')
            print(f"  {j}. [{score:.1f}] {title[:60]}...")
            print(f"     URL: {url}")
        
        print()

def compare_systems():
    """Compare old vs new system on sample questions."""
    
    # Initialize both systems
    from src.processor import QuestionProcessor
    from src.responder import VirtualTAResponder
    
    old_processor = QuestionProcessor()
    old_responder = VirtualTAResponder()
    
    new_processor = SmartQuestionProcessor()
    new_responder = SmartVirtualTAResponder()
    
    # Sample questions for comparison
    comparison_questions = [
        "Should I use gpt-4o-mini or gpt-3.5-turbo?",
        "How to use podman on Windows?",
        "What are the course prerequisites?",
        "When is the exam?",
        "How to score bonus marks in GA4?"
    ]
    
    print("\nCOMPARISON: OLD vs NEW System")
    print("=" * 60)
    
    for i, question in enumerate(comparison_questions, 1):
        print(f"\n{i}. Question: {question}")
        print("=" * 40)
        
        # Old system
        print("OLD SYSTEM:")
        old_processed = old_processor.process_question(question)
        old_response = old_responder.generate_response(old_processed)
        print(f"Answer: {old_response.get('answer', 'No answer')[:100]}...")
        print(f"Links: {len(old_response.get('links', []))}")
        
        print("\nNEW SYSTEM:")
        new_processed = new_processor.process_question(question)
        new_response = new_responder.generate_response(new_processed)
        print(f"Answer: {new_response.get('answer', 'No answer')}")
        print(f"Links: {len(new_response.get('links', []))}")
        if new_response.get('links'):
            best_link = new_response['links'][0]
            print(f"Best: [{best_link.get('score', 0):.1f}] {best_link.get('title', 'No title')[:50]}...")
        
        print("-" * 40)

if __name__ == "__main__":
    test_new_system()
    compare_systems() 