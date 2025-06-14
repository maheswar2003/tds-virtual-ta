#!/usr/bin/env python3
"""
Responder module for generating answers to student questions.
This version loads data from external JSON files for maximum flexibility.
"""

import json
import logging
import os
from typing import Dict, List
import re

logger = logging.getLogger(__name__)

class VirtualTAResponder:
    """Generates answers using course content and discourse posts."""
    
    def __init__(self):
        """Initializes the responder by loading all data."""
        self.load_data()
        
    def load_data(self):
        """
        Loads course content and discourse posts from the data directory.
        Constructs absolute paths to ensure reliability across environments.
        """
        self.course_content = []
        self.discourse_posts = []

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        course_content_path = os.path.join(project_root, 'data', 'tds_course_content.json')
        discourse_posts_path = os.path.join(project_root, 'data', 'discourse_posts.json')
        
        try:
            if os.path.exists(course_content_path):
                with open(course_content_path, "r", encoding="utf-8") as f:
                    self.course_content = json.load(f)
                logger.info(f"✅ Loaded {len(self.course_content)} course items.")
            else:
                logger.warning(f"⚠️ Could not find course content at {course_content_path}")
            
            if os.path.exists(discourse_posts_path):
                with open(discourse_posts_path, "r", encoding="utf-8") as f:
                    self.discourse_posts = json.load(f)
                logger.info(f"✅ Loaded {len(self.discourse_posts)} discourse posts.")
            else:
                logger.warning(f"⚠️ Could not find discourse posts at {discourse_posts_path}")
                
        except json.JSONDecodeError as e:
            logger.error(f"⚠️ JSON Error: Failed to decode a data file. Check for syntax errors: {e}")
        except Exception as e:
            logger.error(f"⚠️ File Load Error: Could not load data files: {e}")
            
        if not self.course_content and not self.discourse_posts:
            logger.error("❌ No data loaded. The responder will not be able to provide answers.")

    def find_relevant_content(self, question: str) -> List[Dict]:
        """
        Finds the most relevant content by scoring based on keyword overlap.
        Gives a significant score boost for critical keywords.
        """
        question_lower = question.lower()
        query_words = set(re.findall(r'[\\w.-]+', question_lower))
        
        if not query_words:
            return []

        all_content = self.course_content + self.discourse_posts
        results = []

        for item in all_content:
            score = 0
            # Ensure title and content are strings before combining
            title = item.get("title", "") or ""
            content = item.get("content", "") or ""
            content_text = (title + " " + content).lower()
            
            content_words = set(re.findall(r'[\w.-]+', content_text))
            common_words = query_words.intersection(content_words)
            
            if common_words:
                score = len(common_words)
                # Boost score for important keywords for higher relevance
                boost_words = {'ga5', 'gpt-3.5-turbo-0125', 'gpt3.5', 'gpt-4o-mini', 'docker', 'podman'}
                if not boost_words.isdisjoint(common_words):
                    score += 20
            
            if score > 0:
                results.append({"score": score, "item": item})
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def generate_response(self, question_data: Dict) -> Dict:
        """
        Generates the final JSON response object based on the best-matching content.
        """
        original_question = question_data['original_question']
        relevant_items = self.find_relevant_content(original_question)
        
        if relevant_items and relevant_items[0]["score"] > 0:
            best_item = relevant_items[0]["item"]
            answer = best_item.get('content', 'Could not extract a specific answer.')
            
            # Create a list of relevant links, starting with the best match
            links = []
            seen_urls = set()
            for res in relevant_items:
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
            answer = "I couldn't find a specific answer in the course materials. Please try rephrasing your question with more specific keywords."
            links = []
        
        return {
            "answer": answer,
            "links": links
        }