#!/usr/bin/env python3
"""
Test script for the refined TDS Virtual TA system.
"""

import json
import os
from src.new_processor import SmartQuestionProcessor
from src.refined_responder import RefinedVirtualTAResponder

def test_refined_system():
    """Test the refined system with focus on answer quality."""
    
    # Initialize refined components
    processor = SmartQuestionProcessor()
    responder = RefinedVirtualTAResponder()
    
    # Key test questions for evaluation
    test_questions = [
        "Should I use gpt-4o-mini or gpt-3.5-turbo for TDS?",
        "How to use podman on Windows?",
        "What are the course prerequisites?",
        "When is the exam?",
        "How to score bonus marks in GA4 dashboard?",
        "What is Unicode and why is it important?",
        "How difficult is the course?",
        "What programming languages are used in TDS?",
        "How to scrape data with Python?",
        "What is the difference between Docker and Podman?"
    ]
    
    print("Testing REFINED TDS Virtual TA System")
    print("=" * 70)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        print("-" * 50)
        
        # Process question
        processed = processor.process_question(question)
        print(f"Category: {processed.get('category', 'unknown')}")
        print(f"Concepts: {list(processed.get('concepts', set()))}")
        
        # Get refined response
        response = responder.generate_response(processed)
        
        answer = response.get('answer', 'No answer')
        print(f"Answer: {answer}")
        
        links = response.get('links', [])
        print(f"Links: {len(links)} found")
        
        # Show top link
        if links:
            top_link = links[0]
            print(f"Top Link: [{top_link.get('score', 0):.1f}] {top_link.get('title', 'No title')[:50]}...")
        
        print()

def evaluate_answer_quality():
    """Evaluate answer quality improvements."""
    
    from src.new_responder import SmartVirtualTAResponder
    from src.refined_responder import RefinedVirtualTAResponder
    
    processor = SmartQuestionProcessor()
    basic_responder = SmartVirtualTAResponder()
    refined_responder = RefinedVirtualTAResponder()
    
    evaluation_questions = [
        "Should I use gpt-4o-mini or gpt-3.5-turbo?",
        "How to use podman on Windows?",
        "What are the course prerequisites?",
        "When is the exam?",
        "How to score bonus marks in GA4?"
    ]
    
    print("\nANSWER QUALITY COMPARISON")
    print("=" * 70)
    
    for i, question in enumerate(evaluation_questions, 1):
        print(f"\n{i}. Question: {question}")
        print("=" * 50)
        
        processed = processor.process_question(question)
        
        # Basic system
        basic_response = basic_responder.generate_response(processed)
        basic_answer = basic_response.get('answer', 'No answer')
        
        # Refined system
        refined_response = refined_responder.generate_response(processed)
        refined_answer = refined_response.get('answer', 'No answer')
        
        print("BASIC SYSTEM:")
        print(f"Answer: {basic_answer}")
        print(f"Length: {len(basic_answer)} chars")
        
        print("\nREFINED SYSTEM:")
        print(f"Answer: {refined_answer}")
        print(f"Length: {len(refined_answer)} chars")
        
        # Simple quality metrics
        basic_complete = basic_answer.endswith(('.', '!', '?'))
        refined_complete = refined_answer.endswith(('.', '!', '?'))
        
        basic_capital = basic_answer and basic_answer[0].isupper()
        refined_capital = refined_answer and refined_answer[0].isupper()
        
        print(f"\nQuality Check:")
        print(f"Basic - Complete sentence: {basic_complete}, Proper capitalization: {basic_capital}")
        print(f"Refined - Complete sentence: {refined_complete}, Proper capitalization: {refined_capital}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_refined_system()
    evaluate_answer_quality() 