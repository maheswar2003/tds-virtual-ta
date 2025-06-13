#!/usr/bin/env python3
"""
Question processor for handling text and image inputs
"""

import base64
import logging
import re
from typing import Dict, Optional, List
import io

# Try to import optional dependencies
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    Image = None

try:
    from transformers import BlipProcessor, BlipForConditionalGeneration
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

logger = logging.getLogger(__name__)

class QuestionProcessor:
    """Processes student questions and optional image attachments"""
    
    def __init__(self):
        self.setup_image_processor()
        
    def setup_image_processor(self):
        """Setup image processing model for visual question answering"""
        if not TRANSFORMERS_AVAILABLE or not PIL_AVAILABLE:
            logger.warning("Image processing dependencies not available. Image processing will be limited.")
            self.image_processor = None
            self.image_model = None
            return
            
        try:
            self.image_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.image_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            logger.info("Image processor initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize image processor: {e}")
            self.image_processor = None
            self.image_model = None
    
    def process_question(self, question: str, image_data: Optional[str] = None) -> Dict:
        """
        Process a student question with optional image attachment
        
        Args:
            question: The student's question text
            image_data: Base64 encoded image data (optional)
            
        Returns:
            Dict containing processed question data
        """
        processed_data = {
            "original_question": question,
            "cleaned_question": self.clean_text(question),
            "keywords": self.extract_keywords(question),
            "question_type": self.classify_question(question),
            "image_description": None,
            "combined_context": question
        }
        
        # Process image if provided
        if image_data:
            try:
                image_description = self.process_image(image_data)
                processed_data["image_description"] = image_description
                processed_data["combined_context"] = f"{question}\n\nImage content: {image_description}"
            except Exception as e:
                logger.error(f"Failed to process image: {e}")
                processed_data["image_description"] = "Image processing failed"
        
        return processed_data
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep essential punctuation
        text = re.sub(r'[^\w\s\.\?\!\-\(\)]', '', text)
        
        return text
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from the question"""
        # Common TDS-related keywords
        tds_keywords = [
            'gpt', 'openai', 'ai proxy', 'model', 'token', 'api',
            'data science', 'python', 'jupyter', 'notebook',
            'assignment', 'project', 'grading', 'submission',
            'discord', 'discourse', 'help', 'error', 'bug',
            'tool', 'library', 'package', 'install', 'setup'
        ]
        
        text_lower = text.lower()
        found_keywords = []
        
        for keyword in tds_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        # Extract technical terms (words with numbers, acronyms, etc.)
        technical_terms = re.findall(r'\b[A-Z]{2,}\b|\b\w*\d+\w*\b|\b[a-z]+-[a-z]+\b', text)
        found_keywords.extend(technical_terms)
        
        return list(set(found_keywords))
    
    def classify_question(self, text: str) -> str:
        """Classify the type of question"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['error', 'bug', 'problem', 'issue', 'not working']):
            return "troubleshooting"
        elif any(word in text_lower for word in ['how to', 'how do', 'tutorial', 'guide']):
            return "how-to"
        elif any(word in text_lower for word in ['what is', 'what are', 'define', 'explain']):
            return "definition"
        elif any(word in text_lower for word in ['assignment', 'project', 'submission', 'grading']):
            return "academic"
        elif any(word in text_lower for word in ['gpt', 'ai', 'model', 'api']):
            return "ai-related"
        else:
            return "general"
    
    def process_image(self, image_data: str) -> str:
        """Process base64 image and extract description"""
        if not PIL_AVAILABLE:
            return "Image processing not available - PIL not installed"
            
        if not self.image_processor or not self.image_model:
            return "Image processing model not available"
        
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Generate caption
            inputs = self.image_processor(image, return_tensors="pt")
            
            with torch.no_grad():
                out = self.image_model.generate(**inputs, max_length=100)
                caption = self.image_processor.decode(out[0], skip_special_tokens=True)
            
            # Try to extract text from image using OCR-like description
            text_description = self.extract_text_description(image)
            
            combined_description = f"Image shows: {caption}"
            if text_description:
                combined_description += f". Text/interface elements: {text_description}"
            
            return combined_description
            
        except Exception as e:
            logger.error(f"Image processing failed: {e}")
            return f"Unable to process image: {str(e)}"
    
    def extract_text_description(self, image) -> str:
        """Extract text-like elements from image (simplified)"""
        if not PIL_AVAILABLE or image is None:
            return ""
            
        # Basic analysis based on image properties
        width, height = image.size
        
        descriptions = []
        
        if width > height * 1.5:
            descriptions.append("wide layout suggesting interface/dashboard")
        elif height > width * 1.5:
            descriptions.append("tall layout suggesting document/chat")
        
        # Add more heuristics based on your specific use case
        return ", ".join(descriptions) if descriptions else "" 