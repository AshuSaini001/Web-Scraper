# 🕷️ Web Scraper – Educational Demo

A lightweight, configurable web scraper built with **Flask**, **Requests**, and **BeautifulSoup**.  
This project demonstrates how to extract data from websites while staying under the radar — with built‑in stealth techniques, error handling, and a clean web interface.

**Live Demo:** [https://web-scraper-40e1.onrender.com](https://web-scraper-40e1.onrender.com)

---

## 📌 Features

- ✅ **Stealth scraping** – rotates User‑Agents and mimics human behavior
- ✅ **Resilient** – retries on failure, logs errors, handles timeouts
- ✅ **Configurable** – easily change the target URL in `scraper.py`
- ✅ **Live web interface** – trigger scraping and view results via `/scrape` and `/data`
- ✅ **Legal disclaimer** – clear warning about ethical use
- ✅ **Example sandbox** – includes a local test page (`sandbox.html`) for safe testing

---

## 🚀 Live Demo

| Endpoint | Description |
| :--- | :--- |
| `/` | Homepage with instructions and legal disclaimer |
| `/scrape` | Triggers the scraper (fetches and saves data) |
| `/data` | Displays the scraped results as JSON |

**Try it now:**

- Run scraper: [https://web-scraper-40e1.onrender.com/scrape](https://web-scraper-40e1.onrender.com/scrape)
- View data: [https://web-scraper-40e1.onrender.com/data](https://web-scraper-40e1.onrender.com/data)

---

## 🧪 How to Run Locally

### 1. Clone the repository

git clone https://github.com/your-username/web-scraper.git
cd web-scraper

### 2. Navigate to the scraper folder

cd scraper

### 3. Create and activate a virtual environment

python -m venv venv
venv\Scripts\activate
(for Windows)

### 4. Install dependencies

pip install -r requirements.txt

### 5. Run the Flask app

python app.py

🏠 Using the Example Sandbox (Optional)
The homepage/ folder contains a local test website called sandbox.html.
You can use this to test the scraper without hitting a live website — perfect for development and learning.

How to use it:
### 1. Serve the sandbox (in a separate terminal):

cd homepage
python -m http.server 8000

### 2. Update the target URL in scraper.py:

TARGET_URL = "http://localhost:8000/sandbox.html"

### 3. Update config.json to match the sandbox structure:

{
  "container": "div.job-listing",
  "title": "h2.title",
  "author": "p.company",
  "link": "a.apply-link"
}

### 4. Run the scraper as usual — it will extract data from your local sandbox.

💡 The sandbox simulates a real job board with 4 sample job listings. It's an excellent way to test your scraper without any legal or ethical concerns.

## 🔧 Changing the Target Website
You can scrape any public website by modifying scraper.py:

### 1. Open scraper.py

### 2. Change the TARGET_URL variable:

TARGET_URL = "https://example.com"

### 3. Update config.json to match the target's HTML structure:

    container: CSS selector for each item container (e.g., div.quote)

    title: CSS selector for the main text (e.g., span.text)

    author: CSS selector for the author/source (e.g., small.author)

    link: CSS selector for the URL (e.g., a[href*='/author/'])

## ⚠️ Important:

Always check the website's robots.txt and Terms of Service before scraping.

Do not scrape sites that explicitly prohibit it (e.g., LinkedIn, Indeed, Facebook).

This tool is for educational purposes only. You are solely responsible for how you use it.

---

## 🛡️ Legal Disclaimer
This project is for educational purposes only.
The author does not approve or encourage scraping websites that prohibit it.
Users are solely responsible for ensuring they comply with all applicable laws and terms of service.

---

## 🧰 Technology Stack
Backend: Flask (Python)

Scraping: Requests + BeautifulSoup (with fake-useragent for rotation)

Deployment: Render (free tier)

Version Control: Git + GitHub

---

## 📂 Project Structure
web-scraper/

├── scraper/

│   ├── app.py              # Flask web server

│   ├── scraper.py          # Core scraping logic

│   ├── config.json         # CSS selectors for parsing

│   ├── requirements.txt    # Python dependencies

│   └── listings.json       # Scraped data (generated at runtime)

├── homepage/

│   └── sandbox.html        # Local test website for scraping

├── README.md               # This file

└── DECISIONS.md            # Design document for assessment
