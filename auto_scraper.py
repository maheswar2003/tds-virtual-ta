#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Automated TDS Scraper (Visible & Robust)
This version is designed to be visible and handle site interactions carefully.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from datetime import datetime
import getpass

class FinalTDSScraper:
    def __init__(self):
        print("🚀 Final Automated TDS Scraper")
        self.setup_browser()

    def setup_browser(self):
        print("🔧 Setting up visible browser...")
        options = Options()
        options.add_argument('--start-maximized')
        # options.add_argument('--headless') # Uncomment for invisible mode
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 20)
            print("✅ Browser opened. You will see its actions.")
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            raise

    def login_to_discourse(self, username, password):
        print("\n🔐 Logging into Discourse...")
        try:
            self.driver.get("https://discourse.onlinedegree.iitm.ac.in/")
            
            # Click initial login button
            login_prompt_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".login-button"))
            )
            login_prompt_button.click()
            print("✅ Clicked initial login prompt.")

            # Enter credentials
            username_field = self.wait.until(EC.presence_of_element_located((By.ID, "login-account-name")))
            password_field = self.driver.find_element(By.ID, "login-account-password")
            
            username_field.send_keys(username)
            password_field.send_keys(password)
            print("✅ Entered credentials.")

            # Click final login button
            login_button = self.driver.find_element(By.ID, "login-button")
            login_button.click()
            print("✅ Submitted login form.")

            # Wait for successful login by looking for user avatar
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".header-dropdown-toggle .avatar")))
            print("✅ Login successful! User avatar is visible.")
            return True

        except TimeoutException:
            print("❌ Login failed: Timed out waiting for an element.")
            print("   Please check your credentials and network. The site might be slow.")
            return False
        except Exception as e:
            print(f"❌ An unexpected error occurred during login: {e}")
            return False

    def scrape_discourse(self):
        print("\n📊 Scraping Discourse posts...")
        posts = []
        try:
            self.driver.get("https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".topic-list-item")))
            
            topic_links_elements = self.driver.find_elements(By.CSS_SELECTOR, ".topic-list-item .title")
            topic_urls = [elem.get_attribute('href') for elem in topic_links_elements if elem.get_attribute('href')]

            for i, url in enumerate(topic_urls[:5]): # Scrape first 5 topics
                try:
                    self.driver.get(url)
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".topic-post")))
                    
                    title = self.driver.find_element(By.CSS_SELECTOR, "h1.title").text.strip()
                    content_element = self.driver.find_element(By.CSS_SELECTOR, ".cooked")
                    content = content_element.text.strip()[:500] + "..." # Truncate content
                    username = self.driver.find_element(By.CSS_SELECTOR, ".username").text.strip()

                    posts.append({
                        "title": title,
                        "content": content,
                        "url": url,
                        "scraped_at": datetime.now().isoformat(),
                        "username": username
                    })
                    print(f"  ✅ Scraped topic: {title[:50]}...")
                except Exception as e:
                    print(f"  ❌ Could not scrape topic at {url}: {e}")
                
            print(f"✅ Finished scraping {len(posts)} posts from Discourse.")
            return posts

        except Exception as e:
            print(f"❌ Failed to scrape Discourse: {e}")
            return posts

    def scrape_course_site(self):
        print("\n📚 Scraping TDS course site...")
        content_items = []
        try:
            self.driver.get("https://tds.s-anand.net/#/2025-01/")
            time.sleep(5) # Wait for this SPA to load

            title = self.driver.title
            content_items.append({
                "title": title,
                "content": "Main page of the Tools in Data Science course for Jan 2025.",
                "url": "https://tds.s-anand.net/#/2025-01/",
                "scraped_at": datetime.now().isoformat()
            })
            print(f"  ✅ Scraped page: {title}")
            
            # You can add more specific selectors here if you know the site structure
            # For now, this is a basic scrape.

            print("✅ Finished scraping course site.")
            return content_items
        except Exception as e:
            print(f"❌ Failed to scrape TDS Course Site: {e}")
            return content_items

    def save_data(self, discourse_posts, course_content):
        print("\n💾 Saving all scraped data...")
        if discourse_posts:
            with open('data/discourse_posts.json', 'w', encoding='utf-8') as f:
                json.dump(discourse_posts, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved {len(discourse_posts)} discourse posts.")

        if course_content:
            with open('data/course_content.json', 'w', encoding='utf-8') as f:
                json.dump(course_content, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved {len(course_content)} course content items.")

    def close_browser(self):
        if hasattr(self, 'driver'):
            print("\n🔒 Closing browser.")
            self.driver.quit()

    def run(self):
        try:
            username = input("Enter your IITM Discourse username: ").strip()
            password = getpass.getpass("Enter your password: ")

            if not username or not password:
                print("❌ Username and password are required.")
                return

            if self.login_to_discourse(username, password):
                discourse_posts = self.scrape_discourse()
                course_content = self.scrape_course_site()
                self.save_data(discourse_posts, course_content)
                print("\n🎉 Scraping complete! Your data files are updated.")
            else:
                print("\n⚠️ Could not complete scraping due to login failure.")

        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
        finally:
            self.close_browser()


if __name__ == "__main__":
    scraper = FinalTDSScraper()
    scraper.run() 