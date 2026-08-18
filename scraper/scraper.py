import json
import asyncio
from playwright.async_api import async_playwright
from utils import get_random_user_agent, random_delay, log_error, logger

with open('config.json', 'r', encoding='utf-8') as f:
    SELECTORS = json.load(f)

async def scrape_page(page, url, retry_count=0):
    try:
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await page.evaluate("window.scrollBy(0, window.innerHeight / 2)")
        await random_delay(1, 2)
        await page.evaluate("window.scrollBy(0, window.innerHeight / 2)")

        await page.wait_for_selector(SELECTORS['jobCard'], timeout=10000)
        listings = await page.eval_on_selector_all(
            SELECTORS['jobCard'],
            """(cards, selectors) => {
                return cards.map(card => ({
                    title: card.querySelector(selectors.title)?.innerText?.trim() || '',
                    company: card.querySelector(selectors.company)?.innerText?.trim() || '',
                    link: card.querySelector(selectors.link)?.href || ''
                }));
            }""",
            SELECTORS
        )
        return listings
    except Exception as e:
        log_error(f"Error scraping {url}: {e}")
        if retry_count < 3:
            await random_delay(5, 15)
            return await scrape_page(page, url, retry_count + 1)
        else:
            raise

async def main():
    # Note: replace with your own sandbox URL
    TARGET_URL =  "http://localhost:8000/sandbox.html"
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )
        context = await browser.new_context(
            user_agent=get_random_user_agent(),
            viewport={'width': 1366, 'height': 768},
            locale='en-US',
            timezone_id='America/New_York'
        )
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        """)
        page = await context.new_page()
        try:
            listings = await scrape_page(page, TARGET_URL)
            logger.info(f"Scraped {len(listings)} listings")
            with open('listings.json', 'w') as f:
                json.dump(listings, f, indent=2)
        except Exception as e:
            log_error(f"Fatal error: {e}")
        finally:
            await browser.close()
if __name__ == '__main__':
    asyncio.run(main())
