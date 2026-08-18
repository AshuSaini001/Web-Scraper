from flask import Flask, jsonify
import os
import json
from scraper import main

app = Flask(__name__)

@app.route('/')
def home():
    return "Scraper is live. Trigger /scrape to run. Visit /data to see scraped results."

@app.route('/scrape')
def run_scrape():
    try:
        main()
        return jsonify({"status": "scraping completed"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/data')
def get_data():
    try:
        with open('listings.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "No data found. Run /scrape first."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
