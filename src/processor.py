#!/usr/bin/env python3
"""
Question processor - handles text and image inputs
"""

import base64
import logging
import re
from typing import Dict, List
import io

# Try to import image processing stuff
try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    print("Warning: PIL not available, image processing disabled")
    HAVE_PIL = False

try:
    from transformers import BlipProcessor, BlipForConditionalGeneration
    import torch
    HAVE_TRANSFORMERS = True
except ImportError:
    print("Warning: Transformers not available, advanced image processing disabled")
    HAVE_TRANSFORMERS = False

logger = logging.getLogger(__name__)

class QuestionProcessor:
    """Processes questions and images from students"""
    
    def __init__(self):
        # Try to set up image processing
        self.image_processor = None
        self.image_model = None
        
        if HAVE_TRANSFORMERS and HAVE_PIL:
            try:
                print("Loading image processing model...")
                self.image_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
                self.image_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
                print("✓ Image processor ready")
            except Exception as e:
                print(f"⚠ Couldn't load image model: {e}")
        else:
            print("⚠ Image processing not available")
    
    def process_question(self, question: str, image_data: str = None) -> Dict:
        """
        Process a student question with optional image
        
        Returns dict with processed data
        """
        # Clean up the question text
        cleaned = self.clean_question(question)
        
        # Extract keywords
        keywords = self.get_keywords(question)
        
        # Classify question type
        q_type = self.classify_question(question)
        
        result = {
            "original_question": question,
            "cleaned_question": cleaned,
            "keywords": keywords,
            "question_type": q_type,
            "image_description": None,
            "combined_context": question
        }
        
        # Handle image if provided
        if image_data:
            try:
                img_desc = self.process_image(image_data)
                result["image_description"] = img_desc
                result["combined_context"] = f"{question}\n\nImage: {img_desc}"
            except Exception as e:
                print(f"Image processing failed: {e}")
                result["image_description"] = "Image processing failed"
        
        return result
    
    def clean_question(self, text: str) -> str:
        """Clean up the question text"""
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Keep only alphanumeric and basic punctuation
        text = re.sub(r'[^\w\s\.\?\!\-\(\)]', '', text)
        
        return text
    
    def get_keywords(self, text: str) -> List[str]:
        """Extract important keywords from the question"""
        # TDS course related keywords
        course_keywords = [
            'gpt', 'openai', 'ai', 'model', 'api', 'proxy',
            'python', 'jupyter', 'notebook', 'pandas', 'numpy',
            'assignment', 'project', 'ga', 'grading', 'submission',
            'error', 'help', 'problem', 'install', 'setup',
            'data', 'science', 'tools', 'library', 'package'
        ]
        
        text_lower = text.lower()
        found = []
        
        # Check for course keywords
        for keyword in course_keywords:
            if keyword in text_lower:
                found.append(keyword)
        
        # Find technical terms (words with numbers, capitals, hyphens)
        tech_terms = re.findall(r'\b[A-Z]{2,}\b|\b\w*\d+\w*\b|\b[a-z]+-[a-z]+\b', text)
        found.extend(tech_terms)
        
        return list(set(found))  # Remove duplicates
    
    def classify_question(self, text: str) -> str:
        """Figure out what type of question this is"""
        text = text.lower()
        
        # Check for error/problem keywords
        if any(word in text for word in ['error', 'bug', 'problem', 'issue', 'not working', 'broken']):
            return "troubleshooting"
        
        # Check for how-to questions
        if any(phrase in text for phrase in ['how to', 'how do', 'how can', 'tutorial', 'guide']):
            return "how-to"
        
        # Check for definition questions
        if any(phrase in text for phrase in ['what is', 'what are', 'define', 'explain', 'meaning']):
            return "definition"
        
        # Check for assignment/academic questions
        if any(word in text for word in ['assignment', 'project', 'submission', 'grading', 'ga', 'marks']):
            return "academic"
        
        # Check for AI/model related questions
        if any(word in text for word in ['gpt', 'ai', 'model', 'api', 'openai']):
            return "ai-related"
        
        return "general"
    
    def process_image(self, image_data: str) -> str:
        """Process base64 image and get description"""
        if not HAVE_PIL:
            return "Image processing not available"
            
        if not self.image_processor:
            return "Image model not loaded"
        
        try:
            # Decode the base64 image
            img_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(img_bytes))
            
            # Make sure it's RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Generate description using BLIP model
            inputs = self.image_processor(image, return_tensors="pt")
            
            with torch.no_grad():
                output = self.image_model.generate(**inputs, max_length=50)
                description = self.image_processor.decode(output[0], skip_special_tokens=True)
            
            # Add some basic analysis
            width, height = image.size
            layout_info = ""
            
            if width > height * 1.5:
                layout_info = " (wide layout - possibly interface/dashboard)"
            elif height > width * 1.5:
                layout_info = " (tall layout - possibly document/chat)"
            
            return f"Image shows: {description}{layout_info}"
            
        except Exception as e:
            print(f"Error processing image: {e}")
            return f"Image processing error: {str(e)}" 