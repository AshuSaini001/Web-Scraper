from flask import Flask, jsonify
from scraper import main

app = Flask(__name__)

@app.route('/')
def home():
    return "Scraper is live. Trigger /scrape to run."

@app.route('/scrape')
def run_scrape():
    try:
        main()
        return jsonify({"status": "scraping completed"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
