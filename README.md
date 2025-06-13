# TDS Virtual TA

My Virtual Teaching Assistant project for IIT Madras Tools in Data Science course. This bot answers student questions using AI and scraped course content.

## What it does

- Takes student questions via API endpoint
- Uses OpenAI GPT to generate smart answers
- Searches through course materials and Discourse posts
- Returns answers with relevant links
- Can handle images too (optional)

## API Usage

**Endpoint:** `POST /api/`

**Send this:**
```json
{
  "question": "Should I use gpt-4o-mini or gpt-3.5-turbo?",
  "image": "base64_image_data (optional)"
}
```

**You get back:**
```json
{
  "answer": "You must use gpt-3.5-turbo-0125, even if the AI Proxy only supports gpt-4o-mini...",
  "links": [
    {
      "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939",
      "text": "Discussion: GA5 Model Question"
    }
  ]
}
```

**Test with curl:**
```bash
curl -X POST "https://your-app-url.com/api/" \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I use gpt-4o-mini or gpt-3.5-turbo?"}'
```

## How to run locally

1. **Clone this repo:**
```bash
git clone https://github.com/maheswar2003/tds-virtual-ta.git
cd tds-virtual-ta
```

2. **Install packages:**

For basic functionality (recommended for deployment):
```bash
pip install -r requirements.txt
```

For full features including image processing and semantic search:
```bash
pip install -r requirements-full.txt
```

3. **Set up environment:**
```bash
# Copy the example file
cp env.example .env

# Edit .env and add your OpenAI API key:
OPENAI_API_KEY=your_api_key_here
```

4. **Run the scraper (optional):**
```bash
python scripts/scrape_data.py
```

5. **Start the app:**
```bash
python app.py
```

App runs on `http://localhost:5000`

## Project Files

```
tds-virtual-ta/
├── app.py                    # Main Flask app
├── requirements.txt          # Python packages needed
├── .env.example             # Environment variables template
├── data/                    # Scraped course data
│   ├── course_content.json
│   └── discourse_posts.json
├── src/                     # Source code
│   ├── processor.py         # Question processing
│   ├── responder.py         # Answer generation
│   └── scraper.py          # Web scraping
├── scripts/
│   └── scrape_data.py      # Data scraping script (bonus marks!)
└── tests/                  # Some basic tests
```

## Deployment

I deployed mine on Railway - it's free and easy:

1. Push your code to GitHub (make sure .env is in .gitignore!)
2. Go to railway.app and connect your GitHub repo
3. Add environment variable: `OPENAI_API_KEY=your_key`
4. Deploy automatically

**Important for deployment:** The default `requirements.txt` uses lightweight dependencies to avoid size limits. The app will work with basic functionality and fallback to rule-based responses.

### Alternative platforms:
- **Render** (free tier available)
- **Heroku** (with lightweight buildpack)
- **Railway** (recommended for students)

### Deployment tips:
- Use the default `requirements.txt` (lightweight)
- Set `OPENAI_API_KEY` environment variable
- The app gracefully handles missing optional dependencies

## Features

✅ **Handles the test question correctly** - "You must use gpt-3.5-turbo-0125"  
✅ **Fast responses** (under 30 seconds)  
✅ **Relevant links** from course content and Discourse  
✅ **Image processing** (if you have the right packages)  
✅ **Data scraping script** for bonus marks  
✅ **Fallback mode** when OpenAI API isn't available  

## Technical Notes

- Uses OpenAI GPT-3.5-turbo for generating answers
- Sentence transformers for semantic search (optional)
- BLIP model for image processing (optional)
- Web scraping with BeautifulSoup and requests
- Flask with CORS for the API

If you don't have all the optional packages, the app still works with basic functionality.

## Assignment Requirements

This project meets all the requirements:

- ✅ API endpoint that accepts POST requests
- ✅ Returns JSON with answer and links
- ✅ Handles the specific test question about GPT models
- ✅ MIT license
- ✅ Public GitHub repository
- ✅ Deployed to public URL
- ✅ Data scraping script (bonus)

## License

MIT License - see LICENSE file

---

*Made for IIT Madras TDS course assignment by Maheswar* 