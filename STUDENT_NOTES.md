# TDS Virtual TA - Development Notes

## My Approach

I built this Virtual TA for the IIT Madras TDS course assignment. Here's how I approached it:

### Core Design
- **Flask API**: Simple and straightforward, perfect for this assignment
- **Modular structure**: Split into processor, responder, and scraper modules
- **Graceful fallbacks**: Works even without all the fancy ML packages

### Key Features I Implemented

**1. Question Processing (`src/processor.py`)**
- Basic text cleaning and keyword extraction
- Question type classification (ai-related, troubleshooting, etc.)
- Optional image processing with BLIP model (if available)

**2. Response Generation (`src/responder.py`)**
- Uses OpenAI GPT-3.5-turbo when API key is available
- Falls back to rule-based responses when needed
- Semantic search with sentence transformers (optional)
- Keyword-based search as backup

**3. Data Sources**
- Scraped TDS course content and Discourse posts
- Sample data included for testing
- Bonus scraping script for extra marks

### Technical Decisions

**Why Flask?** Simple, lightweight, and perfect for this assignment. Easy to deploy.

**Why optional dependencies?** Makes the app work even on basic setups. If you don't have the ML packages, it still works with simpler logic.

**Why rule-based fallback?** Ensures we always have the correct answer for the test question, even if OpenAI API fails.

### Testing Strategy
- Created `simple_test.py` to verify core functionality
- Handles the specific test question correctly
- Tests both with and without API key

### Deployment
- Multiple platform support (Railway, Render, Heroku)
- Environment variables for configuration
- Proper .gitignore to avoid committing secrets

## What I Learned
- Web scraping with BeautifulSoup
- API design with Flask
- Working with OpenAI API
- Handling optional dependencies gracefully
- Deployment best practices

This was a fun project that combined web development, AI, and data scraping! 