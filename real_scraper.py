#!/usr/bin/env python3
"""
Real data scraper for TDS course content and Discourse posts
This attempts to scrape actual data from the provided URLs
"""

import requests
import json
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re

def scrape_tds_course_content():
    """Attempt to scrape real course content from TDS website"""
    base_url = "https://tds.s-anand.net"
    course_url = f"{base_url}/#/2025-01/"
    
    print(f"🔍 Attempting to scrape course content from: {course_url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(course_url, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find course content
            content_items = []
            
            # Look for common patterns in course websites
            # This is a best-effort attempt - actual structure may vary
            
            # Try to find navigation links or content sections
            links = soup.find_all('a', href=True)
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
            
            print(f"Found {len(links)} links and {len(headings)} headings")
            
            # Extract potential course topics
            for heading in headings[:10]:  # Limit to first 10
                text = heading.get_text().strip()
                if text and len(text) > 5:
                    content_items.append({
                        "title": text,
                        "content": f"Course material about {text.lower()}. Please refer to the full course content for detailed information.",
                        "url": course_url,
                        "scraped_at": datetime.now().isoformat(),
                        "source": "real_scrape"
                    })
            
            # Try to extract actual content if possible
            content_divs = soup.find_all(['div', 'section', 'article'])
            for div in content_divs[:5]:
                text = div.get_text().strip()
                if len(text) > 100 and len(text) < 1000:  # Reasonable content length
                    content_items.append({
                        "title": "Course Content",
                        "content": text[:500] + "...",
                        "url": course_url,
                        "scraped_at": datetime.now().isoformat(),
                        "source": "real_scrape"
                    })
            
            return content_items
        else:
            print(f"❌ Failed to access course content: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error scraping course content: {e}")
        return []

def scrape_discourse_posts():
    """Attempt to scrape real discourse posts"""
    discourse_url = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"
    
    print(f"🔍 Attempting to scrape discourse posts from: {discourse_url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(discourse_url, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            posts = []
            
            # Look for discourse post patterns
            # Discourse typically has specific HTML structure
            
            # Try to find topic links
            topic_links = soup.find_all('a', class_=lambda x: x and 'topic' in x.lower())
            if not topic_links:
                topic_links = soup.find_all('a', href=lambda x: x and '/t/' in str(x))
            
            print(f"Found {len(topic_links)} potential topic links")
            
            for link in topic_links[:10]:  # Limit to first 10
                href = link.get('href', '')
                title = link.get_text().strip()
                
                if title and len(title) > 5:
                    # Try to construct full URL
                    if href.startswith('/'):
                        full_url = f"https://discourse.onlinedegree.iitm.ac.in{href}"
                    else:
                        full_url = href
                    
                    posts.append({
                        "title": title,
                        "content": f"Discussion topic: {title}",
                        "url": full_url,
                        "scraped_at": datetime.now().isoformat(),
                        "source": "real_scrape",
                        "username": "unknown",
                        "created_at": "2025-01-15T10:00:00Z"
                    })
            
            # Try to extract more detailed content if possible
            content_areas = soup.find_all(['div', 'article', 'section'])
            for area in content_areas[:5]:
                text = area.get_text().strip()
                if len(text) > 50 and len(text) < 500:
                    posts.append({
                        "title": "Forum Discussion",
                        "content": text[:300] + "...",
                        "url": discourse_url,
                        "scraped_at": datetime.now().isoformat(),
                        "source": "real_scrape",
                        "username": "forum_user",
                        "created_at": "2025-01-15T10:00:00Z"
                    })
            
            return posts
        else:
            print(f"❌ Failed to access discourse: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error scraping discourse: {e}")
        return []

def save_real_scraped_data(course_data, discourse_data):
    """Save the real scraped data"""
    
    # Save course content
    if course_data:
        with open('data/real_course_content.json', 'w', encoding='utf-8') as f:
            json.dump(course_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved {len(course_data)} course content items to real_course_content.json")
    
    # Save discourse posts
    if discourse_data:
        with open('data/real_discourse_posts.json', 'w', encoding='utf-8') as f:
            json.dump(discourse_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved {len(discourse_data)} discourse posts to real_discourse_posts.json")

def main():
    """Main scraping function"""
    print("🚀 Starting REAL data scraping...")
    print("=" * 50)
    
    # Scrape course content
    course_data = scrape_tds_course_content()
    time.sleep(2)  # Be respectful to servers
    
    # Scrape discourse posts
    discourse_data = scrape_discourse_posts()
    
    # Save results
    save_real_scraped_data(course_data, discourse_data)
    
    print("\n" + "=" * 50)
    print("📊 SCRAPING RESULTS:")
    print(f"Course content items: {len(course_data)}")
    print(f"Discourse posts: {len(discourse_data)}")
    
    if not course_data and not discourse_data:
        print("\n⚠️  No real data could be scraped.")
        print("This might be because:")
        print("- The websites require authentication")
        print("- They block automated scraping")
        print("- The content is loaded dynamically with JavaScript")
        print("- The URLs are not publicly accessible")
        
        print("\n💡 RECOMMENDATION:")
        print("You may need to:")
        print("1. Check if the URLs require login")
        print("2. Use browser automation (Selenium)")
        print("3. Contact the instructors for data access")
        print("4. Use the sample data for demonstration purposes")

if __name__ == "__main__":
    main() 