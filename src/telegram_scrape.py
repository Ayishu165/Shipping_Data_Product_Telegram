# ----------------------------------------
# scraping.py
# Task 1: Telegram Scraping + Image Collection
# Author: 10 Academy - KAIM Week 7
# ----------------------------------------

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto

# ----------------------------------------
# 1. Load .env credentials
# ----------------------------------------
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

API_ID= int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "telegram_session")

# ----------------------------------------
# 2. Define channel lists
# ----------------------------------------
ALL_CHANNELS = [
    "https://t.me/CheMed123",
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma",
    "https://t.me/tenamereja"
]

IMAGE_CHANNELS = {
    "CheMed123",
    "lobelia4cosmetics"
}

# ----------------------------------------
# 3. Setup paths and logging
# ----------------------------------------
today = datetime.now().strftime("%Y-%m-%d")

RAW_DATA_DIR = Path(f"data/raw/telegram_messages/{today}")
IMAGE_DIR = Path("data/images")
LOG_FILE = Path("logs/scrape.log")

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ----------------------------------------
# 4. Utility functions
# ----------------------------------------
def sanitize_channel_name(url: str) -> str:
    return url.split("/")[-1]

def get_output_path(channel: str):
    return RAW_DATA_DIR / f"{channel}.json"

# ----------------------------------------
# 5. Main scraping logic
# ----------------------------------------
async def scrape_telegram():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        for url in ALL_CHANNELS:
            channel = sanitize_channel_name(url)
            message_count = 0
            image_count = 0
            output = []

            print(f"📡 Scraping channel: {channel}")
            logging.info(f"Started scraping {channel}")

            try:
                async for message in client.iter_messages(url, limit=25000):
                    msg_data = message.to_dict()

                    # Download image only from selected channels
                    if message.media and isinstance(message.media, MessageMediaPhoto) and channel in IMAGE_CHANNELS:
                        image_name = f"{channel}_{message.id}.jpg"
                        image_path = IMAGE_DIR / image_name
                        await client.download_media(message.media, file=image_path)
                        msg_data['downloaded_image'] = str(image_path)
                        image_count += 1

                    output.append(msg_data)
                    message_count += 1

                # Save messages as JSON
                with open(get_output_path(channel), "w", encoding="utf-8") as f:
                    json.dump(output, f, ensure_ascii=False, indent=2)

                print(f"✅ Done: {channel} | Messages: {message_count} | Images: {image_count}")
                logging.info(f"Finished scraping {channel} - Messages: {message_count}, Images: {image_count}")

            except Exception as e:
                logging.error(f"❌ Error scraping {channel}: {e}")
                print(f"❌ Failed to scrape {channel}. Check logs.")

# ----------------------------------------
# 6. Entry Point
# ----------------------------------------
if __name__ == "__main__":
    import asyncio
    asyncio.run(scrape_telegram())
