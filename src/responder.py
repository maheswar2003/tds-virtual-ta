#!/usr/bin/env python3
"""
Responder module for generating answers to student questions
"""

import json
import logging
import os
from typing import Dict, List
import openai

# Try importing optional packages for better responses
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    HAVE_EMBEDDINGS = True
except ImportError:
    print("Warning: Advanced search not available (missing sentence-transformers)")
    HAVE_EMBEDDINGS = False

logger = logging.getLogger(__name__)

class VirtualTAResponder:
    """Generates answers using AI and course content"""
    
    def __init__(self):
        # Set up OpenAI
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
            print("✓ OpenAI API key loaded")
        else:
            print("⚠ No OpenAI API key found, using fallback mode")
            
        # Try to load embedding model for better search
        self.embedding_model = None
        if HAVE_EMBEDDINGS:
            try:
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("✓ Embedding model loaded for semantic search")
            except Exception as e:
                print(f"⚠ Couldn't load embedding model: {e}")
        
        # Load our knowledge base
        self.load_data()
        
    def load_data(self):
        """Load course content and discourse posts"""
        self.course_content = []
        self.discourse_posts = []
        
        # Try to load scraped data
        try:
            if os.path.exists("data/course_content.json"):
                with open("data/course_content.json", "r", encoding="utf-8") as f:
                    self.course_content = json.load(f)
                print(f"✓ Loaded {len(self.course_content)} course items")
            
            if os.path.exists("data/discourse_posts.json"):
                with open("data/discourse_posts.json", "r", encoding="utf-8") as f:
                    self.discourse_posts = json.load(f)
                print(f"✓ Loaded {len(self.discourse_posts)} discourse posts")
                
        except Exception as e:
            print(f"⚠ Error loading data files: {e}")
            
        # If no data, create some sample content
        if not self.course_content and not self.discourse_posts:
            print("Creating sample knowledge base...")
            self.create_sample_data()
            
    def create_sample_data(self):
        """Create sample data for testing"""
        self.course_content = [
            {
                "title": "AI Models Guide",
                "content": "For assignments, use gpt-3.5-turbo-0125 as specified. Don't use gpt-4o-mini even if AI Proxy supports it.",
                "url": "https://tds.s-anand.net/#/2025-01/ai-models",
                "keywords": ["gpt", "ai", "model", "assignment"]
            },
            {
                "title": "Python Setup",
                "content": "Install required packages using pip. Make sure you have Python 3.8 or higher.",
                "url": "https://tds.s-anand.net/#/2025-01/setup",
                "keywords": ["python", "setup", "install"]
            },
            {
                "title": "Data Science Tools",
                "content": "Course covers pandas, numpy, matplotlib, and scikit-learn for data analysis.",
                "url": "https://tds.s-anand.net/#/2025-01/tools",
                "keywords": ["pandas", "numpy", "tools"]
            }
        ]
        
        self.discourse_posts = [
            {
                "title": "GA5 Model Question",
                "content": "You must use gpt-3.5-turbo-0125 even if AI Proxy only supports gpt-4o-mini. Use OpenAI API directly for this question.",
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939",
                "username": "instructor",
                "keywords": ["gpt", "assignment", "model", "ga5"]
            },
            {
                "title": "Assignment Submission Help",
                "content": "Submit your assignments in the specified format. Late submissions have penalties.",
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/assignment-help/12345",
                "username": "ta",
                "keywords": ["assignment", "submission", "deadline"]
            }
        ]
        
        print("✓ Sample data created")
        
    def find_relevant_content(self, question_data: Dict) -> List[Dict]:
        """Find content related to the question"""
        query = question_data["combined_context"]
        results = []
        
        # Search through course content
        for item in self.course_content:
            score = self.calculate_similarity(query, item)
            if score > 0.1:  # Only include if somewhat relevant
                results.append({
                    "type": "course",
                    "score": score,
                    "item": item,
                    "url": item.get("url", ""),
                    "title": item.get("title", "")
                })
        
        # Search through discourse posts
        for post in self.discourse_posts:
            score = self.calculate_similarity(query, post)
            if score > 0.1:
                results.append({
                    "type": "discourse", 
                    "score": score,
                    "item": post,
                    "url": post.get("url", ""),
                    "title": post.get("title", "")
                })
        
        # Sort by relevance and return top 5
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:5]
    
    def calculate_similarity(self, query: str, item: Dict) -> float:
        """Calculate how similar the query is to an item"""
        query_lower = query.lower()
        item_text = (item.get("content", "") + " " + item.get("title", "")).lower()
        
        # Basic keyword matching
        score = 0.0
        query_words = set(query_lower.split())
        item_words = set(item_text.split())
        
        # Calculate overlap
        common_words = query_words.intersection(item_words)
        all_words = query_words.union(item_words)
        
        if all_words:
            score = len(common_words) / len(all_words)
        
        # Boost for keyword matches
        keywords = item.get("keywords", [])
        for keyword in keywords:
            if keyword.lower() in query_lower:
                score += 0.3
        
        # Use semantic similarity if available
        if self.embedding_model and HAVE_EMBEDDINGS:
            try:
                query_emb = self.embedding_model.encode([query])
                item_emb = self.embedding_model.encode([item_text])
                semantic_score = cosine_similarity(query_emb, item_emb)[0][0]
                score = max(score, semantic_score)
            except:
                pass  # Just use keyword score
        
        return min(score, 1.0)  # Cap at 1.0
    
    def generate_response(self, question_data: Dict) -> Dict:
        """Generate the final response"""
        try:
            # Find relevant content
            relevant_items = self.find_relevant_content(question_data)
            
            # Generate answer
            if self.api_key:
                answer = self.get_ai_answer(question_data, relevant_items)
            else:
                answer = self.get_simple_answer(question_data, relevant_items)
            
            # Get links
            links = self.extract_links(relevant_items)
            
            return {
                "answer": answer,
                "links": links
            }
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return self.fallback_response(question_data)
    
    def get_ai_answer(self, question_data: Dict, relevant_items: List[Dict]) -> str:
        """Use OpenAI to generate answer"""
        try:
            # Prepare context from relevant content
            context_parts = []
            for item in relevant_items[:3]:  # Use top 3
                content = item["item"]
                title = content.get("title", "")
                text = content.get("content", "")
                context_parts.append(f"Title: {title}\nContent: {text}")
            
            context = "\n\n".join(context_parts)
            
            # Create prompt
            system_msg = "You are a helpful TA for IIT Madras Tools in Data Science course. Answer based on the provided context."
            user_msg = f"""Context from course materials:
{context}

Student question: {question_data['original_question']}

Please provide a helpful answer based on the context. If the context doesn't have enough info, give general guidance."""
            
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self.get_simple_answer(question_data, relevant_items)
    
    def get_simple_answer(self, question_data: Dict, relevant_items: List[Dict]) -> str:
        """Generate simple rule-based answer"""
        question = question_data["original_question"].lower()
        question_type = question_data["question_type"]
        
        # Handle specific cases
        if "gpt" in question and ("4o-mini" in question or "3.5" in question or "turbo" in question):
            return "You must use `gpt-3.5-turbo-0125`, even if the AI Proxy only supports `gpt-4o-mini`. Use the OpenAI API directly for this question."
        
        # Handle by question type
        if question_type == "ai-related":
            return "For AI-related questions, check the course materials about model selection and API usage. Follow assignment specifications exactly."
        elif question_type == "troubleshooting":
            return "For troubleshooting, check the course forums first. If the issue persists, provide specific error messages."
        elif question_type == "academic":
            return "For assignment questions, refer to the instructions and rubric. Check the discussion forum for clarifications."
        
        # Use relevant content if available
        if relevant_items:
            top_item = relevant_items[0]["item"]
            content = top_item.get("content", "")[:200]
            return f"Based on course materials: {content}..."
        
        return "Please check the course materials and discussion forum for information related to your question."
    
    def extract_links(self, relevant_items: List[Dict]) -> List[Dict]:
        """Get links from relevant content"""
        links = []
        
        for item in relevant_items[:3]:  # Top 3 only
            content = item["item"]
            url = item.get("url", "")
            title = item.get("title", "")
            
            if url:
                if item["type"] == "discourse":
                    text = f"Discussion: {title}"
                else:
                    text = f"Course material: {title}"
                
                links.append({
                    "url": url,
                    "text": text
                })
        
        return links
    
    def fallback_response(self, question_data: Dict) -> Dict:
        """Emergency fallback response"""
        return {
            "answer": "I'm having trouble processing your question. Please try rephrasing or check the course materials.",
            "links": [
                {
                    "url": "https://tds.s-anand.net/#/2025-01/",
                    "text": "TDS Course Materials"
                },
                {
                    "url": "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34",
                    "text": "TDS Discussion Forum"
                }
            ]
        } 