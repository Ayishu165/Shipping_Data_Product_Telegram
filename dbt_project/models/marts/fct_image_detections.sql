SELECT
  d.image_file,
  d.class_id AS detected_object_class,
  d.confidence AS confidence_score,
  m.id AS message_id
FROM {{ ref('stg_image_detections') }} d
LEFT JOIN {{ ref('stg_telegram_messages') }} m
  ON d.image_file = m.downloaded_image