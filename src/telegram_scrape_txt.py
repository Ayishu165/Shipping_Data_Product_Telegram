# ----------------------------------------
# scrape_text_only.py
# Task 1: Scrape Only Messages from All Channels
# ----------------------------------------

import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from telethon.sync import TelegramClient

# Load credentials from .env
load_dotenv()
API_ID= int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "telegram_session1")
# Define channels to scrape from
CHANNELS = [
    "https://t.me/CheMed123",
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma",
    "https://t.me/tenamereja"
]

# Output paths
today = datetime.now().strftime("%Y-%m-%d")
OUTPUT_DIR = Path(f"data/raw/telegram_messages/{today}")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Helper
def channel_name_from_url(url):
    return url.split("/")[-1]

# Main scraper
async def scrape_messages_only():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        for url in CHANNELS:
            channel = channel_name_from_url(url)
            messages = []

            print(f"🔍 Scraping messages from {channel}...")

            try:
                async for message in client.iter_messages(url, limit=25000):
                    msg_data = {
                        "id": message.id,
                        "date": str(message.date),
                        "message": message.message,
                        "sender_id": getattr(message.from_id, "user_id", None) if message.from_id else None
                    }
                    messages.append(msg_data)

                output_file = OUTPUT_DIR / f"{channel}.json"
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(messages, f, ensure_ascii=False, indent=2)

                print(f"✅ {len(messages)} messages saved to {output_file}")

            except Exception as e:
                print(f"❌ Error scraping {channel}: {e}")

# Run it
if __name__ == "__main__":
    import asyncio
    asyncio.run(scrape_messages_only())
