#!/usr/bin/env python3
"""
Simple script to help add real data you find manually
"""

import json
from datetime import datetime

def add_discourse_post():
    """Add a real discourse post"""
    print("\n📝 Adding a real discourse post...")
    
    title = input("Post title: ").strip()
    url = input("Full URL: ").strip()
    content = input("Key content (what it says): ").strip()
    username = input("Username (optional): ").strip() or "student"
    
    post = {
        "title": title,
        "content": content,
        "url": url,
        "username": username,
        "created_at": datetime.now().isoformat(),
        "scraped_at": datetime.now().isoformat(),
        "keywords": title.lower().split()[:3]
    }
    
    return post

def add_course_content():
    """Add real course content"""
    print("\n📚 Adding real course content...")
    
    title = input("Section/topic title: ").strip()
    url = input("Full URL: ").strip()
    content = input("Content description: ").strip()
    
    item = {
        "title": title,
        "content": content,
        "url": url,
        "scraped_at": datetime.now().isoformat(),
        "keywords": title.lower().split()[:3]
    }
    
    return item

def main():
    """Main function"""
    print("🎯 REAL DATA ADDER")
    print("=" * 40)
    print("This helps you add real data you find manually")
    print("=" * 40)
    
    # Load existing data
    try:
        with open('data/discourse_posts.json', 'r', encoding='utf-8') as f:
            discourse_posts = json.load(f)
    except:
        discourse_posts = []
    
    try:
        with open('data/course_content.json', 'r', encoding='utf-8') as f:
            course_content = json.load(f)
    except:
        course_content = []
    
    print(f"\nCurrent data:")
    print(f"📊 Discourse posts: {len(discourse_posts)}")
    print(f"📚 Course content: {len(course_content)}")
    
    while True:
        print("\nWhat do you want to add?")
        print("1. Discourse post")
        print("2. Course content")
        print("3. Done")
        
        choice = input("Choice (1-3): ").strip()
        
        if choice == "1":
            post = add_discourse_post()
            discourse_posts.append(post)
            print("✅ Added discourse post!")
            
        elif choice == "2":
            content = add_course_content()
            course_content.append(content)
            print("✅ Added course content!")
            
        elif choice == "3":
            break
        else:
            print("Invalid choice")
    
    # Save updated data
    with open('data/discourse_posts.json', 'w', encoding='utf-8') as f:
        json.dump(discourse_posts, f, indent=2, ensure_ascii=False)
    
    with open('data/course_content.json', 'w', encoding='utf-8') as f:
        json.dump(course_content, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved!")
    print(f"📊 Total discourse posts: {len(discourse_posts)}")
    print(f"📚 Total course content: {len(course_content)}")

if __name__ == "__main__":
    main() 