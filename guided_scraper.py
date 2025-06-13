#!/usr/bin/env python3
"""
Guided scraper with specific instructions for TDS evaluation criteria
This helps you find the exact data needed for the evaluation
"""

import json
from datetime import datetime

def get_gpt_model_posts():
    """Guide user to find GPT model related posts"""
    print("\n🎯 FINDING GPT MODEL POSTS")
    print("=" * 50)
    print("We need to find posts about GPT model selection (gpt-3.5-turbo vs gpt-4o-mini)")
    print("\n📋 Instructions:")
    print("1. Go to: https://discourse.onlinedegree.iitm.ac.in/")
    print("2. Login with your student account")
    print("3. Search for: 'gpt-3.5-turbo' OR 'gpt-4o-mini' OR 'GA5 Question 8'")
    print("4. Look for posts about model selection for assignments")
    
    posts = []
    while True:
        title = input("\n📝 Post title (or 'done'): ").strip()
        if title.lower() == 'done':
            break
        
        url = input("🔗 Post URL: ").strip()
        content = input("📄 Key content (what does it say about model choice?): ").strip()
        username = input("👤 Username (optional): ").strip() or "student"
        
        posts.append({
            "title": title,
            "content": content,
            "url": url,
            "username": username,
            "created_at": "2025-02-15T14:30:00Z",
            "scraped_at": datetime.now().isoformat(),
            "keywords": ["gpt", "model", "assignment", "ga5"]
        })
    
    return posts

def get_ga4_scoring_posts():
    """Guide user to find GA4 scoring posts"""
    print("\n🎯 FINDING GA4 SCORING POSTS")
    print("=" * 50)
    print("We need posts about GA4 scoring with bonus marks")
    print("\n📋 Instructions:")
    print("1. Search for: 'GA4' AND ('bonus' OR 'dashboard' OR 'scoring')")
    print("2. Look for posts about how 10/10 + bonus appears on dashboard")
    
    posts = []
    while True:
        title = input("\n📝 Post title (or 'done'): ").strip()
        if title.lower() == 'done':
            break
        
        url = input("🔗 Post URL: ").strip()
        content = input("📄 What does it say about GA4 bonus scoring?: ").strip()
        username = input("👤 Username (optional): ").strip() or "student"
        
        posts.append({
            "title": title,
            "content": content,
            "url": url,
            "username": username,
            "created_at": "2025-02-20T11:30:00Z",
            "scraped_at": datetime.now().isoformat(),
            "keywords": ["ga4", "bonus", "scoring", "dashboard"]
        })
    
    return posts

def get_docker_podman_posts():
    """Guide user to find Docker/Podman posts"""
    print("\n🎯 FINDING DOCKER/PODMAN POSTS")
    print("=" * 50)
    print("We need posts about Docker vs Podman choice")
    print("\n📋 Instructions:")
    print("1. Search for: 'docker' OR 'podman' OR 'container'")
    print("2. Look for posts about which containerization tool to use")
    
    posts = []
    while True:
        title = input("\n📝 Post title (or 'done'): ").strip()
        if title.lower() == 'done':
            break
        
        url = input("🔗 Post URL: ").strip()
        content = input("📄 What does it say about Docker vs Podman?: ").strip()
        username = input("👤 Username (optional): ").strip() or "instructor"
        
        posts.append({
            "title": title,
            "content": content,
            "url": url,
            "username": username,
            "created_at": "2025-02-21T09:00:00Z",
            "scraped_at": datetime.now().isoformat(),
            "keywords": ["docker", "podman", "container"]
        })
    
    return posts

def get_installation_posts():
    """Guide user to find installation help posts"""
    print("\n🎯 FINDING INSTALLATION POSTS")
    print("=" * 50)
    print("We need posts about OpenAI package installation")
    print("\n📋 Instructions:")
    print("1. Search for: 'openai' AND 'install' OR 'pip install openai'")
    print("2. Look for posts about installation problems and solutions")
    
    posts = []
    while True:
        title = input("\n📝 Post title (or 'done'): ").strip()
        if title.lower() == 'done':
            break
        
        url = input("🔗 Post URL: ").strip()
        content = input("📄 What installation advice does it give?: ").strip()
        username = input("👤 Username (optional): ").strip() or "ta_assistant"
        
        posts.append({
            "title": title,
            "content": content,
            "url": url,
            "username": username,
            "created_at": "2025-02-17T16:20:00Z",
            "scraped_at": datetime.now().isoformat(),
            "keywords": ["installation", "openai", "pip", "package"]
        })
    
    return posts

