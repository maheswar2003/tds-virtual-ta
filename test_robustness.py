#!/usr/bin/env python3
"""
Robustness test with completely different questions to verify 
the system works on ANY question, not just hardcoded test cases.
"""

from src.new_processor import SmartQuestionProcessor
from src.refined_responder import RefinedVirtualTAResponder

def test_robustness_with_novel_questions():
    """Test with completely different questions not used in development."""
    
    processor = SmartQuestionProcessor()
    responder = RefinedVirtualTAResponder()
    
    # COMPLETELY DIFFERENT QUESTIONS - never used in development/testing
    novel_questions = [
        # Variations of model questions
        "Which LLM should I choose for my TDS project?",
        "Is ChatGPT-4 better than GPT-3.5 for this course?",
        "What's the difference between different OpenAI models?",
        
        # Different container questions  
        "Can I use Docker instead of Podman?",
        "How do I run containers on my Windows machine?",
        "What container technology is recommended?",
        
        # Different course questions
        "How many credits is this course?",
        "What topics are covered in TDS?",
        "Is programming experience required?",
        
        # Different exam questions
        "What's the format of the final exam?",
        "How are grades calculated?",
        "Are there any midterm exams?",
        
        # Different tool questions
        "How do I set up my development environment?",
        "What text editor should I use?",
        "How do I handle CSV files?",
        
        # Completely different domains
        "How do I analyze social media data?",
        "What's the best way to visualize time series?",
        "How do I clean messy datasets?",
        "What's the difference between supervised and unsupervised learning?",
        
        # Edge cases
        "Can you help me with my homework?",
        "What's the weather like?",
        "How do I cook pasta?",
        "What's 2+2?",
        "Tell me a joke about data science"
    ]
    
    print("ROBUSTNESS TEST - Novel Questions Never Used in Development")
    print("=" * 80)
    print("Testing if system is truly robust or just optimized for test cases...")
    print()
    
    for i, question in enumerate(novel_questions, 1):
        print(f"{i}. Question: {question}")
        print("-" * 60)
        
        # Process question
        processed = processor.process_question(question)
        category = processed.get('category', 'unknown')
        concepts = processed.get('concepts', set())
        
        print(f"Category: {category}")
        print(f"Concepts: {list(concepts)}")
        
        # Get response
        response = responder.generate_response(processed)
        answer = response.get('answer', 'No answer')
        links = response.get('links', [])
        
        print(f"Answer: {answer}")
        print(f"Links: {len(links)} found")
        
        # Analyze quality
        is_relevant = "course" in answer.lower() or "tds" in answer.lower() or len(links) > 0
        is_coherent = len(answer.split()) > 3 and answer.endswith(('.', '!', '?'))
        
        print(f"Quality: Relevant={is_relevant}, Coherent={is_coherent}")
        
        if links:
            top_link = links[0]
            print(f"Top Link: [{top_link.get('score', 0):.1f}] {top_link.get('title', 'No title')[:40]}...")
        
        print()

def analyze_pattern_dependency():
    """Analyze if the system relies too heavily on hardcoded patterns."""
    
    processor = SmartQuestionProcessor()
    
    print("PATTERN DEPENDENCY ANALYSIS")
    print("=" * 50)
    
    # Test questions that don't match any specific patterns
    edge_cases = [
        "I'm confused about the assignment",
        "Need help with data cleaning",
        "Struggling with the course material",
        "Can't understand the documentation",
        "Having trouble with my project"
    ]
    
    for question in edge_cases:
        processed = processor.process_question(question)
        category = processed.get('category', 'unknown')
        concepts = processed.get('concepts', set())
        
        print(f"Question: {question}")
        print(f"Category: {category} | Concepts: {list(concepts)}")
        print()

def test_keyword_extraction_robustness():
    """Test if keyword extraction works for various question formats."""
    
    processor = SmartQuestionProcessor()
    
    print("KEYWORD EXTRACTION ROBUSTNESS")
    print("=" * 50)
    
    # Different ways to ask about the same thing
    model_questions = [
        "Should I use gpt-4o-mini or gpt-3.5-turbo?",
        "Which model is better: 4o-mini or 3.5-turbo?",
        "What about using GPT 3.5 instead of GPT 4o?",
        "gpt-3.5-turbo vs gpt-4o-mini which one?",
        "Model selection for OpenAI API"
    ]
    
    for question in model_questions:
        processed = processor.process_question(question)
        concepts = processed.get('concepts', set())
        category = processed.get('category', 'unknown')
        
        print(f"Q: {question}")
        print(f"Concepts: {list(concepts)} | Category: {category}")
        print()

if __name__ == "__main__":
    test_robustness_with_novel_questions()
    analyze_pattern_dependency()
    test_keyword_extraction_robustness() 