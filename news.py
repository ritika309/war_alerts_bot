import requests
import hashlib
import json
import os
import time
import logging
from dotenv import load_dotenv

load_dotenv()

# ================= CONFIG =================

NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

CHECK_INTERVAL = 1200  # 20 minutes
SEEN_FILE = "seen_articles.json"
REQUEST_TIMEOUT = 15

# ===========================================

UAE_LOCATIONS = [
    "uae",
    "abu dhabi",
    "dubai",
    "sharjah",
    "ajman",
    "ras al khaimah",
    "fujairah",
    "umm al quwain"
]

ATTACK_KEYWORDS = [
    "missile", "airstrike", "drone", "rocket", "bombing",
    "explosion", "attack", "strike", "intercepted",
    "killed", "injured", "casualties", "fire",
    "explosives", "shot down"
]

# ================= LOGGING =================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ===========================================


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def fetch_news():
    url = "https://newsdata.io/api/1/news"

    params = {
        "apikey": NEWSDATA_API_KEY,
        "q": "UAE",
        "language": "en",
    }

    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"API request failed: {e}")
        return []

    data = response.json()

    if "results" not in data:
        logging.warning(f"Unexpected API response: {data}")
        return []

    return data["results"]


def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        r = requests.post(
            url,
            data={"chat_id": CHAT_ID, "text": message},
            timeout=REQUEST_TIMEOUT
        )
        r.raise_for_status()
        logging.info("Telegram alert sent successfully.")
    except Exception as e:
        logging.error(f"Telegram send failed: {e}")


def is_serious(article):
    title = (article.get("title") or "").lower()
    description = (article.get("description") or "").lower()
    content = title + " " + description

    location_present = any(loc in content for loc in UAE_LOCATIONS)
    attack_present = any(word in content for word in ATTACK_KEYWORDS)

    return location_present and attack_present


def main():
    logging.info("🚨 UAE Production Monitor Started")
    seen_articles = load_seen()

    while True:
        try:
            logging.info("Checking news...")
            articles = fetch_news()
            logging.info(f"Fetched {len(articles)} articles")

            for article in articles:
                link = article.get("link")
                if not link:
                    continue

                article_id = hashlib.md5(link.encode()).hexdigest()

                if article_id in seen_articles:
                    continue

                if not is_serious(article):
                    continue

                message = (
                    f"🚨 UAE ATTACK ALERT\n\n"
                    f"{article.get('title')}\n\n"
                    f"{link}"
                )

                send_alert(message)
                seen_articles.add(article_id)

            save_seen(seen_articles)

        except Exception as e:
            logging.error(f"Unexpected error: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()