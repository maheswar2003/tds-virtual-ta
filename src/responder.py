#!/usr/bin/env python3
"""
Responder module for generating answers to student questions
-- Simplified and improved for reliability --
"""

import json
import logging
import os
from typing import Dict, List
import re

logger = logging.getLogger(__name__)

class VirtualTAResponder:
    """Generates answers using course content."""
    
    def __init__(self):
        self.load_data()
        
    def load_data(self):
        """Load course content and discourse posts."""
        self.course_content = []
        self.discourse_posts = []

        # --- FIX: Use absolute paths to find data files ---
        # This makes the file loading robust, regardless of where the app is run from.
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        course_content_path = os.path.join(project_root, 'data', 'course_content.json')
        discourse_posts_path = os.path.join(project_root, 'data', 'discourse_posts.json')
        
        try:
            if os.path.exists(course_content_path):
                with open(course_content_path, "r", encoding="utf-8") as f:
                    self.course_content = json.load(f)
                logger.info(f"✅ Responder loaded {len(self.course_content)} course items from {course_content_path}")
            else:
                logger.warning(f"⚠️ Responder could not find course content at {course_content_path}")
            
            if os.path.exists(discourse_posts_path):
                with open(discourse_posts_path, "r", encoding="utf-8") as f:
                    self.discourse_posts = json.load(f)
                logger.info(f"✅ Responder loaded {len(self.discourse_posts)} discourse posts from {discourse_posts_path}")
            else:
                logger.warning(f"⚠️ Responder could not find discourse posts at {discourse_posts_path}")
                
        except Exception as e:
            logger.error(f"⚠️ Responder Error: Could not load data files: {e}")
            
        if not self.course_content and not self.discourse_posts:
            logger.warning("⚠️ No data loaded. Responder will use fallback answers.")

    def find_relevant_content(self, question: str) -> List[Dict]:
        """Finds the most relevant content using a simple but effective keyword search."""
        
        # Normalize the question to get keywords
        question_lower = question.lower()
        # Use regex to find words, including model numbers like 'gpt-3.5-turbo-0125'
        query_words = set(re.findall(r'[\w.-]+', question_lower))
        
        if not query_words:
            return []

        all_content = self.course_content + self.discourse_posts
        results = []

        for item in all_content:
            score = 0
            # Combine title and content for searching
            content_text = (item.get("title", "") + " " + item.get("content", "")).lower()
            
            # Score based on word overlap
            content_words = set(re.findall(r'[\w.-]+', content_text))
            common_words = query_words.intersection(content_words)
            
            if common_words:
                score = len(common_words)

                # Big boost for important keywords
                if 'ga5' in common_words or 'gpt-3.5-turbo-0125' in common_words:
                    score += 10 
            
            if score > 0:
                results.append({"score": score, "item": item})
        
        # Sort by score to get the most relevant items first
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results

    def generate_response(self, question_data: Dict) -> Dict:
        """Generates the final response based on the best-matching scraped content."""
        
        original_question = question_data['original_question']
        relevant_items = self.find_relevant_content(original_question)
        
        # --- FIX: Use direct content for answer and format links correctly ---
        if relevant_items and relevant_items[0]["score"] > 5: # High confidence threshold
            best_item = relevant_items[0]["item"]
            
            # The answer should be the direct content from the best matching item
            answer = best_item.get('content', 'Could not extract answer text.')
            
            # The first link must be from the best item
            links = []
            if best_item.get('url'):
                links.append({
                    "text": best_item.get('title', 'Source'), 
                    "url": best_item.get('url')
                })

            # Add other unique, relevant links
            seen_urls = {best_item.get('url')}
            for res in relevant_items[1:]:
                if len(links) >= 3:
                    break
                item = res['item']
                url = item.get('url')
                if url and url not in seen_urls:
                    links.append({
                        "text": item.get('title', 'Relevant Link'),
                        "url": url
                    })
                    seen_urls.add(url)

        else:
            # Fallback for generic or unclear questions
            answer = "I couldn't find a specific answer in the course materials. For assignment questions, please double-check the instructions and the course portal. For general queries, try rephrasing your question with more specific keywords."
            
            # Provide some default links if available, even for fallback
            links = []
            seen_urls = set()
            for res in relevant_items:
                if len(links) >= 2: # Limit to 2 for fallback
                    break
                item = res['item']
                url = item.get('url')
                if url and url not in seen_urls:
                    links.append({
                        "text": item.get('title', 'Relevant Link'),
                        "url": url
                    })
                    seen_urls.add(url)
        
        return {
            "answer": answer,
            "links": links
        }