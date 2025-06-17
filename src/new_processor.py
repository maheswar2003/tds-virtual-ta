#!/usr/bin/env python3
"""
Final optimized question processor with enhanced keyword handling for real student questions.
"""

import re
import logging
from typing import Dict, List, Optional, Set

logger = logging.getLogger(__name__)

class SmartQuestionProcessor:
    """Final optimized question processor for TDS student questions."""
    
    def __init__(self):
        """Initialize with enhanced patterns for real student questions."""
        
        # Enhanced GPT/API model patterns
        self.gpt_patterns = [
            r'gpt[-\s]*(3\.5|4o)[-\s]*(?:turbo|mini)?',
            r'(?:which|what)\s+(?:model|llm|ai)',
            r'(?:openai|chatgpt)\s*(?:api|model)?',
            r'(?:api\s+)?model\s+(?:selection|choice|recommendation)',
            r'(?:use|choose|select)\s+(?:gpt|model|llm)',
            r'(?:better|recommend|prefer)\s+(?:gpt|model)',
            r'llm\s+(?:model|choice|selection)'
        ]
        
        # Enhanced container patterns
        self.container_patterns = [
            r'podman',
            r'docker',
            r'container(?:s|ization)?',
            r'(?:windows|mac|linux).*(?:podman|docker)',
            r'(?:podman|docker).*(?:windows|mac|linux)',
            r'(?:install|setup|run).*(?:podman|docker)',
            r'(?:podman|docker).*(?:install|setup|run)'
        ]
        
        # Enhanced GA4/Dashboard patterns  
        self.ga4_patterns = [
            r'ga4',
            r'google\s+analytics',
            r'dashboard',
            r'bonus\s+(?:marks?|points?|score)',
            r'(?:score|earn|get)\s+bonus',
            r'extra\s+(?:marks?|points?|credit)'
        ]
        
        # Enhanced exam patterns
        self.exam_patterns = [
            r'exam\s+(?:date|time|when|schedule)',
            r'(?:when|what\s+time).*exam',
            r'exam\s+(?:schedule|timing|format)',
            r'(?:roe|final|mid-?term)\s+exam',
            r'(?:test|quiz|assessment)\s+(?:date|time|schedule)'
        ]
        
        # Enhanced course structure patterns
        self.course_patterns = [
            r'(?:pre-?)?requisites?',
            r'course\s+(?:structure|outline|syllabus|content)',
            r'(?:modules?|topics?|subjects?)\s+covered',
            r'(?:assignments?|projects?|homework)',
            r'(?:grading|evaluation|marks?|score)',
            r'course\s+(?:difficulty|hard|tough|easy)',
            r'(?:credits?|weightage|percentage)'
        ]
        
        # Enhanced tools patterns
        self.tools_patterns = [
            r'vs\s+code|vscode|visual\s+studio',
            r'unicode|encoding|character',
            r'scrap(?:ing|e|er)',
            r'python\s+(?:tools|libraries|packages)',
            r'(?:data\s+science|development)\s+tools',
            r'terminal|command\s+line|bash|shell',
            r'(?:text\s+)?editor|ide',
            r'git(?:hub)?|version\s+control'
        ]
        
        logger.info("SmartQuestionProcessor initialized with enhanced patterns")
    
    def clean_text(self, text: str) -> str:
        """Enhanced text cleaning for better processing."""
        if not text:
            return ""
        
        # Basic cleanup
        text = re.sub(r'\s+', ' ', text.strip())
        text = text.lower()
        
        # Normalize common variations
        text = re.sub(r'gpt[-\s]*3\.5[-\s]*turbo', 'gpt-3.5-turbo', text)
        text = re.sub(r'gpt[-\s]*4o[-\s]*mini', 'gpt-4o-mini', text)
        text = re.sub(r'vs[-\s]*code', 'vscode', text)
        text = re.sub(r'open[-\s]*ai', 'openai', text)
        
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\-\.\?]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def match_patterns(self, text: str, patterns: List[str]) -> bool:
        """Enhanced pattern matching with better scoring."""
        text_clean = self.clean_text(text)
        matches = sum(1 for pattern in patterns if re.search(pattern, text_clean, re.IGNORECASE))
        return matches > 0
    
    def categorize_question(self, question: str) -> str:
        """Enhanced question categorization with priority ordering."""
        
        # Check patterns in order of specificity
        if self.match_patterns(question, self.gpt_patterns):
            return "gpt_api"
        
        if self.match_patterns(question, self.container_patterns):
            return "containers"
        
        if self.match_patterns(question, self.ga4_patterns):
            return "ga4_bonus"
        
        if self.match_patterns(question, self.exam_patterns):
            return "exam_schedule"
        
        if self.match_patterns(question, self.course_patterns):
            return "course_info"
        
        if self.match_patterns(question, self.tools_patterns):
            return "tools_usage"
        
        return "general"
    
    def extract_key_concepts(self, question: str) -> Set[str]:
        """Enhanced concept extraction with better normalization."""
        text_clean = self.clean_text(question)
        
        concepts = set()
        
        # Model concepts with variations
        if any(term in text_clean for term in ['gpt-3.5', '3.5', 'gpt3.5', 'three point five']):
            concepts.add('gpt-3.5-turbo')
        if any(term in text_clean for term in ['gpt-4o', '4o', 'gpt4o', 'four o']):
            concepts.add('gpt-4o-mini')
        if any(term in text_clean for term in ['model', 'llm', 'ai']):
            concepts.add('model')
        if any(term in text_clean for term in ['api', 'openai']):
            concepts.add('api')
        
        # Container concepts
        if 'podman' in text_clean:
            concepts.add('podman')
        if 'docker' in text_clean:
            concepts.add('docker')
        if any(term in text_clean for term in ['windows', 'win', 'pc']):
            concepts.add('windows')
        if 'container' in text_clean:
            concepts.add('container')
        
        # Tool concepts
        if any(term in text_clean for term in ['vscode', 'vs code', 'visual studio']):
            concepts.add('vscode')
        if 'unicode' in text_clean:
            concepts.add('unicode')
        if any(term in text_clean for term in ['scrap', 'crawl', 'extract']):
            concepts.add('scraping')
        
        # Course concepts
        if any(term in text_clean for term in ['exam', 'test', 'assessment']):
            concepts.add('exam')
        if any(term in text_clean for term in ['bonus', 'extra', 'additional']):
            concepts.add('bonus')
        if 'ga4' in text_clean:
            concepts.add('ga4')
        if any(term in text_clean for term in ['prerequisite', 'requirement', 'prereq']):
            concepts.add('prerequisites')
        if any(term in text_clean for term in ['grade', 'mark', 'score', 'point']):
            concepts.add('grading')
        
        return concepts
    
    def enhance_question_for_search(self, question: str, category: str, concepts: Set[str]) -> str:
        """Enhanced search term generation for better content matching."""
        
        base_question = self.clean_text(question)
        
        # Category-specific enhancements
        enhancements = []
        
        if category == "gpt_api":
            enhancements.extend(['openai', 'api', 'model', 'gpt-3.5-turbo-0125', 'gpt-4o-mini', 'llm'])
        elif category == "containers":
            enhancements.extend(['docker', 'podman', 'container', 'windows', 'install', 'setup'])
        elif category == "ga4_bonus":
            enhancements.extend(['ga4', 'dashboard', 'bonus', 'marks', 'scoring', 'extra', 'points'])
        elif category == "exam_schedule":
            enhancements.extend(['exam', 'date', 'schedule', 'roe', 'final', 'timing', 'format'])
        elif category == "course_info":
            enhancements.extend(['course', 'prerequisite', 'structure', 'module', 'syllabus', 'content'])
        elif category == "tools_usage":
            enhancements.extend(['tools', 'development', 'editor', 'programming', 'setup'])
        
        # Add concepts
        enhancements.extend(list(concepts))
        
        # Add TDS-specific terms
        enhancements.extend(['tds', 'tools', 'data', 'science'])
        
        # Combine and deduplicate
        all_terms = [base_question] + enhancements
        enhanced = ' '.join(set(all_terms))
        
        logger.debug(f"Enhanced search: {enhanced[:100]}...")
        return enhanced
    
    def process_question(self, question: str, image: Optional[str] = None) -> Dict:
        """Enhanced question processing for real student questions."""
        
        if not question or not question.strip():
            return {
                "original_question": "",
                "processed_question": "",
                "category": "invalid",
                "concepts": set(),
                "enhanced_search": "",
                "has_image": False
            }
        
        original_question = question.strip()
        category = self.categorize_question(original_question)
        concepts = self.extract_key_concepts(original_question)
        enhanced_search = self.enhance_question_for_search(original_question, category, concepts)
        
        result = {
            "original_question": original_question,
            "processed_question": self.clean_text(original_question),
            "category": category,
            "concepts": concepts,
            "enhanced_search": enhanced_search,
            "has_image": bool(image and image.strip())
        }
        
        logger.info(f"Processed: '{original_question[:40]}...' -> {category}, {len(concepts)} concepts")
        
        return result 