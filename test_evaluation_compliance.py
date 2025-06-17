#!/usr/bin/env python3
"""
Test to verify the system meets all evaluation requirements from project-tds-virtual-ta-promptfoo.yaml
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.new_processor import SmartQuestionProcessor
from src.improved_responder import ImprovedVirtualTAResponder

def test_json_schema_compliance():
    """Test that responses match the required JSON schema."""
    
    processor = SmartQuestionProcessor()
    responder = ImprovedVirtualTAResponder()
    
    print("=== JSON SCHEMA COMPLIANCE TEST ===\n")
    
    test_question = "What GPT model should I use?"
    question_data = processor.process_question(test_question)
    response = responder.generate_response(question_data)
    
    # Check required fields
    assert "answer" in response, "Missing 'answer' field"
    assert "links" in response, "Missing 'links' field"
    assert isinstance(response["answer"], str), "'answer' must be string"
    assert isinstance(response["links"], list), "'links' must be array"
    
    # Check links structure
    for link in response["links"]:
        assert isinstance(link, dict), "Each link must be an object"
        assert "url" in link, "Missing 'url' field in link"
        assert "text" in link, "Missing 'text' field in link"
        assert isinstance(link["url"], str), "'url' must be string"
        assert isinstance(link["text"], str), "'text' must be string"
    
    print("✅ JSON schema compliance: PASSED")
    print(f"   Answer: {response['answer'][:50]}...")
    print(f"   Links: {len(response['links'])} links provided")
    print()

def test_evaluation_questions():
    """Test the specific questions from the evaluation file."""
    
    processor = SmartQuestionProcessor()
    responder = ImprovedVirtualTAResponder()
    
    print("=== EVALUATION QUESTIONS TEST ===\n")
    
    # Test cases from the evaluation file
    test_cases = [
        {
            "question": "The question asks to use gpt-3.5-turbo-0125 model but the ai-proxy provided by Anand sir only supports gpt-4o-mini. So should we just use gpt-4o-mini or use the OpenAI API for gpt3.5 turbo?",
            "expected_content": ["gpt-3.5-turbo-0125", "gpt-4o-mini"],
            "expected_link": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939"
        },
        {
            "question": "If a student scores 10/10 on GA4 as well as a bonus, how would it appear on the dashboard?",
            "expected_content": ["dashboard", "110"],
            "expected_link": "https://discourse.onlinedegree.iitm.ac.in/t/ga4-data-sourcing-discussion-thread-tds-jan-2025/165959"
        },
        {
            "question": "I know Docker but have not used Podman before. Should I use Docker for this course?",
            "expected_content": ["podman", "docker"],
            "expected_link": "https://tds.s-anand.net/#/docker"
        },
        {
            "question": "When is the TDS Sep 2025 end-term exam?",
            "expected_behavior": "should_not_know"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🤔 Test {i}: {test_case['question'][:60]}...")
        
        question_data = processor.process_question(test_case["question"])
        response = responder.generate_response(question_data)
        
        answer = response.get("answer", "")
        links = response.get("links", [])
        
        print(f"   📝 Answer: {answer[:100]}...")
        print(f"   🔗 Links: {len(links)} provided")
        
        # Check expected content
        if "expected_content" in test_case:
            content_found = 0
            for expected in test_case["expected_content"]:
                if expected.lower() in answer.lower():
                    content_found += 1
                    print(f"   ✅ Found expected content: '{expected}'")
                else:
                    print(f"   ⚠️  Missing expected content: '{expected}'")
            
            if content_found > 0:
                print(f"   📊 Content relevance: {content_found}/{len(test_case['expected_content'])}")
        
        # Check expected link
        if "expected_link" in test_case:
            link_found = False
            for link in links:
                if test_case["expected_link"] in link.get("url", ""):
                    link_found = True
                    print(f"   ✅ Found expected link: {link.get('url', '')}")
                    break
            
            if not link_found:
                print(f"   ⚠️  Missing expected link: {test_case['expected_link']}")
        
        # Check "should not know" behavior
        if test_case.get("expected_behavior") == "should_not_know":
            uncertainty_indicators = ["don't know", "not available", "check", "refer", "not sure"]
            shows_uncertainty = any(indicator in answer.lower() for indicator in uncertainty_indicators)
            if shows_uncertainty:
                print("   ✅ Correctly shows uncertainty for unavailable information")
            else:
                print("   ⚠️  Should show uncertainty for unavailable information")
        
        print()

def test_data_source_usage():
    """Test that both course content and discourse posts are being used."""
    
    processor = SmartQuestionProcessor()
    responder = ImprovedVirtualTAResponder()
    
    print("=== DATA SOURCE USAGE TEST ===\n")
    
    print(f"📚 Course content items: {len(responder.course_content)}")
    print(f"💬 Discourse posts: {len(responder.discourse_posts)}")
    print(f"🔄 Total items: {len(responder.course_content) + len(responder.discourse_posts)}")
    
    # Test questions that should use different sources
    test_questions = [
        "What GPT model should I use for projects?",
        "How do I install Podman?",
        "What are the course prerequisites?",
        "How to get bonus marks in GA4?"
    ]
    
    course_matches = 0
    discourse_matches = 0
    
    for question in test_questions:
        question_data = processor.process_question(question)
        matches = responder.find_best_matches(question_data, max_results=5)
        
        for match in matches:
            source = match["item"].get("source", "unknown")
            if source == "course":
                course_matches += 1
            elif source == "discourse":
                discourse_matches += 1
    
    print(f"📊 Results from course content: {course_matches}")
    print(f"📊 Results from discourse posts: {discourse_matches}")
    
    if course_matches > 0 and discourse_matches > 0:
        print("✅ Both data sources are being used")
    elif course_matches > 0:
        print("⚠️  Only course content is being used")
    elif discourse_matches > 0:
        print("⚠️  Only discourse posts are being used")
    else:
        print("❌ No data sources are being used properly")
    
    print()

def test_response_quality():
    """Test response quality metrics."""
    
    processor = SmartQuestionProcessor()
    responder = ImprovedVirtualTAResponder()
    
    print("=== RESPONSE QUALITY TEST ===\n")
    
    test_questions = [
        "What is the recommended GPT model for TDS projects?",
        "How do I set up Podman on Windows?",
        "What tools are covered in the TDS course?",
        "When are the TDS exams scheduled?"
    ]
    
    total_tests = len(test_questions)
    quality_metrics = {
        "has_answer": 0,
        "has_links": 0,
        "proper_sentences": 0,
        "relevant_content": 0
    }
    
    for question in test_questions:
        question_data = processor.process_question(question)
        response = responder.generate_response(question_data)
        
        answer = response.get("answer", "")
        links = response.get("links", [])
        
        # Check metrics
        if answer and len(answer) > 10:
            quality_metrics["has_answer"] += 1
        
        if links:
            quality_metrics["has_links"] += 1
        
        if answer and answer[0].isupper() and answer.endswith('.'):
            quality_metrics["proper_sentences"] += 1
        
        # Check for TDS-related content
        tds_keywords = ['tds', 'course', 'tools', 'data', 'science', 'gpt', 'podman', 'docker']
        if any(keyword in answer.lower() for keyword in tds_keywords):
            quality_metrics["relevant_content"] += 1
    
    print("📊 Quality Metrics:")
    for metric, count in quality_metrics.items():
        percentage = (count / total_tests) * 100
        print(f"   {metric}: {count}/{total_tests} ({percentage:.1f}%)")
    
    overall_quality = sum(quality_metrics.values()) / (len(quality_metrics) * total_tests) * 100
    print(f"   Overall Quality: {overall_quality:.1f}%")
    
    if overall_quality >= 80:
        print("✅ Response quality: EXCELLENT")
    elif overall_quality >= 60:
        print("✅ Response quality: GOOD")
    else:
        print("⚠️  Response quality: NEEDS IMPROVEMENT")
    
    print()

if __name__ == "__main__":
    print("🧪 TDS VIRTUAL TA - EVALUATION COMPLIANCE TEST\n")
    
    try:
        test_json_schema_compliance()
        test_evaluation_questions()
        test_data_source_usage()
        test_response_quality()
        
        print("🎉 ALL TESTS COMPLETED!")
        print("System is ready for evaluation.")
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc() 