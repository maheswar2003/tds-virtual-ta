#!/usr/bin/env python3
"""
New responder with advanced content filtering and answer generation.
Completely rewritten from scratch for much better performance.
"""

import json
import os
import re
import logging
from typing import Dict, List, Set, Tuple, Optional
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

class SmartVirtualTAResponder:
    """Advanced responder with intelligent content filtering and answer generation."""
    
    def __init__(self):
        """Initialize responder with better data loading and processing."""
        self.course_content = []
        self.discourse_posts = []
        
        # Junk patterns to filter out garbage content
        self.junk_patterns = [
            r'git\s+(?:push|commit|clone)',
            r'github-actions?',
            r'copy\s+to\s+clipboard',
            r'error\s+copied',
            r'exit\s+\d+',
            r'super-linter',
            r'rawcontent',
            r'statuscode',
            r'```[\s\S]*?```',  # Code blocks
            r'---+',  # Markdown dividers
            r'\[skip\s+ci\]',
            r'release\s+drafter'
        ]
        
        # Answer quality patterns - sentences that make good answers
        self.answer_patterns = [
            r'you\s+(?:must|should|need\s+to|can)',
            r'it\s+is\s+(?:recommended|important|required)',
            r'use\s+\w+\s+(?:for|to|when)',
            r'the\s+(?:recommended|preferred|best)\s+\w+\s+is',
            r'in\s+this\s+course',
            r'for\s+(?:tds|this\s+course)',
            r'(?:students?|you)\s+(?:should|must|need)'
        ]
        
        # Load and process data after patterns are defined
        self.load_and_process_data()
        
    def load_and_process_data(self):
        """Load and preprocess data with better filtering."""
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        course_content_path = os.path.join(project_root, 'data', 'tds_course_content.json')
        discourse_posts_path = os.path.join(project_root, 'data', 'discourse_posts.json')
        
        try:
            # Load course content
            if os.path.exists(course_content_path):
                with open(course_content_path, "r", encoding="utf-8") as f:
                    raw_course_content = json.load(f)
                    self.course_content = self.preprocess_content(raw_course_content, "course")
                logger.info(f"✅ Loaded and processed {len(self.course_content)} course items")
            
            # Load discourse posts  
            if os.path.exists(discourse_posts_path):
                with open(discourse_posts_path, "r", encoding="utf-8") as f:
                    raw_discourse_posts = json.load(f)
                    self.discourse_posts = self.preprocess_content(raw_discourse_posts, "discourse")
                logger.info(f"✅ Loaded and processed {len(self.discourse_posts)} discourse posts")
                
        except Exception as e:
            logger.error(f"⚠️ Error loading data: {e}")
    
    def preprocess_content(self, raw_content: List[Dict], source_type: str) -> List[Dict]:
        """Preprocess content for better searchability."""
        processed = []
        
        for item in raw_content:
            content_text = item.get("content", "")
            title_text = item.get("title", "")
            
            # Skip empty content
            if not content_text or len(content_text.strip()) < 20:
                continue
            
            # Skip junk content
            if self.is_junk_content(content_text):
                continue
            
            # Clean and process content
            cleaned_content = self.clean_content_text(content_text)
            if len(cleaned_content) < 50:  # Skip very short content
                continue
            
            # Extract searchable keywords
            keywords = self.extract_content_keywords(title_text + " " + cleaned_content)
            
            processed_item = {
                "title": title_text.strip(),
                "content": cleaned_content,
                "original_content": content_text,
                "url": item.get("url", ""),
                "keywords": keywords,
                "source": source_type,
                "word_count": len(cleaned_content.split())
            }
            
            processed.append(processed_item)
        
        return processed
    
    def is_junk_content(self, text: str) -> bool:
        """Check if content is junk with better patterns."""
        if not text or len(text.strip()) < 20:
            return True
        
        text_lower = text.lower()
        
        # Check for junk patterns
        junk_count = sum(1 for pattern in self.junk_patterns 
                        if re.search(pattern, text_lower, re.IGNORECASE))
        
        # If more than 20% of patterns match, it's likely junk
        if junk_count > len(self.junk_patterns) * 0.2:
            return True
        
        # Check for excessive repetition
        words = text_lower.split()
        if len(words) > 0:
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # If any word appears more than 30% of the time, it's likely junk
            max_freq = max(word_freq.values())
            if max_freq / len(words) > 0.3:
                return True
        
        return False
    
    def clean_content_text(self, text: str) -> str:
        """Clean content text for better processing."""
        if not text:
            return ""
        
        # Remove junk patterns
        for pattern in self.junk_patterns:
            text = re.sub(pattern, ' ', text, flags=re.IGNORECASE)
        
        # Clean up whitespace and formatting
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove excessive newlines and formatting
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\t+', ' ', text)
        
        # Remove URLs and email addresses
        text = re.sub(r'https?://\S+', '', text)
        text = re.sub(r'\S+@\S+\.\S+', '', text)
        
        # Clean up punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\(\)]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_content_keywords(self, text: str) -> Set[str]:
        """Extract keywords from content for better searchability."""
        if not text:
            return set()
        
        text_lower = text.lower()
        
        # Extract words (3+ characters)
        words = re.findall(r'\b\w{3,}\b', text_lower)
        
        # Stop words to exclude
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'out', 'off', 'down', 'under', 'again', 'further', 'then', 'once',
            'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
            'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so',
            'than', 'too', 'very', 'can', 'will', 'just', 'should', 'now', 'this', 'that',
            'these', 'those', 'they', 'them', 'their', 'what', 'which', 'who', 'whom',
            'whose', 'would', 'could', 'might', 'may', 'shall', 'must', 'ought', 'need'
        }
        
        keywords = {word for word in words if word not in stop_words and len(word) > 2}
        
        return keywords
    
    def calculate_relevance_score(self, question_data: Dict, content_item: Dict) -> float:
        """Calculate relevance score with better algorithms."""
        
        category = question_data.get("category", "general")
        concepts = question_data.get("concepts", set())
        enhanced_search = question_data.get("enhanced_search", "")
        
        content_keywords = content_item.get("keywords", set())
        content_text = content_item.get("content", "").lower()
        title_text = content_item.get("title", "").lower()
        
        score = 0.0
        
        # Base keyword matching
        search_terms = set(enhanced_search.lower().split())
        common_keywords = search_terms.intersection(content_keywords)
        score += len(common_keywords) * 2
        
        # Concept matching
        concept_matches = 0
        for concept in concepts:
            concept_lower = concept.lower()
            if concept_lower in content_text or concept_lower in title_text:
                concept_matches += 1
                score += 5  # Higher weight for concept matches
        
        # Category-specific boosting
        category_boosts = {
            "gpt_api": {
                "keywords": ["gpt-3.5-turbo-0125", "gpt-4o-mini", "openai", "api", "model"],
                "boost": 10
            },
            "containers": {
                "keywords": ["podman", "docker", "container", "windows"],
                "boost": 8
            },
            "ga4_bonus": {
                "keywords": ["ga4", "dashboard", "bonus", "marks"],
                "boost": 7
            },
            "exam_schedule": {
                "keywords": ["exam", "schedule", "date", "roe", "final"],
                "boost": 6
            },
            "course_info": {
                "keywords": ["prerequisite", "course", "structure", "module"],
                "boost": 5
            },
            "tools_usage": {
                "keywords": ["vscode", "vs code", "tools", "development"],
                "boost": 4
            }
        }
        
        if category in category_boosts:
            boost_info = category_boosts[category]
            for keyword in boost_info["keywords"]:
                if keyword in content_text or keyword in title_text:
                    score += boost_info["boost"]
        
        # Source priority (course content > discourse)
        if content_item.get("source") == "course":
            score *= 3  # Strong preference for course content
        
        # Title matching bonus
        if any(term in title_text for term in search_terms):
            score += 8
        
        # Answer quality bonus
        quality_score = 0
        for pattern in self.answer_patterns:
            if re.search(pattern, content_text, re.IGNORECASE):
                quality_score += 2
        score += quality_score
        
        # Content length penalty for very long content (often less relevant)
        word_count = content_item.get("word_count", 0)
        if word_count > 500:
            score *= 0.8
        
        return score
    
    def find_best_matches(self, question_data: Dict, max_results: int = 5) -> List[Dict]:
        """Find best matching content with improved scoring."""
        
        all_content = self.course_content + self.discourse_posts
        scored_results = []
        
        for item in all_content:
            score = self.calculate_relevance_score(question_data, item)
            if score > 0:
                scored_results.append({
                    "score": score,
                    "item": item
                })
        
        # Sort by score and return top results
        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:max_results]
    
    def extract_best_answer(self, content: str, question_data: Dict) -> str:
        """Extract the best answer from content with intelligent sentence selection."""
        
        if not content:
            return "No relevant information found."
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', content)
        
        category = question_data.get("category", "general")
        concepts = question_data.get("concepts", set())
        
        best_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 15 or len(sentence) > 400:
                continue
            
            sentence_score = 0
            sentence_lower = sentence.lower()
            
            # Skip junk sentences
            if any(re.search(pattern, sentence_lower) for pattern in self.junk_patterns):
                continue
            
            # Concept matching
            for concept in concepts:
                if concept.lower() in sentence_lower:
                    sentence_score += 3
            
            # Answer quality patterns
            for pattern in self.answer_patterns:
                if re.search(pattern, sentence_lower):
                    sentence_score += 2
            
            # Category-specific scoring
            if category == "gpt_api" and any(term in sentence_lower for term in ["gpt-3.5-turbo-0125", "gpt-4o-mini", "model", "api"]):
                sentence_score += 5
            elif category == "containers" and any(term in sentence_lower for term in ["podman", "docker", "windows"]):
                sentence_score += 5
            elif category == "exam_schedule" and any(term in sentence_lower for term in ["exam", "date", "schedule"]):
                sentence_score += 5
            
            if sentence_score > 0:
                best_sentences.append((sentence_score, sentence))
        
        if not best_sentences:
            # Fallback: return first clean sentence
            for sentence in sentences:
                sentence = sentence.strip()
                if (len(sentence) > 20 and len(sentence) < 300 and 
                    not any(re.search(pattern, sentence.lower()) for pattern in self.junk_patterns)):
                    return sentence
            return "Information available but requires more specific question."
        
        # Sort by score and combine top sentences
        best_sentences.sort(key=lambda x: x[0], reverse=True)
        
        # Take top 1-2 sentences
        top_sentences = [sent[1] for sent in best_sentences[:2]]
        answer = '. '.join(top_sentences)
        
        # Ensure answer ends properly
        if not answer.endswith('.'):
            answer += '.'
        
        return answer
    
    def generate_response(self, question_data: Dict) -> Dict:
        """Generate comprehensive response with better quality."""
        
        original_question = question_data.get("original_question", "")
        if not original_question:
            return {
                "answer": "Please provide a valid question.",
                "links": []
            }
        
        # Find best matches
        matches = self.find_best_matches(question_data, max_results=3)
        
        if not matches:
            return {
                "answer": f"I couldn't find specific information about your question. Please try rephrasing or being more specific about what you'd like to know regarding the TDS course.",
                "links": []
            }
        
        # Generate answer from best match
        best_match = matches[0]["item"]
        answer = self.extract_best_answer(best_match.get("content", ""), question_data)
        
        # Prepare links
        links = []
        for match in matches:
            item = match["item"]
            
            # Create meaningful title
            title = item.get("title", "")
            if not title:
                # Generate title from content
                content_words = item.get("content", "").split()[:10]
                title = " ".join(content_words) + "..."
            
            if len(title) > 80:
                title = title[:77] + "..."
            
            links.append({
                "text": title,
                "url": item.get("url", ""),
                "score": round(match["score"], 2)
            })
        
        logger.info(f"Generated response with {len(links)} links, best score: {matches[0]['score']:.2f}")
        
        return {
            "answer": answer,
            "links": links
        } 