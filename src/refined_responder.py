#!/usr/bin/env python3
"""
Refined responder with improved answer extraction and sentence quality.
Built upon the new system but with better natural language generation.
"""

import json
import os
import re
import logging
from typing import Dict, List, Set, Tuple, Optional
from src.new_responder import SmartVirtualTAResponder

logger = logging.getLogger(__name__)

class RefinedVirtualTAResponder(SmartVirtualTAResponder):
    """Refined responder with better answer quality and coherence."""
    
    def __init__(self):
        """Initialize with enhanced answer generation patterns."""
        super().__init__()
        
        # Enhanced answer patterns for better sentence detection
        self.enhanced_answer_patterns = [
            r'(?:you\s+(?:must|should|need\s+to|can)|it\s+is\s+(?:recommended|important|required))',
            r'(?:use|install|run|execute)\s+[\w\-]+',
            r'the\s+(?:recommended|preferred|best|correct)\s+\w+\s+is\s+[\w\-]+',
            r'in\s+this\s+course[,\s]+(?:you|we|students)',
            r'for\s+(?:tds|this\s+course)[,\s]+(?:you|we|students)',
            r'(?:students?|you)\s+(?:should|must|need)\s+to\s+\w+',
            r'to\s+\w+[,\s]+(?:you|students)\s+(?:should|must|need)',
            r'(?:first|next|then|finally)[,\s]+\w+'
        ]
        
        # Question-specific answer patterns
        self.specific_patterns = {
            "gpt_api": [
                r'gpt-(?:3\.5-turbo-0125|4o-mini)',
                r'(?:use|recommended|prefer)\s+gpt-[\w\-]+',
                r'openai\s+api\s+(?:directly|model)',
                r'model\s+(?:that|mentioned|specified)'
            ],
            "containers": [
                r'podman\s+(?:machine|login|build|run)',
                r'docker\s+(?:login|build|run)',
                r'(?:initialize|install|setup)\s+(?:podman|docker)',
                r'container\s+(?:engine|build|run)'
            ],
            "exam_schedule": [
                r'exam\s+(?:on|date|schedule)',
                r'(?:roe|final)\s+exam',
                r'(?:march|april|feb)\s+\d{4}',
                r'\d{2}\s+(?:mar|apr|feb)\s+\d{4}'
            ],
            "ga4_bonus": [
                r'bonus\s+(?:marks?|points?)',
                r'(?:score|earn|get)\s+bonus',
                r'(?:1|2)\s+marks?\s+if',
                r'github\s+repo\s+includes'
            ]
        }

    def extract_coherent_sentences(self, content: str, question_data: Dict) -> List[Tuple[float, str]]:
        """Extract coherent, well-formed sentences with better scoring."""
        
        if not content:
            return []
        
        # Split into sentences more carefully
        # Split on sentence endings but keep context
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', content)
        
        category = question_data.get("category", "general")
        concepts = question_data.get("concepts", set())
        
        scored_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            
            # Skip very short or very long sentences
            if len(sentence) < 20 or len(sentence) > 300:
                continue
            
            # Skip sentences with junk patterns
            sentence_lower = sentence.lower()
            if any(re.search(pattern, sentence_lower) for pattern in self.junk_patterns):
                continue
            
            # Skip sentences that are mostly punctuation or numbers
            word_count = len(re.findall(r'\b\w+\b', sentence))
            if word_count < 5:
                continue
            
            # Calculate sentence score
            score = self.calculate_sentence_score(sentence, question_data)
            
            if score > 0:
                scored_sentences.append((score, sentence))
        
        return scored_sentences
    
    def calculate_sentence_score(self, sentence: str, question_data: Dict) -> float:
        """Calculate sentence quality score with enhanced criteria."""
        
        sentence_lower = sentence.lower()
        category = question_data.get("category", "general")
        concepts = question_data.get("concepts", set())
        
        score = 0.0
        
        # Base score for sentence structure
        if re.match(r'^[A-Z]', sentence) and sentence.endswith(('.', '!', '?')):
            score += 2  # Proper sentence structure
        
        # Concept matching
        for concept in concepts:
            if concept.lower() in sentence_lower:
                score += 5
        
        # Enhanced answer patterns
        for pattern in self.enhanced_answer_patterns:
            if re.search(pattern, sentence_lower):
                score += 3
        
        # Category-specific patterns
        if category in self.specific_patterns:
            for pattern in self.specific_patterns[category]:
                if re.search(pattern, sentence_lower):
                    score += 4
        
        # Penalize incomplete sentences (starting with lowercase, conjunctions)
        if re.match(r'^(?:and|or|but|so|then|also|however|therefore)', sentence_lower):
            score -= 2
        
        # Boost for direct answers
        if any(phrase in sentence_lower for phrase in ['you should', 'you must', 'you can', 'it is', 'use the']):
            score += 2
        
        # Penalize overly technical or fragmented content
        tech_indicators = len(re.findall(r'(?:http|git|json|api|url|id|src|div)', sentence_lower))
        if tech_indicators > 2:
            score -= tech_indicators
        
        return score
    
    def combine_sentences_intelligently(self, scored_sentences: List[Tuple[float, str]], max_sentences: int = 2) -> str:
        """Combine top sentences into a coherent answer."""
        
        if not scored_sentences:
            return "No relevant information found."
        
        # Sort by score
        scored_sentences.sort(key=lambda x: x[0], reverse=True)
        
        # Take top sentences
        selected_sentences = []
        total_length = 0
        
        for score, sentence in scored_sentences[:max_sentences * 2]:  # Consider more options
            if len(selected_sentences) >= max_sentences:
                break
            
            # Avoid overly long answers
            if total_length + len(sentence) > 400:
                break
            
            # Avoid duplicate information
            if not any(self.sentences_too_similar(sentence, existing) for existing in selected_sentences):
                selected_sentences.append(sentence)
                total_length += len(sentence)
        
        if not selected_sentences:
            # Fallback to highest scoring sentence
            return scored_sentences[0][1]
        
        # Combine sentences with proper spacing
        combined = ' '.join(selected_sentences)
        
        # Clean up the combined answer
        combined = re.sub(r'\s+', ' ', combined).strip()
        
        # Ensure proper ending
        if not combined.endswith(('.', '!', '?')):
            combined += '.'
        
        return combined
    
    def sentences_too_similar(self, sentence1: str, sentence2: str) -> bool:
        """Check if two sentences are too similar (avoid duplication)."""
        
        words1 = set(re.findall(r'\b\w+\b', sentence1.lower()))
        words2 = set(re.findall(r'\b\w+\b', sentence2.lower()))
        
        if len(words1) == 0 or len(words2) == 0:
            return False
        
        overlap = len(words1.intersection(words2))
        similarity = overlap / max(len(words1), len(words2))
        
        return similarity > 0.6  # 60% similarity threshold
    
    def generate_category_specific_answer(self, question_data: Dict, best_content: str) -> str:
        """Generate category-specific answers with better context."""
        
        category = question_data.get("category", "general")
        original_question = question_data.get("original_question", "")
        
        # Extract sentences
        scored_sentences = self.extract_coherent_sentences(best_content, question_data)
        
        if not scored_sentences:
            return self.generate_fallback_answer(category, original_question)
        
        # Generate answer based on category
        if category == "gpt_api":
            return self.generate_gpt_answer(scored_sentences, question_data)
        elif category == "containers":
            return self.generate_container_answer(scored_sentences, question_data)
        elif category == "exam_schedule":
            return self.generate_exam_answer(scored_sentences, question_data)
        elif category == "ga4_bonus":
            return self.generate_bonus_answer(scored_sentences, question_data)
        elif category == "course_info":
            return self.generate_course_answer(scored_sentences, question_data)
        else:
            return self.combine_sentences_intelligently(scored_sentences)
    
    def generate_gpt_answer(self, scored_sentences: List[Tuple[float, str]], question_data: Dict) -> str:
        """Generate GPT/API specific answer."""
        
        concepts = question_data.get("concepts", set())
        
        # Look for specific model recommendations
        for score, sentence in scored_sentences:
            if any(model in sentence.lower() for model in ['gpt-3.5-turbo-0125', 'gpt-4o-mini']):
                if 'use' in sentence.lower() or 'recommended' in sentence.lower():
                    return sentence
        
        # Fallback to best sentence
        return self.combine_sentences_intelligently(scored_sentences, 1)
    
    def generate_container_answer(self, scored_sentences: List[Tuple[float, str]], question_data: Dict) -> str:
        """Generate container-specific answer."""
        
        # Look for installation/setup instructions
        for score, sentence in scored_sentences:
            if any(cmd in sentence.lower() for cmd in ['podman machine', 'podman login', 'install', 'initialize']):
                return sentence
        
        return self.combine_sentences_intelligently(scored_sentences, 1)
    
    def generate_exam_answer(self, scored_sentences: List[Tuple[float, str]], question_data: Dict) -> str:
        """Generate exam-specific answer."""
        
        # Look for specific dates or scheduling info
        for score, sentence in scored_sentences:
            if re.search(r'\d{2}\s+(?:mar|apr|feb|jan|may)\s+\d{4}', sentence.lower()):
                return sentence
        
        return self.combine_sentences_intelligently(scored_sentences, 1)
    
    def generate_bonus_answer(self, scored_sentences: List[Tuple[float, str]], question_data: Dict) -> str:
        """Generate bonus-specific answer."""
        
        # Look for specific bonus criteria
        for score, sentence in scored_sentences:
            if 'mark' in sentence.lower() and ('bonus' in sentence.lower() or 'score' in sentence.lower()):
                return sentence
        
        return self.combine_sentences_intelligently(scored_sentences, 1)
    
    def generate_course_answer(self, scored_sentences: List[Tuple[float, str]], question_data: Dict) -> str:
        """Generate course info answer."""
        
        return self.combine_sentences_intelligently(scored_sentences, 2)
    
    def generate_fallback_answer(self, category: str, question: str) -> str:
        """Generate fallback answers when no good content found."""
        
        fallbacks = {
            "gpt_api": "For TDS course, check the specific model requirements mentioned in the course materials or project instructions.",
            "containers": "Refer to the Docker/Podman section in the course materials for installation and setup instructions.",
            "exam_schedule": "Check the course schedule and announcements for exam dates and times.",
            "ga4_bonus": "Look for bonus activity announcements on the course Discourse or course materials.",
            "course_info": "Refer to the course overview and syllabus for detailed information about course structure and requirements."
        }
        
        return fallbacks.get(category, f"Please refer to the course materials for information about your question: '{question}'")
    
    def extract_best_answer(self, content: str, question_data: Dict) -> str:
        """Enhanced answer extraction with better coherence."""
        
        if not content:
            return "No relevant information found."
        
        # Use the refined answer generation
        answer = self.generate_category_specific_answer(question_data, content)
        
        # Final cleanup
        answer = re.sub(r'\s+', ' ', answer).strip()
        
        # Ensure proper capitalization
        if answer and not answer[0].isupper():
            answer = answer[0].upper() + answer[1:]
        
        return answer 