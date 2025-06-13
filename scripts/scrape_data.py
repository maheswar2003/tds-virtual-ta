#!/usr/bin/env python3
"""
Main data scraping script for TDS Virtual TA
This script scrapes data from TDS course content and Discourse posts
and can be run independently or with date range parameters.
"""

import sys
import os
import argparse
import logging
from datetime import datetime

# Add parent directory to path to import src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scraper import TDSScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function for scraping script"""
    parser = argparse.ArgumentParser(description='Scrape TDS course content and Discourse posts')
    parser.add_argument(
        '--start-date', 
        type=str, 
        default='2025-01-01',
        help='Start date for Discourse posts (YYYY-MM-DD format)'
    )
    parser.add_argument(
        '--end-date', 
        type=str, 
        default='2025-04-14',
        help='End date for Discourse posts (YYYY-MM-DD format)'
    )
    parser.add_argument(
        '--course-only',
        action='store_true',
        help='Only scrape course content, skip Discourse posts'
    )
    parser.add_argument(
        '--discourse-only',
        action='store_true',
        help='Only scrape Discourse posts, skip course content'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='data',
        help='Output directory for scraped data'
    )
    
    args = parser.parse_args()
    
    # Validate date format
    try:
        datetime.strptime(args.start_date, '%Y-%m-%d')
        datetime.strptime(args.end_date, '%Y-%m-%d')
    except ValueError:
        logger.error("Invalid date format. Use YYYY-MM-DD format.")
        return 1
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize scraper
    scraper = TDSScraper()
    
    course_data = []
    discourse_data = []
    
    try:
        # Scrape course content
        if not args.discourse_only:
            logger.info("Starting course content scraping...")
            course_data = scraper.scrape_course_content()
            logger.info(f"Scraped {len(course_data)} course content items")
        
        # Scrape discourse posts
        if not args.course_only:
            logger.info(f"Starting Discourse scraping from {args.start_date} to {args.end_date}...")
            discourse_data = scraper.scrape_discourse_posts(args.start_date, args.end_date)
            logger.info(f"Scraped {len(discourse_data)} Discourse posts")
        
        # Save scraped data
        logger.info(f"Saving data to {args.output_dir}/")
        scraper.save_scraped_data(course_data, discourse_data)
        
        # Print summary
        print("\n" + "="*50)
        print("SCRAPING COMPLETED SUCCESSFULLY")
        print("="*50)
        print(f"Course content items: {len(course_data)}")
        print(f"Discourse posts: {len(discourse_data)}")
        print(f"Data saved to: {args.output_dir}/")
        print("="*50)
        
        return 0
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 