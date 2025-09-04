import os
import json
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

KEYWORDS_FILE = "drone_uav_keywords.md"
DATA_FILE = "scraped_news.json"
MAX_ARTICLE_WORDS = 500
MAX_HEADLINES = 100  # Display limit for dashboard

app = Flask(__name__)

def load_keywords():
    with open(KEYWORDS_FILE, "r") as f:
        keywords = [line.strip() for line in f if line.strip() and not line[0].isdigit()]
    return keywords

def scrape_news():
    keywords = load_keywords()
    all_articles = []
    for kw in keywords:
        url = f"https://news.google.com/search?q={kw.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
        try:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            headlines = soup.select("article h3 a")
            for h in headlines:
                link = "https://news.google.com" + h["href"][1:] if h["href"].startswith(".") else h["href"]
                title = h.get_text(strip=True)
                article_data = fetch_article(link)
                all_articles.append({
                    "keyword": kw,
                    "title": title,
                    "url": link,
                    "date": datetime.utcnow().isoformat(),
                    "summary": article_data[:MAX_ARTICLE_WORDS]
                })
        except Exception as e:
            print(f"Error for keyword '{kw}': {e}")
    save_articles(all_articles)

def fetch_article(url):
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)
        words = text.split()
        return " ".join(words[:MAX_ARTICLE_WORDS])
    except Exception:
        return ""

def save_articles(articles):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            existing = json.load(f)
    else:
        existing = []
    existing.extend(articles)
    with open(DATA_FILE, "w") as f:
        json.dump(existing, f, indent=2)

def get_recent_articles():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        articles = json.load(f)
    articles = sorted(articles, key=lambda x: x["date"], reverse=True)[:MAX_HEADLINES]
    return articles

@app.route("/")
def dashboard():
    articles = get_recent_articles()
    return render_template("dashboard.html", articles=articles)

@app.route("/data")
def data():
    return send_from_directory(".", DATA_FILE)

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_news, "interval", hours=12)
    scheduler.start()
    app.run(host="0.0.0.0", port=5000)