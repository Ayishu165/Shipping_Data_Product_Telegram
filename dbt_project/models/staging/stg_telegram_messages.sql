with raw as (

  select * from raw.telegram_messages

)

select
  id,
  channel,
  message,
  cast(date as timestamp) as message_time,
  case when downloaded_image is not null then true else false end as has_image,
  length(coalesce(message, '')) as message_length,
  downloaded_image

from raw
