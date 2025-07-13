import os, json
import psycopg2
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load DB credentials
load_dotenv()
DB_NAME = os.getenv("DB_NAME", "telegramdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

RAW_PATH = Path("data/raw/telegram_messages") / datetime.now().strftime("%Y-%m-%d")

def load_json_to_postgres():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS raw.telegram_messages (
        id BIGINT PRIMARY KEY,
        channel TEXT,
        date TIMESTAMP,
        message TEXT,
        sender_id BIGINT,
        downloaded_image TEXT
    );
    """)

    for file in RAW_PATH.glob("*.json"):
        channel = file.stem
        with open(file, "r", encoding="utf-8") as f:
            messages = json.load(f)
            for msg in messages:
                if not msg.get("id") or not msg.get("date"):
                    continue
                try:
                    cur.execute("""
                        INSERT INTO raw.telegram_messages (id, channel, date, message, sender_id, downloaded_image)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING;
                    """, (
                        msg["id"], channel, msg["date"],
                        msg.get("message", ""),
                        msg.get("from_id", {}).get("user_id") if isinstance(msg.get("from_id"), dict) else None,
                        msg.get("downloaded_image")
                    ))
                except Exception as e:
                    print(f"❌ Error loading message {msg['id']}: {e}")
    conn.commit()
    cur.close()
    conn.close()
    print("✅ All messages loaded into raw.telegram_messages")

if __name__ == "__main__":
    load_json_to_postgres()
