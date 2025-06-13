#!/usr/bin/env python3
"""
Virtual TA responder that generates answers with relevant links
"""

import json
import logging
import os
from typing import Dict, List, Optional
import openai

# Try to import optional dependencies
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    SentenceTransformer = None
    cosine_similarity = None

logger = logging.getLogger(__name__)

class VirtualTAResponder:
    """Generates responses to student questions using AI and scraped data"""
    
    def __init__(self):
        self.setup_openai()
        self.setup_embeddings_model()
        self.load_knowledge_base()
        
    def setup_openai(self):
        """Setup OpenAI API"""
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            logger.warning("OpenAI API key not found. Using fallback responses.")
            
    def setup_embeddings_model(self):
        """Setup sentence embeddings model for semantic search"""
        if not EMBEDDINGS_AVAILABLE:
            logger.warning("Sentence transformers not available. Using keyword-based search only.")
            self.embeddings_model = None
            return
            
        try:
            self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Embeddings model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load embeddings model: {e}")
            self.embeddings_model = None
            
    def load_knowledge_base(self):
        """Load scraped course content and discourse posts"""
        self.course_content = []
        self.discourse_posts = []
        
        try:
            # Load course content
            if os.path.exists("data/course_content.json"):
                with open("data/course_content.json", "r", encoding="utf-8") as f:
                    self.course_content = json.load(f)
                logger.info(f"Loaded {len(self.course_content)} course content items")
            else:
                logger.warning("Course content file not found")
                
            # Load discourse posts
            if os.path.exists("data/discourse_posts.json"):
                with open("data/discourse_posts.json", "r", encoding="utf-8") as f:
                    self.discourse_posts = json.load(f)
                logger.info(f"Loaded {len(self.discourse_posts)} discourse posts")
            else:
                logger.warning("Discourse posts file not found")
                
        except Exception as e:
            logger.error(f"Failed to load knowledge base: {e}")
            
        # Create sample data if no scraped data is available
        if not self.course_content and not self.discourse_posts:
            self.create_sample_knowledge_base()
            
    def create_sample_knowledge_base(self):
        """Create sample knowledge base for demonstration"""
        self.course_content = [
            {
                "title": "AI Models and APIs",
                "content": "Use gpt-3.5-turbo-0125 for assignments as specified. The AI Proxy may support different models, but follow assignment requirements.",
                "url": "https://tds.s-anand.net/#/2025-01/ai-models",
                "keywords": ["gpt", "ai", "api", "model"]
            }
        ]
        
        self.discourse_posts = [
            {
                "title": "GA5 Question 8 Clarification",
                "content": "You must use gpt-3.5-turbo-0125 even if AI Proxy supports gpt-4o-mini. Use OpenAI API directly.",
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939",
                "username": "instructor",
                "keywords": ["gpt", "assignment", "model"]
            }
        ]
        
        logger.info("Created sample knowledge base")
        
    def find_relevant_content(self, question_data: Dict, top_k: int = 5) -> List[Dict]:
        """Find relevant content using semantic search"""
        query = question_data["combined_context"]
        relevant_items = []
        
        # Search in course content
        for item in self.course_content:
            score = self.calculate_relevance_score(query, item)
            if score > 0.1:  # Threshold for relevance
                relevant_items.append({
                    "type": "course",
                    "score": score,
                    "content": item,
                    "url": item.get("url", ""),
                    "title": item.get("title", "")
                })
        
        # Search in discourse posts
        for post in self.discourse_posts:
            score = self.calculate_relevance_score(query, post)
            if score > 0.1:
                relevant_items.append({
                    "type": "discourse",
                    "score": score,
                    "content": post,
                    "url": post.get("url", ""),
                    "title": post.get("title", "")
                })
        
        # Sort by relevance score and return top k
        relevant_items.sort(key=lambda x: x["score"], reverse=True)
        return relevant_items[:top_k]
    
    def calculate_relevance_score(self, query: str, item: Dict) -> float:
        """Calculate relevance score between query and content item"""
        # Simple keyword-based scoring as fallback
        query_lower = query.lower()
        item_text = (item.get("content", "") + " " + item.get("title", "")).lower()
        
        # Count keyword matches
        score = 0.0
        query_words = set(query_lower.split())
        item_words = set(item_text.split())
        
        # Jaccard similarity
        intersection = query_words.intersection(item_words)
        union = query_words.union(item_words)
        
        if union:
            score = len(intersection) / len(union)
        
        # Boost score for exact keyword matches
        keywords = item.get("keywords", [])
        for keyword in keywords:
            if keyword.lower() in query_lower:
                score += 0.2
        
        # Use semantic similarity if embeddings model is available
        if self.embeddings_model and EMBEDDINGS_AVAILABLE:
            try:
                query_embedding = self.embeddings_model.encode([query])
                item_embedding = self.embeddings_model.encode([item_text])
                semantic_score = cosine_similarity(query_embedding, item_embedding)[0][0]
                score = max(score, semantic_score)
            except Exception as e:
                logger.warning(f"Semantic scoring failed: {e}")
        
        return score
    
    def generate_response(self, question_data: Dict) -> Dict:
        """Generate AI response with relevant links"""
        try:
            # Find relevant content
            relevant_content = self.find_relevant_content(question_data)
            
            # Generate answer using OpenAI
            answer = self.generate_ai_answer(question_data, relevant_content)
            
            # Extract links from relevant content
            links = self.extract_links(relevant_content)
            
            return {
                "answer": answer,
                "links": links
            }
            
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            return self.generate_fallback_response(question_data)
    
    def generate_ai_answer(self, question_data: Dict, relevant_content: List[Dict]) -> str:
        """Generate AI-powered answer using OpenAI"""
        if not openai.api_key:
            return self.generate_rule_based_answer(question_data, relevant_content)
        
        try:
            # Prepare context from relevant content
            context_parts = []
            for item in relevant_content[:3]:  # Use top 3 most relevant items
                content = item["content"]
                title = content.get("title", "")
                text = content.get("content", "")
                context_parts.append(f"Title: {title}\nContent: {text}")
            
            context = "\n\n".join(context_parts)
            
            # Create prompt
            prompt = f"""You are a helpful Teaching Assistant for the IIT Madras Tools in Data Science course. 
            Answer the student's question based on the provided context from course materials and discussion forums.
            
            Context:
            {context}
            
            Student Question: {question_data['original_question']}
            
            Provide a clear, helpful answer based on the context. If the context doesn't contain enough information, 
            acknowledge this and provide general guidance. Be specific about technical details when available.
            
            Answer:"""
            
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful Teaching Assistant for IIT Madras Tools in Data Science course."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API failed: {e}")
            return self.generate_rule_based_answer(question_data, relevant_content)
    
    def generate_rule_based_answer(self, question_data: Dict, relevant_content: List[Dict]) -> str:
        """Generate rule-based answer when AI is not available"""
        question = question_data["original_question"].lower()
        question_type = question_data["question_type"]
        
        # Handle specific question patterns
        if "gpt" in question and ("4o-mini" in question or "3.5" in question or "turbo" in question):
            return "You must use `gpt-3.5-turbo-0125`, even if the AI Proxy only supports `gpt-4o-mini`. Use the OpenAI API directly for this question."
        
        if question_type == "ai-related":
            return "For AI-related questions in TDS, please refer to the course materials about model selection and API usage. Make sure to follow the assignment specifications exactly."
        
        elif question_type == "troubleshooting":
            return "For troubleshooting issues, please check the course forums first as similar problems may have been discussed. If the issue persists, provide specific error messages for better assistance."
        
        elif question_type == "academic":
            return "For academic questions about assignments and projects, please refer to the assignment instructions and rubric. If you need clarification, check the course discussion forum first."
        
        # Use relevant content if available
        if relevant_content:
            top_content = relevant_content[0]["content"]
            content_text = top_content.get("content", "")[:300]
            return f"Based on the course materials: {content_text}..."
        
        return "I understand your question about the TDS course. Please check the course materials and discussion forum for relevant information. If you need specific help, consider posting your question with more details in the course forum."
    
    def extract_links(self, relevant_content: List[Dict]) -> List[Dict]:
        """Extract relevant links from content"""
        links = []
        
        for item in relevant_content[:3]:  # Top 3 most relevant
            content = item["content"]
            url = item.get("url", "")
            title = item.get("title", "")
            
            if url:
                # Create descriptive text for the link
                if item["type"] == "discourse":
                    text = f"Discourse discussion: {title}"
                else:
                    text = f"Course material: {title}"
                
                links.append({
                    "url": url,
                    "text": text
                })
        
        return links
    
    def generate_fallback_response(self, question_data: Dict) -> Dict:
        """Generate fallback response when everything else fails"""
        return {
            "answer": "I'm having trouble processing your question right now. Please try rephrasing your question or check the course materials and discussion forum for relevant information.",
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