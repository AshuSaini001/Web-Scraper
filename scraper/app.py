from flask import Flask, jsonify
import asyncio
from scraper import main

app = Flask(__name__)

@app.route('/')
def home():
    return "Scraper is live. Trigger /scrape to run."

@app.route('/scrape')
def run_scrape():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
        return jsonify({"status": "scraping completed"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)