import os, json
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

# Load DB credentials
load_dotenv()
DB_NAME = os.getenv("DB_NAME", "telegramdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Absolute path to the scraped data folder
RAW_PATH = Path(r"D:\kaimtenx\project\week7\Shipping_Data_Product_Telegram\data\raw\telegram_messages\2025-07-12")

def load_json_to_postgres():
    print(f"🔍 Loading JSON files from: {RAW_PATH}")
    if not RAW_PATH.exists():
        print(f"❌ Path does not exist: {RAW_PATH}")
        return

    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS,
        host=DB_HOST, port=DB_PORT
    )
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

    inserted, skipped = 0, 0

    for file in RAW_PATH.glob("*.json"):
        print(f"📄 Processing file: {file.name}")
        # Safely extract channel name from file name
        channel = file.stem.split("_")[-1]

        with open(file, "r", encoding="utf-8") as f:
            try:
                messages = json.load(f)
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON in {file.name}: {e}")
                continue

            for msg in messages:
                if not msg.get("id") or not msg.get("date"):
                    skipped += 1
                    continue

                try:
                    cur.execute("""
                        INSERT INTO raw.telegram_messages 
                        (id, channel, date, message, sender_id, downloaded_image)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING;
                    """, (
                        msg["id"], channel, msg["date"],
                        msg.get("message", ""),
                        msg.get("from_id", {}).get("user_id") if isinstance(msg.get("from_id"), dict) else None,
                        msg.get("downloaded_image")
                    ))
                    inserted += 1
                except Exception as e:
                    print(f"❌ Error loading message {msg.get('id')}: {e}")
                    skipped += 1

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Done. Inserted: {inserted}, Skipped: {skipped}")

if __name__ == "__main__":
    load_json_to_postgres()
