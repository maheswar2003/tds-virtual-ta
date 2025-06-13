#!/usr/bin/env python3
"""
Web scraper for TDS course content and Discourse posts
"""

import requests
import json
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

class TDSScraper:
    """Scraper for TDS course content and Discourse posts"""
    
    def __init__(self):
        self.course_base_url = "https://tds.s-anand.net/#/2025-01/"
        self.discourse_base_url = "https://discourse.onlinedegree.iitm.ac.in"
        self.discourse_category_url = f"{self.discourse_base_url}/c/courses/tds-kb/34"
        
    def setup_driver(self) -> webdriver.Chrome:
        """Setup Chrome driver for web scraping"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            driver = webdriver.Chrome(
                service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            return driver
        except Exception as e:
            logger.error(f"Failed to setup Chrome driver: {e}")
            raise
    
    def scrape_course_content(self) -> List[Dict]:
        """Scrape TDS course content"""
        logger.info("Starting course content scraping...")
        
        course_data = []
        driver = None
        
        try:
            driver = self.setup_driver()
            driver.get(self.course_base_url)
            
            # Wait for content to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extract main content sections
            sections = driver.find_elements(By.CSS_SELECTOR, ".content-section, .lesson, .topic")
            
            for section in sections:
                try:
                    title = section.find_element(By.CSS_SELECTOR, "h1, h2, h3, .title").text
                    content = section.get_attribute("innerText")
                    
                    # Extract links
                    links = []
                    link_elements = section.find_elements(By.TAG_NAME, "a")
                    for link in link_elements:
                        href = link.get_attribute("href")
                        text = link.text.strip()
                        if href and text:
                            links.append({"url": href, "text": text})
                    
                    course_data.append({
                        "title": title,
                        "content": content,
                        "links": links,
                        "url": driver.current_url,
                        "scraped_at": datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    logger.warning(f"Failed to extract section data: {e}")
                    continue
            
            # Navigate through different pages/sections
            nav_links = driver.find_elements(By.CSS_SELECTOR, ".nav a, .menu a")
            for nav_link in nav_links[:10]:  # Limit to avoid infinite loops
                try:
                    href = nav_link.get_attribute("href")
                    if href and "2025-01" in href:
                        driver.get(href)
                        time.sleep(2)
                        
                        # Extract content from this page
                        page_content = driver.find_element(By.TAG_NAME, "body").get_attribute("innerText")
                        course_data.append({
                            "title": driver.title,
                            "content": page_content,
                            "url": href,
                            "scraped_at": datetime.now().isoformat()
                        })
                        
                except Exception as e:
                    logger.warning(f"Failed to navigate to {href}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Course content scraping failed: {e}")
        finally:
            if driver:
                driver.quit()
        
        logger.info(f"Scraped {len(course_data)} course content items")
        return course_data
    
    def scrape_discourse_posts(self, start_date: str = "2025-01-01", end_date: str = "2025-04-14") -> List[Dict]:
        """Scrape Discourse posts from TDS category within date range"""
        logger.info(f"Starting Discourse scraping from {start_date} to {end_date}...")
        
        posts_data = []
        
        try:
            # Get category page
            response = requests.get(f"{self.discourse_category_url}.json")
            if response.status_code != 200:
                logger.error(f"Failed to fetch Discourse category: {response.status_code}")
                return posts_data
            
            category_data = response.json()
            
            # Extract topic IDs
            topic_ids = []
            if "topic_list" in category_data and "topics" in category_data["topic_list"]:
                for topic in category_data["topic_list"]["topics"]:
                    topic_created = datetime.fromisoformat(topic["created_at"].replace("Z", "+00:00"))
                    start_dt = datetime.fromisoformat(start_date + "T00:00:00+00:00")
                    end_dt = datetime.fromisoformat(end_date + "T23:59:59+00:00")
                    
                    if start_dt <= topic_created <= end_dt:
                        topic_ids.append(topic["id"])
            
            # Scrape individual topics
            for topic_id in topic_ids[:50]:  # Limit to avoid rate limiting
                try:
                    topic_url = f"{self.discourse_base_url}/t/{topic_id}.json"
                    response = requests.get(topic_url)
                    
                    if response.status_code == 200:
                        topic_data = response.json()
                        
                        # Extract posts from topic
                        if "post_stream" in topic_data and "posts" in topic_data["post_stream"]:
                            for post in topic_data["post_stream"]["posts"]:
                                posts_data.append({
                                    "topic_id": topic_id,
                                    "post_id": post["id"],
                                    "title": topic_data.get("title", ""),
                                    "content": post.get("cooked", ""),
                                    "raw_content": post.get("raw", ""),
                                    "username": post.get("username", ""),
                                    "created_at": post.get("created_at", ""),
                                    "url": f"{self.discourse_base_url}/t/{topic_id}/{post['post_number']}",
                                    "scraped_at": datetime.now().isoformat()
                                })
                    
                    time.sleep(0.5)  # Rate limiting
                    
                except Exception as e:
                    logger.warning(f"Failed to scrape topic {topic_id}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Discourse scraping failed: {e}")
        
        logger.info(f"Scraped {len(posts_data)} Discourse posts")
        return posts_data
    
    def save_scraped_data(self, course_data: List[Dict], discourse_data: List[Dict]):
        """Save scraped data to JSON files"""
        import os
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Save course content
        with open("data/course_content.json", "w", encoding="utf-8") as f:
            json.dump(course_data, f, indent=2, ensure_ascii=False)
        
        # Save discourse posts
        with open("data/discourse_posts.json", "w", encoding="utf-8") as f:
            json.dump(discourse_data, f, indent=2, ensure_ascii=False)
        
        logger.info("Scraped data saved to data/ directory")

def main():
    """Main scraping function"""
    scraper = TDSScraper()
    
    # Scrape course content
    course_data = scraper.scrape_course_content()
    
    # Scrape discourse posts
    discourse_data = scraper.scrape_discourse_posts()
    
    # Save data
    scraper.save_scraped_data(course_data, discourse_data)
    
    print(f"Scraping completed!")
    print(f"Course content items: {len(course_data)}")
    print(f"Discourse posts: {len(discourse_data)}")

if __name__ == "__main__":
    main() 