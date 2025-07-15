-- ✅ Custom Test: Media posts (with downloaded_image) must not have empty messages
select *
from {{ ref('fct_messages') }}
where downloaded_image is not null
  and (message is null or message = '')
