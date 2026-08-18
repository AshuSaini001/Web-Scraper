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

```bash
git clone https://github.com/your-username/web-scraper.git
cd web-scraper

2. Navigate to the scraper folder
cd scraper

3. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate
(for Windows)

4. Install dependencies
pip install -r requirements.txt

5. Run the Flask app
python app.py
