WITH base AS (
    SELECT 
        id,
        channel,
        CAST(date AS TIMESTAMP) AS message_time,
        message,
        sender_id,
        downloaded_image
    FROM raw.telegram_messages
)

SELECT * FROM base
