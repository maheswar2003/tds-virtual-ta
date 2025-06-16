#!/usr/bin/env python3
"""
Responder module for generating answers to student questions.
Final, robust version with pre-computation and advanced answer extraction.
"""

import json
import logging
import os
from typing import Dict, List, Tuple
import re

logger = logging.getLogger(__name__)

class VirtualTAResponder:
    """Generates answers using a pre-computed, sanitized data source."""
    
    def __init__(self):
        """Initializes the responder, loads data, and pre-computes clean text."""
        self.all_content = []
        self._load_and_clean_data()
        
    def _radical_clean(self, text: str) -> str:
        """Aggressively removes junk, code, and meta-text."""
        if not text:
            return ""
        # Remove URLs
        text = re.sub(r'https?://\S+', '', text)
        # Remove anything that looks like code or JSON snippets
        text = re.sub(r'\{.*?\}', '', text, flags=re.DOTALL)
        text = re.sub(r'<.*?>', '', text, flags=re.DOTALL)
        # Remove UI text and instructions
        negative_patterns = [
            'copy to clipboard', 'error copied', 'this is a real question',
            'the response must be a json object', 'screenshot', 'for example',
            'relevant resource', 'related resources', 'rawcontent', 'statuscode',
            'like this:', 'must accept a post request', 'out of kindness'
        ]
        for pattern in negative_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        # Normalize whitespace and remove leftover characters
        text = re.sub(r'\s+', ' ', text).strip()
        text = text.replace('`', '').replace('"', '').replace("'", "")
        return text

    def _load_and_clean_data(self):
        """Loads data and pre-computes a clean, searchable text field for each item."""
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        course_content_path = os.path.join(project_root, 'data', 'tds_course_content.json')
        discourse_posts_path = os.path.join(project_root, 'data', 'discourse_posts.json')
        
        raw_content = []
        try:
            if os.path.exists(course_content_path):
                with open(course_content_path, "r", encoding="utf-8") as f:
                    raw_content.extend(json.load(f))
                logger.info("✅ Loaded course content.")
            if os.path.exists(discourse_posts_path):
                with open(discourse_posts_path, "r", encoding="utf-8") as f:
                    raw_content.extend(json.load(f))
                logger.info("✅ Loaded discourse posts.")
        except Exception as e:
            logger.error(f"⚠️ Could not load data files: {e}")

        if not raw_content:
            logger.error("❌ No data loaded. The responder is offline.")
            return

        for item in raw_content:
            full_raw_text = item.get('title', '') + " " + item.get('content', '')
            # Create a new key with the sanitized text for searching
            item['clean_search_text'] = self._radical_clean(full_raw_text)
        
        self.all_content = raw_content
        logger.info(f"✅ Pre-computation complete. {len(self.all_content)} items ready for search.")

    def _get_keywords(self, text: str) -> set:
        """Utility to get a set of keywords from text."""
        words = re.findall(r'[\w.-]+', text.lower())
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        return {word for word in words if len(word) > 2 and word not in stop_words}

    def find_relevant_content(self, question: str) -> List[Dict]:
        """Finds relevant content using the pre-computed clean text."""
        question_keywords = self._get_keywords(question)
        
        scored_results = []
        for item in self.all_content:
            if not item.get('clean_search_text'):
                continue

            content_keywords = self._get_keywords(item['clean_search_text'])
            common_keywords = question_keywords.intersection(content_keywords)
            
            if not common_keywords:
                continue

            # Scoring based on keyword overlap and boosting critical terms
            score = len(common_keywords) * 5
            
            critical_terms = {
                'gpt-3.5-turbo-0125': 50, 'gpt-4o-mini': 40, 'podman': 30, 
                'docker': 25, 'ga4': 20, 'dashboard': 15, 'api key': 20
            }
            for term, boost in critical_terms.items():
                if term in question.lower() and term in item['clean_search_text'].lower():
                    score += boost
            
            scored_results.append({'score': score, 'item': item})

        return sorted(scored_results, key=lambda x: x['score'], reverse=True)

    def extract_final_answer(self, item: Dict, question: str) -> str:
        """Extracts the best possible sentence as the answer."""
        clean_text = item.get('clean_search_text', '')
        question_keywords = self._get_keywords(question)

        sentences = re.split(r'[.!?]+', clean_text)
        best_sentence = ""
        highest_score = -1

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue
            
            sentence_keywords = self._get_keywords(sentence)
            common_keywords = question_keywords.intersection(sentence_keywords)
            score = len(common_keywords)
            
            # Boost for sentences that look like direct answers
            if any(phrase in sentence.lower() for phrase in ['you must', 'you should', 'the answer is', 'it is recommended']):
                score += 3
            
            if score > highest_score:
                highest_score = score
                best_sentence = sentence

        return best_sentence if highest_score > 0 else "I found some relevant information, but not a direct answer. It's best to check the linked resources."

    def generate_response(self, question_data: Dict) -> Dict:
        """The main response generation function."""
        original_question = question_data.get('original_question', '')
        if not original_question:
            return {"answer": "Please provide a question.", "links": []}

        relevant_items = self.find_relevant_content(original_question)
        
        if not relevant_items or relevant_items[0]['score'] < 10:
            return {
                "answer": "I'm sorry, I couldn't find a specific answer in the course materials. Please try rephrasing your question or checking the Discourse forum directly.",
                "links": []
            }

        best_item = relevant_items[0]['item']
        answer = self.extract_final_answer(best_item, original_question)
        
        links = []
        seen_urls = set()
        for res in relevant_items[:3]:
            item = res['item']
            url = item.get('url')
            title = self._radical_clean(item.get('title', 'Relevant Resource'))
            if url and url not in seen_urls:
                links.append({"text": title.title(), "url": url})
                seen_urls.add(url)
        
        return {"answer": answer, "links": links}