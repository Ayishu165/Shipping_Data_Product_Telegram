select
  id as message_id,
  channel,
  message,
  message_time,
  message_length,
  has_image,
  downloaded_image
from {{ ref('stg_telegram_messages') }}