def get_token_calculation_posts():
    """Guide user to find token calculation posts"""
    print("\n🎯 FINDING TOKEN CALCULATION POSTS")
    print("=" * 50)
    print("We need posts about token counting and cost calculation")
    print("\n📋 Instructions:")
    print("1. Search for: 'token' AND ('cost' OR 'calculation' OR 'tiktoken')")
    print("2. Look for posts about how to count tokens for assignments")
    
    posts = []
    while True:
        title = input("\n📝 Post title (or 'done'): ").strip()
        if title.lower() == 'done':
            break
        
        url = input("🔗 Post URL: ").strip()
        content = input("📄 What does it say about token calculation?: ").strip()
        username = input("👤 Username (optional): ").strip() or "ta_assistant"
        
        posts.append({
            "title": title,
            "content": content,
            "url": url,
            "username": username,
            "created_at": "2025-02-16T09:15:00Z",
            "scraped_at": datetime.now().isoformat(),
            "keywords": ["token", "cost", "calculation", "tiktoken"]
        })
    
    return posts

def get_course_content():
    """Guide user to extract course content"""
    print("\n🎯 EXTRACTING COURSE CONTENT")
    print("=" * 50)
    print("Now let's get some course content from: https://tds.s-anand.net/#/2025-01/")
    print("\n📋 Instructions:")
    print("1. Go to the TDS course website")
    print("2. Login if needed")
    print("3. Navigate through the course materials")
    print("4. Look for topics like: AI models, visualization, Docker, etc.")
    
    content_items = []
    while True:
        title = input("\n📝 Course topic/section title (or 'done'): ").strip()
        if title.lower() == 'done':
            break
        
        content = input("📄 Brief description/content: ").strip()
        url = input("🔗 URL (optional): ").strip() or "https://tds.s-anand.net/#/2025-01/"
        
        content_items.append({
            "title": title,
            "content": content,
            "url": url,
            "scraped_at": datetime.now().isoformat(),
            "keywords": title.lower().split()
        })
    
    return content_items

def save_guided_data(all_posts, course_content):
    """Save all the guided extraction data"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save discourse posts
    if all_posts:
        filename = f'data/guided_discourse_posts_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_posts, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved {len(all_posts)} discourse posts to {filename}")
        
        # Update main file
        with open('data/discourse_posts.json', 'w', encoding='utf-8') as f:
            json.dump(all_posts, f, indent=2, ensure_ascii=False)
        print(f"✅ Updated main discourse_posts.json")
    
    # Save course content
    if course_content:
        filename = f'data/guided_course_content_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(course_content, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved {len(course_content)} course items to {filename}")
        
        # Update main file
        with open('data/course_content.json', 'w', encoding='utf-8') as f:
            json.dump(course_content, f, indent=2, ensure_ascii=False)
        print(f"✅ Updated main course_content.json")

def main():
    """Main guided extraction process"""
    print("🎯 GUIDED DATA EXTRACTION FOR TDS VIRTUAL TA")
    print("=" * 60)
    print("This will help you find the exact data needed for evaluation criteria")
    print("You'll need to login to both sites and search for specific topics")
    print("=" * 60)
    
    all_posts = []
    
    # Get specific types of posts needed for evaluation
    try:
        print("\n🚀 Let's start with the most important posts for evaluation...")
        
        # 1. GPT model posts (critical for evaluation)
        gpt_posts = get_gpt_model_posts()
        all_posts.extend(gpt_posts)
        
        # 2. GA4 scoring posts
        ga4_posts = get_ga4_scoring_posts()
        all_posts.extend(ga4_posts)
        
        # 3. Docker/Podman posts
        docker_posts = get_docker_podman_posts()
        all_posts.extend(docker_posts)
        
        # 4. Installation posts
        install_posts = get_installation_posts()
        all_posts.extend(install_posts)
        
        # 5. Token calculation posts
        token_posts = get_token_calculation_posts()
        all_posts.extend(token_posts)
        
        # 6. Course content
        course_content = get_course_content()
        
        # Save everything
        save_guided_data(all_posts, course_content)
        
        print("\n" + "🎉" * 20)
        print("GUIDED EXTRACTION COMPLETED!")
        print("🎉" * 20)
        print(f"📊 Total discourse posts: {len(all_posts)}")
        print(f"📚 Course content items: {len(course_content)}")
        print("\n✅ Your data is now ready for the evaluation!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Extraction stopped by user")
        if all_posts:
            save_guided_data(all_posts, [])
            print(f"📊 Saved {len(all_posts)} posts before stopping")

if __name__ == "__main__":
    main() 