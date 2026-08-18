import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import logging
import time
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ua = UserAgent()

def random_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))

def scrape_listings(url):
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    try:
        logger.info(f"Fetching {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        random_delay()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')
        
        listings = []
        for quote in quotes:
            title = quote.find('span', class_='text')
            author = quote.find('small', class_='author')
            link = quote.find('a', href=True)
            
            if title and author:
                listings.append({
                    'title': title.text.strip(),
                    'company': author.text.strip(),
                    'link': link['href'] if link else ''
                })
        
        logger.info(f"Scraped {len(listings)} listings")
        return listings
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        raise
    except Exception as e:
        logger.error(f"Parsing error: {e}")
        raise

def main():
    TARGET_URL = "https://quotes.toscrape.com"
    try:
        listings = scrape_listings(TARGET_URL)
        with open('listings.json', 'w') as f:
            json.dump(listings, f, indent=2)
        return listings
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise

if __name__ == '__main__':
    main()
