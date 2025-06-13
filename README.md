# TDS Virtual TA

A virtual Teaching Assistant for IIT Madras' Tools in Data Science course that automatically answers student questions based on course content and Discourse discussions.

## Features

- **API Endpoint**: Accepts POST requests with student questions and optional base64 image attachments
- **Intelligent Responses**: Provides answers with relevant links from course content and Discourse posts
- **Data Scraping**: Extracts data from TDS course content and Discourse posts
- **Fast Response**: Responds within 30 seconds
- **Deployment Ready**: Configured for easy deployment to various platforms

## API Usage

### Endpoint
```
POST https://your-app-url.com/api/
```

### Request Format
```json
{
  "question": "Your question here",
  "image": "base64_encoded_image_data (optional)"
}
```

### Response Format
```json
{
  "answer": "Detailed answer to the question",
  "links": [
    {
      "url": "https://relevant-link.com",
      "text": "Description of the link"
    }
  ]
}
```

### Example Usage
```bash
curl "https://your-app-url.com/api/" \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I use gpt-4o-mini or gpt-3.5-turbo?", "image": "base64_image_data"}'
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/tds-virtual-ta.git
cd tds-virtual-ta
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run data scraping (optional - pre-scraped data is included):
```bash
python scripts/scrape_data.py
```

5. Start the application:
```bash
python app.py
```

## Deployment

### Using Railway
1. Connect your GitHub repository to Railway
2. Deploy automatically

### Using Render
1. Connect your GitHub repository to Render
2. Use the provided `render.yaml` configuration

### Using Heroku
1. Install Heroku CLI
2. Run: `heroku create your-app-name`
3. Run: `git push heroku main`

## Project Structure

```
tds-virtual-ta/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version specification
├── Procfile             # Process configuration for deployment
├── render.yaml          # Render deployment configuration
├── .env.example         # Environment variables template
├── data/                # Scraped data storage
│   ├── course_content.json
│   └── discourse_posts.json
├── scripts/             # Utility scripts
│   ├── scrape_data.py   # Data scraping script
│   └── preprocess.py    # Data preprocessing
├── src/                 # Source code
│   ├── __init__.py
│   ├── api.py           # API handlers
│   ├── scraper.py       # Web scraping utilities
│   ├── processor.py     # Question processing
│   └── responder.py     # Response generation
└── tests/              # Test files
    ├── test_api.py
    └── test_scraper.py
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- IIT Madras Tools in Data Science course
- Course instructors and teaching assistants
- Student community on Discourse 