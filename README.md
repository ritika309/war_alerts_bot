### 🚨 UAE Attack Monitor Bot

A production-ready Python bot that monitors real-time news for potential attack-related incidents in the UAE and sends instant alerts via Telegram.

This project runs automatically using GitHub Actions, requiring no server or paid hosting.

📌 Features

🔎 Fetches latest news via NewsData API

📍 Filters articles related to UAE locations

🚨 Detects serious attack-related keywords

📲 Sends real-time Telegram alerts

🔁 Prevents duplicate alerts using hashed article links

⏰ Runs automatically every hour (custom cron schedule)

💸 100% free deployment (GitHub Actions)

🧠 How It Works

GitHub Actions triggers the script on a schedule.

The bot fetches latest news articles.

It filters articles containing:

UAE-related locations

Attack-related keywords

If a matching article is new:

Telegram alert is sent

Article hash is saved to prevent duplicates

🛠 Tech Stack

Python 3.11

Requests

python-dotenv

Telegram Bot API

GitHub Actions (scheduler)

🔐 Environment Variables (Required)

Add these under:

Repository → Settings → Secrets and variables → Actions → Repository secrets

NEWSDATA_API_KEY
BOT_TOKEN
CHAT_ID
⚙️ Deployment

This project uses GitHub Actions for automatic execution.

Workflow file location:

.github/workflows/monitor.yml

Example cron schedule:

cron: "0 2-18 * * *"

Runs hourly between ~7:30 AM and ~11:30 PM IST.

📁 Project Structure
.
├── main.py
├── requirements.txt
├── seen_articles.json
└── .github/
    └── workflows/
        └── monitor.yml
🚀 Running Locally (Optional)

Clone repo

Create .env file:

NEWSDATA_API_KEY=your_key
BOT_TOKEN=your_token
CHAT_ID=your_chat_id

Install dependencies:

pip install -r requirements.txt

Run:

python main.py
📈 Future Improvements

Smarter NLP filtering

Multiple news source fallback

Better alert formatting (HTML / Markdown)

Database storage instead of JSON

Threat severity scoring

⚠️ Disclaimer

This bot relies on third-party news APIs and keyword detection.
It is intended for informational purposes only.

If you want, I can now:

Make a more portfolio-impressive version

Add badges (build status, Python version, etc.)

Or rewrite it in a more “startup-grade” style 😄
