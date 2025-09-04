# Drone & UAV News Dashboard

A simple, self-hostable Python app that continuously scrapes the web for news about drones, UAVs, and their startup ecosystem—plots them in a neat dashboard, and saves all crawled data with timestamps in a JSON file.

## Features

- Scrapes news headlines for 250 key drone/UAV/startup ecosystem keywords.
- Dashboard shows latest news, summaries, dates, and links.
- Refreshes automatically every 12 hours (no manual intervention).
- All crawled articles saved in `scraped_news.json` with timestamps.
- Each article is trimmed to 500 words max.
- Download all raw data from `/data` endpoint.
- Easy to run on any server, open in your browser.

## Setup

1. **Clone the repo:**
   ```sh
   git clone https://github.com/shiva16/drone-uav-news-dashboard.git
   cd drone-uav-news-dashboard
   ```

2. **Install dependencies:**
   ```sh
   pip install flask apscheduler beautifulsoup4 requests
   ```

3. **Run the app:**
   ```sh
   python app.py
   ```
   The dashboard will be live at `http://localhost:5000/` (or your server IP).

## Data Storage

- All scraped articles are stored in `scraped_news.json` with keyword, title, url, summary, and timestamp.

## Customization

- Edit `drone_uav_keywords.md` to add/remove keywords.
- Adjust refresh interval or display limits in `app.py`.

## License

MIT
