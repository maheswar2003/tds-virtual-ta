#!/usr/bin/env python3
"""
Final optimized responder focused on TDS course questions.
Minimal off-topic handling, maximum focus on real student questions.
"""

import re
import logging
from typing import Dict, List, Set
from src.refined_responder import RefinedVirtualTAResponder

logger = logging.getLogger(__name__)

class ImprovedVirtualTAResponder(RefinedVirtualTAResponder):
    """Final optimized responder focused on real TDS course questions."""
    
    def __init__(self):
        """Initialize with minimal off-topic handling, focus on TDS questions."""
        super().__init__()
        
        # Only check for obviously off-topic patterns (minimal list)
        self.off_topic_patterns = [
            r'(?:cook|recipe|food|meal)',
            r'(?:weather|temperature|rain|snow)',
            r'(?:joke|funny|humor)',
            r'(?:math.*\d+.*[\+\-\*\/].*\d+)',  # Basic math like "2+2"
        ]
    
    def is_question_relevant(self, question: str, concepts: Set[str]) -> bool:
        """Minimal relevance check - assume most questions are TDS-related."""
        
        question_lower = question.lower()
        
        # Only filter out obviously ridiculous questions
        for pattern in self.off_topic_patterns:
            if re.search(pattern, question_lower):
                return False
        
        # Assume everything else is potentially TDS-related
        return True
    
    def calculate_answer_relevance(self, answer: str, question: str) -> float:
        """Enhanced relevance calculation for TDS content."""
        
        if not answer or len(answer) < 10:
            return 0.0
        
        answer_lower = answer.lower()
        question_lower = question.lower()
        
        relevance_score = 0.0
        
        # TDS-specific keywords boost
        tds_keywords = [
            'tds', 'course', 'tools', 'data', 'science', 'programming', 'python',
            'gpt', 'openai', 'api', 'model', 'project', 'assignment', 'exam',
            'podman', 'docker', 'container', 'development', 'git', 'github'
        ]
        
        for keyword in tds_keywords:
            if keyword in answer_lower:
                relevance_score += 3
        
        # Question term matching
        question_words = set(re.findall(r'\b\w{3,}\b', question_lower))
        answer_words = set(re.findall(r'\b\w{3,}\b', answer_lower))
        overlap = question_words.intersection(answer_words)
        relevance_score += len(overlap) * 2
        
        # Boost for actionable content
        actionable_indicators = [
            'you should', 'you must', 'you can', 'use', 'install', 'run',
            'create', 'check', 'see', 'refer', 'follow'
        ]
        
        for indicator in actionable_indicators:
            if indicator in answer_lower:
                relevance_score += 2
        
        # Penalize generic boilerplate
        if 'tools in data science tools in data science' in answer_lower:
            relevance_score -= 10
        
        return relevance_score
    
    def generate_off_topic_response(self, question: str) -> Dict:
        """Simple off-topic response for obviously irrelevant questions."""
        
        return {
            "answer": f"I'm designed to help with TDS (Tools in Data Science) course questions. Please ask me about course content, assignments, tools, or technical topics covered in TDS.",
            "links": []
        }
    
    def generate_response(self, question_data: Dict) -> Dict:
        """Optimized response generation focused on TDS questions."""
        
        original_question = question_data.get("original_question", "")
        concepts = question_data.get("concepts", set())
        
        if not original_question:
            return {
                "answer": "Please provide a valid question about TDS course content.",
                "links": []
            }
        
        # Minimal off-topic filtering
        if not self.is_question_relevant(original_question, concepts):
            return self.generate_off_topic_response(original_question)
        
        # Generate response using parent class
        response = super().generate_response(question_data)
        
        # Check answer quality and improve if needed
        answer = response.get("answer", "")
        relevance_score = self.calculate_answer_relevance(answer, original_question)
        
        # Only improve if answer is really poor quality
        if relevance_score < 3:
            logger.info(f"Improving low-quality answer for: {original_question[:50]}...")
            category = question_data.get("category", "general")
            improved_answer = self.generate_improved_fallback(category, original_question)
            response["answer"] = improved_answer
        
        return response
    
    def generate_improved_fallback(self, category: str, question: str) -> str:
        """Generate improved fallback answers for TDS questions."""
        
        fallbacks = {
            "gpt_api": "For TDS projects, you typically use gpt-3.5-turbo-0125 or gpt-4o-mini. Check your specific project instructions for the exact model requirement.",
            
            "containers": "TDS course uses Podman (preferred) or Docker for containerization. Refer to the course materials for setup instructions on your operating system.",
            
            "exam_schedule": "Check the TDS course page at tds.s-anand.net for current exam schedules, dates, and format information.",
            
            "ga4_bonus": "Bonus marks are awarded for additional features in projects. Check the specific project requirements for bonus criteria.",
            
            "course_info": "TDS covers data science tools including development tools, LLMs, data sourcing, analysis, and visualization. See the course syllabus for complete details.",
            
            "tools_usage": "TDS covers development tools like VS Code, Python (uv), JavaScript (npx), Git, containers, and more. Check the relevant course section.",
            
            "general": f"For TDS course help with '{question}', please check the course materials at tds.s-anand.net or ask on the course Discourse forum for specific guidance."
        }
        
        return fallbacks.get(category, fallbacks["general"]) 