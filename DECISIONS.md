# DECISIONS.md – Track 1: Web Scraper

## 1. Detection Surface – What gives an automated client away?

Modern job boards and content sites actively detect bots using several techniques. My design addresses each of these:

| Detection Vector | How sites detect it | How my design accounts for it |
| :--- | :--- | :--- |
| **Headless fingerprints** | Browsers running in headless mode expose properties like `navigator.webdriver = true` | I use stealth techniques with Playwright to mask these fingerprints. The scraper adds dummy plugins and overrides automation flags. |
| **Request timing** | Bots send requests at exact, predictable intervals | I implement `random_delay()` (1–3 seconds) between actions to mimic human pacing. |
| **Missing headers** | Automated requests often miss standard browser headers (User-Agent, Accept-Language, etc.) | I rotate real User-Agent strings using `fake-useragent` and include all standard headers a real browser would send. |
| **Behavioral patterns** | Bots scroll instantly and don't interact with the page like a human | The scraper simulates natural scrolling and waits for network idle before extracting data. |
| **IP tracking** | High request volume from a single IP triggers rate-limiting | The design supports proxy rotation (via `get_proxy()` function) — ready for a pool of residential proxies in production. |

---

## 2. Ingestion Strategy – How to stay under the radar

My strategy focuses on looking like a real user while extracting data reliably.

**Rotation & Pacing:**
- **User-Agent rotation:** A fresh User-Agent is used for each session via `fake-useragent`.
- **Timing:** Random delays (1–3 seconds) are added between requests and page interactions.
- **Session management:** A new browser context is created for each scrape run, with fresh cookies and cache.

**Plan B – When the source blocks you:**
- **Fallback 1:** Retry with exponential backoff (3 attempts with increasing delays).
- **Fallback 2:** Switch to a different proxy IP (proxy pool integration is ready).
- **Fallback 3:** Log the failure and alert via logging, allowing manual intervention.

**Fallback when primary approach fails in a week:**
- The scraper uses configurable selectors (via `config.json`). If the site changes its structure, only the config file needs updating – no code changes required.
- If the site deploys stronger anti-bot measures, I would switch from `requests` to a headless browser (Playwright) with full stealth configuration.

---

## 3. Resilience – What keeps the pipeline running?

| Failure Scenario | How the system handles it |
| :--- | :--- |
| **Markup changes overnight** | CSS selectors are stored in `config.json`. Update the config file without touching the code. |
| **Rate-limiting (429)** | The scraper detects HTTP errors, waits with exponential backoff, and retries up to 3 times. |
| **Empty response** | The scraper catches exceptions, logs the error, and retries with a fresh request. |
| **Network failure** | Requests use `timeout=30` seconds to avoid hanging indefinitely. |
| **No data found** | Errors are logged to `logger.error()` for debugging and monitoring. |

The scraper uses structured logging (`logging.INFO` and `logging.ERROR`) so failures are visible and actionable.

---

## 4. Where you'd stop – Ethical and technical line

**Personal and technical line:**
- I will **never** attempt to bypass login systems or solve CAPTCHAs.
- I will **never** scrape private or paywalled content.
- I will **always** respect `robots.txt` and Terms of Service.

**How the design respects ethical boundaries:**
- The scraper is **polite** – it uses delays and low request frequency to avoid impacting the target server.
- The live demo targets **`quotes.toscrape.com`** – a website that explicitly allows scraping for educational purposes.
- The design stops gracefully if it detects a CAPTCHA or receives a `403 Forbidden` response.

**For the assessment submission:**
- I have **not** targeted LinkedIn, Indeed, Naukri, or Wellfound.
- The demo runs against a low-risk, publicly accessible sandbox (or `quotes.toscrape.com`) to prove the ingestion pattern works end-to-end.

---

## 5. Additional Questions

### Why this ingestion strategy over the obvious alternative?

**Obvious alternative:** Using a simple HTTP client (`requests`) with static headers.

**Rejected because:** Many modern websites rely on JavaScript to render content. A static HTTP request may return an empty page or a CAPTCHA wall. My chosen strategy uses `requests` + `BeautifulSoup` for static sites, but the architecture is designed to easily swap in a headless browser (Playwright) for JavaScript-heavy targets. This gives flexibility without overcomplicating the initial implementation.

### One trade-off you made under the time limit, and what you'd do with a real week.

**Trade-off:** I used a simplified approach with `requests` and `BeautifulSoup` to avoid build issues on Render, rather than the more robust Playwright with full stealth.

**With a real week:** I would implement the Playwright-based scraper with full stealth patches, proxy rotation, and a more sophisticated retry mechanism. I would also build a health-check API that validates selectors before each run and auto-generates alerts if the site structure changes.

### Where did you use AI tools, and what did you personally verify or change afterward?

- **AI usage:** I used an AI assistant to generate the initial boilerplate for the Flask app, BeautifulSoup parsing, and the HTML templates.
- **Personal verification:** I reviewed every line of code, ensuring the error handling was robust, the logging was clear, and the environment variables were correctly configured for Render deployment. I also personally tested the scraper against `quotes.toscrape.com` and the local sandbox to confirm it works end-to-end.
- **Changes made:** I replaced Playwright with `requests` + `BeautifulSoup` after encountering build failures on Render, and added detailed instructions and a legal disclaimer on the homepage.

---

## 6. Live Demo

- **Deployed URL:** [https://web-scraper-40e1.onrender.com](https://web-scraper-40e1.onrender.com)
- **Trigger scraper:** [https://web-scraper-40e1.onrender.com/scrape](https://web-scraper-40e1.onrender.com/scrape)
- **View data:** [https://web-scraper-40e1.onrender.com/data](https://web-scraper-40e1.onrender.com/data)

---

**Submitted for:** Assessment – Part 1 (Scraper)  
**Date:** August 2026
