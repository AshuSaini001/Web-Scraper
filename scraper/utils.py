import asyncio
import random
import logging
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
ua = UserAgent()

def get_random_user_agent():
    return ua.random

async def random_delay(min_sec=2, max_sec=5):
    """Asynchronous delay using asyncio.sleep."""
    await asyncio.sleep(random.uniform(min_sec, max_sec))

def get_proxy():
    # For demo, return None (no proxy). Replace with a real proxy pool for production.
    return None

def log_error(msg):
    logger.error(msg)