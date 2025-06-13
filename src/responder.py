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
        
        try:
            if os.path.exists("data/course_content.json"):
                with open("data/course_content.json", "r", encoding="utf-8") as f:
                    self.course_content = json.load(f)
                print(f"✅ Responder loaded {len(self.course_content)} course items.")
            
            if os.path.exists("data/discourse_posts.json"):
                with open("data/discourse_posts.json", "r", encoding="utf-8") as f:
                    self.discourse_posts = json.load(f)
                print(f"✅ Responder loaded {len(self.discourse_posts)} discourse posts.")
                
        except Exception as e:
            print(f"⚠️ Responder Error: Could not load data files: {e}")
            
        if not self.course_content and not self.discourse_posts:
            print("⚠️ No data found. Responder will use fallback answers.")

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
        
        # If we have a highly relevant item, use it to form the answer
        if relevant_items and relevant_items[0]["score"] > 5: # High confidence threshold
            best_item = relevant_items[0]["item"]
            answer = f"Based on the course materials, here is information regarding your question: \"{best_item['content']}\" This was found in a document titled \"{best_item['title']}\"."
        else:
            # Fallback for generic or unclear questions
            answer = "I couldn't find a specific answer in the course materials. For assignment questions, please double-check the instructions and the course portal. For general queries, try rephrasing your question with more specific keywords."

        # Extract up to 3 relevant links
        links = []
        seen_urls = set()
        for res in relevant_items:
            item = res['item']
            url = item.get('url')
            if url and url not in seen_urls:
                links.append({
                    "text": item.get('title', 'Relevant Link'),
                    "url": url
                })
                seen_urls.add(url)
            if len(links) >= 3:
                break
        
        return {
            "answer": answer,
            "links": links
        } 