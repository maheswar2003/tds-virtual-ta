#!/usr/bin/env python3
"""
Responder module for generating answers to student questions.
Simple, reliable version focused on accurate keyword matching.
"""

import json
import logging
import os
from typing import Dict, List
import re

logger = logging.getLogger(__name__)

class VirtualTAResponder:
    """Simple, reliable responder using basic keyword matching."""
    
    def __init__(self):
        """Initialize responder and load data."""
        self.course_content = []
        self.discourse_posts = []
        self.load_data()
        
    def load_data(self):
        """Load course content and discourse posts."""
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        course_content_path = os.path.join(project_root, 'data', 'tds_course_content.json')
        discourse_posts_path = os.path.join(project_root, 'data', 'discourse_posts.json')
        
        try:
            if os.path.exists(course_content_path):
                with open(course_content_path, "r", encoding="utf-8") as f:
                    self.course_content = json.load(f)
                logger.info(f"✅ Loaded {len(self.course_content)} course items.")
            
            if os.path.exists(discourse_posts_path):
                with open(discourse_posts_path, "r", encoding="utf-8") as f:
                    self.discourse_posts = json.load(f)
                logger.info(f"✅ Loaded {len(self.discourse_posts)} discourse posts.")
                
        except Exception as e:
            logger.error(f"⚠️ Could not load data files: {e}")

    def clean_text(self, text: str) -> str:
        """Basic text cleaning - minimal processing."""
        if not text:
            return ""
        # Just normalize whitespace and make lowercase
        text = re.sub(r'\s+', ' ', text.strip()).lower()
        return text

    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        words = re.findall(r'\b\w+\b', text.lower())
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        return [word for word in words if len(word) > 2 and word not in stop_words]

    def calculate_relevance_score(self, question: str, item: Dict) -> float:
        """Calculate relevance score based on keyword overlap."""
        question_keywords = set(self.extract_keywords(question))
        
        title = self.clean_text(item.get("title", ""))
        content = self.clean_text(item.get("content", ""))
        full_text = title + " " + content
        
        content_keywords = set(self.extract_keywords(full_text))
        common_keywords = question_keywords.intersection(content_keywords)
        
        if not common_keywords:
            return 0.0
        
        # Base score
        score = len(common_keywords)
        
        # Boost for specific terms
        question_lower = question.lower()
        if 'gpt-3.5-turbo' in question_lower and 'gpt-3.5-turbo' in full_text:
            score += 10
        if 'gpt-4o-mini' in question_lower and 'gpt-4o-mini' in full_text:
            score += 8
        if 'podman' in question_lower and 'podman' in full_text:
            score += 5
        
        return score

    def find_relevant_content(self, question: str) -> List[Dict]:
        """Find relevant content items."""
        all_content = self.course_content + self.discourse_posts
        scored_results = []
        
        for item in all_content:
            score = self.calculate_relevance_score(question, item)
            if score > 0:
                scored_results.append({
                    "score": score,
                    "item": item
                })
        
        return sorted(scored_results, key=lambda x: x["score"], reverse=True)

    def extract_answer(self, content: str, question: str) -> str:
        """Extract a clean answer from content."""
        if not content:
            return "No specific answer found."
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', content)
        question_keywords = set(self.extract_keywords(question))
        
        best_sentence = ""
        best_score = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20 or len(sentence) > 300:
                continue
                
            sentence_keywords = set(self.extract_keywords(sentence))
            overlap = len(question_keywords.intersection(sentence_keywords))
            
            if overlap > best_score:
                best_score = overlap
                best_sentence = sentence
        
        return best_sentence if best_sentence else content[:200] + "..."

    def generate_response(self, question_data: Dict) -> Dict:
        """Generate response to user question."""
        original_question = question_data.get('original_question', '')
        if not original_question:
            return {"answer": "Please provide a question.", "links": []}

        relevant_items = self.find_relevant_content(original_question)
        
        if not relevant_items:
            return {
                "answer": "I couldn't find relevant information for your question. Please try rephrasing it.",
                "links": []
            }

        # Get the best match
        best_item = relevant_items[0]["item"]
        raw_content = best_item.get('content', '') or best_item.get('title', '')
        answer = self.extract_answer(raw_content, original_question)
        
        # Prepare links
        links = []
        seen_urls = set()
        for result in relevant_items[:3]:
            item = result['item']
            url = item.get('url')
            title = item.get('title', 'Relevant Resource')
            if url and url not in seen_urls:
                links.append({
                    "text": title,
                    "url": url
                })
                seen_urls.add(url)
        
        return {
            "answer": answer,
            "links": links
        }