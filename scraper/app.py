from flask import Flask, jsonify, render_template_string
import os
import json
from scraper import main

app = Flask(__name__)

# ===== HOME PAGE =====
@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Web Scraper – Instructions</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f7fafc;
            padding: 40px 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .card {
            background: white;
            max-width: 750px;
            padding: 45px 50px;
            border-radius: 20px;
            box-shadow: 0 8px 40px rgba(0,0,0,0.08);
        }
        h1 {
            font-size: 2.2rem;
            color: #1a202c;
            margin-bottom: 4px;
        }
        .sub {
            color: #4a5568;
            font-size: 1.05rem;
            margin-bottom: 28px;
            border-bottom: 1px solid #edf2f7;
            padding-bottom: 16px;
        }
        .sub a {
            color: #6366f1;
            text-decoration: none;
        }
        .sub a:hover {
            text-decoration: underline;
        }
        h3 {
            color: #2d3748;
            font-size: 1.1rem;
            margin-bottom: 12px;
        }
        .endpoint {
            background: #edf2f7;
            padding: 14px 20px;
            border-radius: 10px;
            margin: 12px 0;
            font-family: 'Courier New', monospace;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }
        .endpoint .label {
            background: #6366f1;
            color: white;
            padding: 2px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        .endpoint a {
            color: #6366f1;
            text-decoration: none;
            font-weight: 500;
        }
        .endpoint a:hover {
            text-decoration: underline;
        }
        .btn-group {
            margin: 24px 0 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }
        .btn {
            display: inline-block;
            padding: 10px 28px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
            transition: 0.2s;
        }
        .btn-primary {
            background: #6366f1;
            color: white;
        }
        .btn-primary:hover {
            background: #4f46e5;
            transform: translateY(-2px);
        }
        .btn-success {
            background: #48bb78;
            color: white;
        }
        .btn-success:hover {
            background: #38a169;
            transform: translateY(-2px);
        }
        .btn-outline {
            background: transparent;
            color: #4a5568;
            border: 2px solid #e2e8f0;
        }
        .btn-outline:hover {
            border-color: #6366f1;
            color: #6366f1;
        }
        .example {
            background: #f7fafc;
            padding: 14px 18px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 0.95rem;
            color: #2d3748;
            margin: 12px 0 16px;
            border-left: 4px solid #6366f1;
        }
        .example code {
            background: #edf2f7;
            padding: 2px 8px;
            border-radius: 4px;
        }
        .disclaimer {
            background: #fefcbf;
            border: 1px solid #f6e05e;
            border-radius: 12px;
            padding: 18px 22px;
            margin: 24px 0 12px;
        }
        .disclaimer h3 {
            color: #744210;
            font-size: 1rem;
            margin-bottom: 6px;
        }
        .disclaimer p {
            color: #5a4516;
            font-size: 0.95rem;
            line-height: 1.6;
        }
        .disclaimer strong {
            color: #975a16;
        }
        .disclaimer a {
            color: #2b6cb0;
            text-decoration: none;
            font-weight: 600;
        }
        .disclaimer a:hover {
            text-decoration: underline;
        }
        .footer {
            margin-top: 28px;
            font-size: 0.85rem;
            color: #a0aec0;
            border-top: 1px solid #edf2f7;
            padding-top: 20px;
            text-align: center;
        }
        .footer a {
            color: #6366f1;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        @media (max-width: 600px) {
            .card { padding: 25px 20px; }
            h1 { font-size: 1.6rem; }
            .endpoint { font-size: 0.9rem; padding: 12px 16px; }
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🕷️ Web Scraper</h1>
        <p class="sub">
            Live demo – extracts quotes from 
            <a href="https://quotes.toscrape.com" target="_blank">quotes.toscrape.com</a>
        </p>

        <h3>📌 How to use</h3>
        <p style="color: #4a5568; margin-bottom: 8px;">
            Add one of these to the end of the website URL:
        </p>

        <div class="endpoint">
            <span class="label">GET</span>
            <a href="/scrape"><strong>/scrape</strong></a>
            <span style="color: #718096; font-weight: 400; font-family: 'Segoe UI', sans-serif; font-size: 0.9rem;">
                — Run the scraper (fetch and save data)
            </span>
        </div>

        <div class="endpoint">
            <span class="label">GET</span>
            <a href="/data"><strong>/data</strong></a>
            <span style="color: #718096; font-weight: 400; font-family: 'Segoe UI', sans-serif; font-size: 0.9rem;">
                — View the scraped results
            </span>
        </div>

        <div class="example">
            💡 <strong>Example:</strong><br />
            <code>{{ request.host_url }}scrape</code> → triggers scraping<br />
            <code>{{ request.host_url }}data</code> → shows the quotes
        </div>

        <div class="btn-group">
            <a href="/scrape" class="btn btn-primary">▶️ Run Scraper</a>
            <a href="/data" class="btn btn-success">📖 View Data</a>
            <a href="https://github.com/your-username/web-scraper" target="_blank" class="btn btn-outline">📦 GitHub Repo</a>
        </div>

        <!-- ===== DISCLAIMER ===== -->
        <div class="disclaimer">
            <h3>⚠️ Legal &amp; Ethical Disclaimer</h3>
            <p>
                <strong>This scraper is for educational purposes only.</strong><br /><br />
                The code is designed to be configurable — you can change the target website by editing 
                <code>scraper.py</code> and setting a new <code>TARGET_URL</code>.
                <br /><br />
                However, <strong>scraping websites without permission may violate their Terms of Service</strong> 
                and could be illegal in some jurisdictions. 
                <strong>I do not approve or encourage</strong> using this tool on any website that prohibits scraping.
                <br /><br />
                If you choose to modify and use this code, you do so <strong>at your own risk</strong>. 
                Always check the website's <code>robots.txt</code> and Terms of Service first.
                <br /><br />
                📥 <strong>To change the target:</strong> Download the repo from 
                <a href="https://github.com/your-username/web-scraper" target="_blank">GitHub</a>, 
                open <code>scraper/scraper.py</code>, and update the <code>TARGET_URL</code> variable.
            </p>
        </div>

        <div class="footer">
            Data from <a href="https://quotes.toscrape.com" target="_blank">quotes.toscrape.com</a> · 
            Powered by Flask · 
            <a href="https://github.com/your-username/web-scraper" target="_blank">View on GitHub</a>
        </div>
    </div>
</body>
</html>
    """)

# ===== TRIGGER SCRAPER =====
@app.route('/scrape')
def run_scrape():
    try:
        main()
        return jsonify({"status": "scraping completed", "message": "Data saved. Visit /data to view."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ===== VIEW DATA =====
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

# ===== START APP =====
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
