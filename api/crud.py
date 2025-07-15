from sqlalchemy.orm import Session
from sqlalchemy import text  # ✅ NEW

# 1. Top products
def get_top_products(db: Session, limit: int):
    query = text("""
        SELECT LOWER(message) AS product, COUNT(*) as count
        FROM raw.telegram_messages_analytics.fct_messages
        GROUP BY LOWER(message)
        ORDER BY count DESC
        LIMIT :limit
    """)
    return db.execute(query, {"limit": limit}).fetchall()

# 2. Channel activity
def get_channel_activity(db: Session, channel: str):
    query = text("""
        SELECT DATE(message_time) AS date, COUNT(*) AS message_count
        FROM raw.telegram_messages.stg_telegram_messages
        WHERE channel = :channel
        GROUP BY date
        ORDER BY date
    """)
    return db.execute(query, {"channel": channel}).fetchall()

# 3. Search messages
def search_messages(db: Session, query: str):
    query_text = text("""
        SELECT message, message_time AS date, channel
        FROM raw.telegram_messages_analytics.fct_messages
        WHERE message ILIKE :search
        ORDER BY message_time DESC
        LIMIT 20
    """)
    return db.execute(query_text, {"search": f"%{query}%"}).fetchall()
