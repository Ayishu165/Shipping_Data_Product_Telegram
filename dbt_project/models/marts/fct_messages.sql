SELECT
    id AS message_id,
    channel,
    message_time,
    sender_id,
    COALESCE(message, '') AS message,
    downloaded_image,
    LENGTH(COALESCE(message, '')) AS message_length,
    downloaded_image IS NOT NULL AS has_image
FROM {{ ref('stg_telegram_messages') }}
