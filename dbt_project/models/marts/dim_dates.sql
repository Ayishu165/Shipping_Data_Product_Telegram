SELECT DISTINCT
    message_time::date AS date,
    EXTRACT(DAY FROM message_time) AS day,
    EXTRACT(MONTH FROM message_time) AS month,
    EXTRACT(YEAR FROM message_time) AS year
FROM {{ ref('stg_telegram_messages') }}
