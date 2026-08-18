from flask import Flask, jsonify, render_template_string
import os
import json
from scraper import main

app = Flask(__name__)

# ===== HTML TEMPLATE for displaying data =====
DATA_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Scraped Quotes</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f4f8;
            padding: 40px 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        h1 {
            font-size: 2.2rem;
            color: #1a202c;
            margin-bottom: 8px;
        }
        .subtitle {
            color: #4a5568;
            margin-bottom: 30px;
            font-size: 1rem;
        }
        .stats {
            background: white;
            padding: 16px 24px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }
        .stats .count {
            font-weight: 600;
            color: #2d3748;
        }
        .stats .badge {
            background: #48bb78;
            color: white;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
        }
        .quote-card {
            background: white;
            border-radius: 12px;
            padding: 24px 28px;
            margin-bottom: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border-left: 5px solid #6366f1;
            transition: transform 0.15s;
        }
        .quote-card:hover {
            transform: translateX(4px);
        }
        .quote-card .text {
            font-size: 1.2rem;
            line-height: 1.6;
            color: #2d3748;
            margin-bottom: 8px;
            font-style: italic;
        }
        .quote-card .author {
            font-weight: 600;
            color: #4a5568;
            font-size: 0.95rem;
        }
        .quote-card .link {
            color: #6366f1;
            font-size: 0.85rem;
            text-decoration: none;
            margin-left: 12px;
        }
        .quote-card .link:hover {
            text-decoration: underline;
        }
        .empty-message {
            background: #fefcbf;
            border: 1px solid #f6e05e;
            border-radius: 12px;
            padding: 30px;
            text-align: center;
        }
        .empty-message h2 {
            color: #744210;
            margin-bottom: 12px;
        }
        .empty-message p {
            color: #5a4516;
            font-size: 1.05rem;
        }
        .empty-message code {
            background: #edf2f7;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 1.1rem;
            color: #2b6cb0;
        }
        .instructions {
            background: #ebf8ff;
            border: 1px solid #bee3f8;
            border-radius: 12px;
            padding: 20px 24px;
            margin-top: 30px;
        }
        .instructions h3 {
            color: #2b6cb0;
            margin-bottom: 8px;
        }
        .instructions ul {
            padding-left: 24px;
            color: #2c5282;
        }
        .instructions li {
            margin-bottom: 4px;
        }
        .footer {
            margin-top: 40px;
            font-size: 0.85rem;
            color: #a0aec0;
            text-align: center;
        }
        .btn {
            display: inline-block;
            background: #6366f1;
            color: white;
            padding: 8px 20px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.9rem;
        }
        .btn:hover {
            background: #4f46e5;
        }
        @media (max-width: 600px) {
            .quote-card .text { font-size: 1rem; }
            .stats { flex-direction: column; align-items: flex-start; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Scraped Quotes</h1>
        <p class="subtitle">Data extracted from <a href="https://quotes.toscrape.com" target="_blank">quotes.toscrape.com</a></p>

        {% if data %}
            <div class="stats">
                <span class="count">📖 {{ data|length }} quotes loaded</span>
                <span class="badge">✅ Live data</span>
                <a href="/scrape" class="btn" style="background:#48bb78;">🔄 Re-scrape</a>
            </div>

            {% for item in data %}
            <div class="quote-card">
                <div class="text">“{{ item.title }}”</div>
                <div class="author">
                    — {{ item.company }}
                    {% if item.link %}
                    <a href="https://quotes.toscrape.com{{ item.link }}" class="link" target="_blank">🔗 author</a>
                    {% endif %}
                </div>
            </div>
            {% endfor %}

        {% else %}
            <div class="empty-message">
                <h2>⚠️ No data found</h2>
                <p>You haven't scraped any quotes yet.</p>
                <p style="margin-top: 12px;">
                    👉 Visit <code>/scrape</code> to fetch the latest quotes.
                </p>
                <p style="margin-top: 8px;">
                    <a href="/scrape" class="btn">🚀 Run Scraper Now</a>
                </p>
            </div>
        {% endif %}

        <!-- Instructions -->
        <div class="instructions">
            <h3>📌 How to trigger the scraper</h3>
            <ul>
                <li>Add <strong><code>/scrape</code></strong> to the end of this website’s URL.</li>
                <li>Example: <code>{{ base_url }}/scrape</code></li>
                <li>After scraping, come back to <code>{{ base_url }}/data</code> to see the results.</li>
                <li>Or simply click the <strong>"Run Scraper Now"</strong> button above.</li>
            </ul>
        </div>

        <div class="footer">
            Powered by Flask · Data from quotes.toscrape.com
        </div>
    </div>
</body>
</html>
"""

# ===== HOME PAGE =====
@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Web Scraper</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; max-width: 700px; margin: 80px auto; padding: 0 20px; background: #f7fafc; }
        .card { background: white; padding: 40px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }
        h1 { color: #1a202c; margin-bottom: 8px; }
        .sub { color: #4a5568; margin-bottom: 24px; }
        .endpoint { background: #edf2f7; padding: 12px 18px; border-radius: 8px; margin: 12px 0; font-family: monospace; font-size: 1.1rem; }
        .endpoint a { color: #6366f1; text-decoration: none; }
        .endpoint a:hover { text-decoration: underline; }
        .btn { display: inline-block; background: #6366f1; color: white; padding: 10px 28px; border-radius: 30px; text-decoration: none; font-weight: 500; margin-top: 12px; }
        .btn:hover { background: #4f46e5; }
        .footer { margin-top: 30px; color: #a0aec0; font-size: 0.9rem; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🕷️ Web Scraper</h1>
        <p class="sub">Live demo — extracts quotes from <a href="https://quotes.toscrape.com" target="_blank">quotes.toscrape.com</a></p>

        <h3>🚀 Available endpoints</h3>
        <div class="endpoint">
            🔹 <a href="/scrape">/scrape</a> — Trigger the scraper (fetch & save quotes)
        </div>
        <div class="endpoint">
            🔹 <a href="/data">/data</a> — View the scraped results (nice HTML page)
        </div>

        <div style="margin-top: 20px;">
            <a href="/scrape" class="btn">▶️ Run Scraper</a>
            <a href="/data" class="btn" style="background:#48bb78; margin-left: 10px;">📖 View Data</a>
        </div>

        <div class="footer">
            <p>💡 <strong>Tip:</strong> Visit <code>/scrape</code> first, then <code>/data</code> to see the results.</p>
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

# ===== VIEW DATA (beautiful HTML) =====
@app.route('/data')
def get_data():
    try:
        with open('listings.json', 'r') as f:
            data = json.load(f)
      
        return render_template_string(DATA_TEMPLATE, data=data, base_url=request.host_url.rstrip('/'))
    except FileNotFoundError:
        return render_template_string(DATA_TEMPLATE, data=None, base_url=request.host_url.rstrip('/'))
    except Exception as e:
        return f"<h3>Error loading data</h3><p>{e}</p>"

# ===== START APP =====
if __name__ == '__main__':
    import os
    from flask import request
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
