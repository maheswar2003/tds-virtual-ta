#!/usr/bin/env python3
"""
Question processor module for the TDS Virtual TA.
Completely rewritten for better question handling.
"""

import logging
import re
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class QuestionProcessor:
    """Processes and normalizes student questions for better matching."""
    
    def __init__(self):
        """Initialize the question processor."""
        logger.info("Question processor initialized")
    
    def clean_question(self, question: str) -> str:
        """Clean and normalize the question text."""
        if not question:
            return ""
        
        # Remove extra whitespace
        question = re.sub(r'\s+', ' ', question.strip())
        
        # Fix common typos and variations
        replacements = {
            'gpt3.5': 'gpt-3.5',
            'gpt 3.5': 'gpt-3.5',
            'gpt-3.5 turbo': 'gpt-3.5-turbo',
            'gpt3.5 turbo': 'gpt-3.5-turbo',
            'gpt 4o mini': 'gpt-4o-mini',
            'gpt4o mini': 'gpt-4o-mini',
            'gpt-4o mini': 'gpt-4o-mini',
            'ai proxy': 'ai-proxy',
            'openai api': 'openai api',
            'open ai': 'openai'
        }
        
        question_lower = question.lower()
        for old, new in replacements.items():
            question_lower = question_lower.replace(old, new)
        
        return question_lower
    
    def extract_key_terms(self, question: str) -> Dict[str, bool]:
        """Extract key terms and concepts from the question."""
        question_clean = self.clean_question(question)
        
        key_terms = {
            'gpt_model': any(term in question_clean for term in ['gpt-3.5-turbo-0125', 'gpt-4o-mini', 'gpt', 'model']),
            'api': 'api' in question_clean,
            'openai': 'openai' in question_clean,
            'docker': 'docker' in question_clean,
            'podman': 'podman' in question_clean,
            'ga4': 'ga4' in question_clean,
            'dashboard': 'dashboard' in question_clean,
            'bonus': 'bonus' in question_clean,
            'exam': 'exam' in question_clean,
            'tds': 'tds' in question_clean,
            'course': 'course' in question_clean
        }
        
        return key_terms
    
    def determine_question_type(self, question: str) -> str:
        """Determine the type/category of the question."""
        question_clean = self.clean_question(question)
        key_terms = self.extract_key_terms(question)
        
        # GPT/Model related questions
        if key_terms['gpt_model'] or key_terms['api']:
            return "gpt_model"
        
        # Docker/Podman questions
        if key_terms['docker'] or key_terms['podman']:
            return "containerization"
        
        # GA4/Dashboard questions
        if key_terms['ga4'] or key_terms['dashboard']:
            return "ga4_dashboard"
        
        # Exam/Course questions
        if key_terms['exam']:
            return "exam_info"
        
        # General course questions
        if key_terms['course'] or key_terms['tds']:
            return "course_general"
        
        return "general"
    
    def enhance_question(self, question: str) -> str:
        """Enhance the question with additional context for better matching."""
        question_clean = self.clean_question(question)
        question_type = self.determine_question_type(question)
        
        # Add context based on question type
        enhancements = {
            "gpt_model": " model api openai gpt-3.5-turbo-0125 gpt-4o-mini",
            "containerization": " docker podman container",
            "ga4_dashboard": " ga4 dashboard scoring bonus marks",
            "exam_info": " exam schedule date time",
            "course_general": " tds course tools data science"
        }
        
        enhancement = enhancements.get(question_type, "")
        enhanced_question = question_clean + enhancement
        
        logger.info(f"Question type: {question_type}")
        logger.info(f"Enhanced question: {enhanced_question[:100]}...")
        
        return enhanced_question
    
    def process_question(self, question: str, image: Optional[str] = None) -> Dict:
        """
        Process a student question and prepare it for the responder.
        
        Args:
            question (str): The student's question
            image (str, optional): Base64 encoded image data
            
        Returns:
            Dict: Processed question data
        """
        if not question or not question.strip():
            logger.warning("Empty question received")
            return {
                "original_question": "",
                "processed_question": "",
                "question_type": "invalid",
                "key_terms": {},
                "has_image": False
            }
        
        # Clean and enhance the question
        original_question = question.strip()
        processed_question = self.enhance_question(original_question)
        question_type = self.determine_question_type(original_question)
        key_terms = self.extract_key_terms(original_question)
        
        # Handle image if provided
        has_image = bool(image and image.strip())
        if has_image:
            logger.info("Image attachment detected")
        
        result = {
            "original_question": original_question,
            "processed_question": processed_question,
            "question_type": question_type,
            "key_terms": key_terms,
            "has_image": has_image
        }
        
        logger.info(f"Processed question: '{original_question[:50]}...' -> Type: {question_type}")
        
        return result 