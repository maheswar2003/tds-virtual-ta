# 📚 TDS Data Scraping Guide

## 🎯 Overview
This guide helps you scrape real data from both TDS sites using your student access. You have two options:

1. **Interactive Scraper** (`interactive_scraper.py`) - Uses Selenium to automate browser
2. **Guided Scraper** (`guided_scraper.py`) - Manual extraction with prompts
3. **Manual Scraping** - Step by step instructions

## 🚀 Quick Start Options

### Option 1: Interactive Scraper (Recommended)
```bash
py interactive_scraper.py
```
- Opens browser automatically
- Guides you through login process
- Attempts automatic extraction
- Falls back to manual prompts if needed

### Option 2: Guided Scraper (Simple)
```bash
py guided_scraper.py
```
- No browser automation
- Step-by-step prompts for specific data
- You manually navigate and copy content
- Focuses on evaluation criteria data

## 🔐 Authentication Requirements

### TDS Course Site
- **URL**: https://tds.s-anand.net/#/2025-01/
- **Login**: Use your IITM student credentials
- **What to look for**:
  - Course syllabus and materials
  - Assignment instructions
  - AI model usage guidelines
  - Docker/containerization info

### Discourse Forum
- **URL**: https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34
- **Login**: Use your IITM student credentials
- **What to look for**:
  - Posts about GPT model selection (gpt-3.5-turbo vs gpt-4o-mini)
  - GA4 scoring and bonus marks discussions
  - Installation help and troubleshooting
  - Docker vs Podman discussions

## 🎯 Critical Data for Evaluation

### 1. GPT Model Posts (MOST IMPORTANT)
**Search terms**: "gpt-3.5-turbo", "gpt-4o-mini", "GA5 Question 8"
**What to find**: Posts that clarify which model to use for assignments

### 2. GA4 Scoring Posts
**Search terms**: "GA4", "bonus", "dashboard", "scoring"
**What to find**: How bonus marks appear on dashboard (e.g., "110" for 10/10 + bonus)

### 3. Installation Posts
**Search terms**: "openai install", "pip install openai", "package installation"
**What to find**: Help with installing Python packages

### 4. Docker/Container Posts
**Search terms**: "docker", "podman", "container"
**What to find**: Which containerization tool to use

### 5. Token Calculation Posts
**Search terms**: "token", "cost", "tiktoken", "calculation"
**What to find**: How to count tokens for cost calculation

## 📝 Manual Scraping Instructions

### Step 1: Login to Discourse
1. Go to: https://discourse.onlinedegree.iitm.ac.in/
2. Click "Log In"
3. Use your IITM student credentials
4. Navigate to: TDS Knowledge Base category

### Step 2: Search for Key Topics
For each search term above:
1. Use the search box (🔍 icon)
2. Filter by category: "TDS Knowledge Base"
3. Filter by date: Jan 1, 2025 - Apr 14, 2025
4. Copy post titles, URLs, and key content

### Step 3: Login to TDS Course Site
1. Go to: https://tds.s-anand.net/#/2025-01/
2. Login if required
3. Navigate through course materials
4. Look for sections on:
   - AI/ML models
   - Assignment instructions
   - Technical requirements
   - Course syllabus

### Step 4: Save Data
For each piece of content found:
```json
{
  "title": "Post/section title",
  "content": "Key content or summary",
  "url": "Direct URL",
  "username": "poster username",
  "created_at": "2025-02-15T14:30:00Z",
  "keywords": ["relevant", "keywords"]
}
```

## 🛠️ Tools Available

### Interactive Scraper Features
- Automatic Chrome browser launch
- Guided login process
- Automatic content extraction attempts
- Manual fallback prompts
- Saves timestamped backups
- Updates main data files

### Guided Scraper Features
- No browser automation required
- Targeted prompts for specific data types
- Focus on evaluation criteria
- Simple command-line interface
- Direct file updates

## 🎯 Expected Results

After scraping, you should have:
- **5-10 course content items** from TDS site
- **8-15 discourse posts** covering key topics
- **Real URLs** pointing to actual content
- **Authentic timestamps** from actual posts
- **Diverse content types** (questions, answers, discussions)

## 🚨 Important Notes

1. **Respect Rate Limits**: Don't scrape too aggressively
2. **Student Access Only**: Only scrape content you have legitimate access to
3. **Privacy**: Don't share other students' personal information
4. **Backup**: Original simulated data is kept as backup
5. **Testing**: Test your API after updating data to ensure it still works

## 🔧 Troubleshooting

### Browser Issues
- Make sure Chrome is installed
- Update Chrome to latest version
- Check internet connection

### Login Problems
- Verify your IITM credentials
- Try logging in manually first
- Clear browser cache/cookies

### Access Denied
- Ensure you're enrolled in TDS course
- Check if you need to access content during specific hours
- Try different search terms

### Data Not Found
- Sites might use JavaScript heavily
- Content might be behind additional authentication
- Some content might be restricted

## 📊 Data Quality Check

After scraping, verify:
- ✅ At least 3 posts about GPT model selection
- ✅ At least 2 posts about GA4 scoring
- ✅ URLs are real and accessible
- ✅ Content is relevant to TDS course
- ✅ Timestamps are realistic
- ✅ API still responds correctly to test questions

## 🎉 Success Criteria

Your scraping is successful if:
1. You have real URLs from both sites
2. Content is relevant to TDS evaluation criteria
3. API continues to work with new data
4. You can answer the test question correctly
5. Links provided are accessible and relevant

---

**Remember**: The goal is to get authentic data that improves your Virtual TA's responses while maintaining the evaluation criteria compatibility! 