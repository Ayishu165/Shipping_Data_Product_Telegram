import json, psycopg2, os
from dotenv import load_dotenv

load_dotenv()

DETECTIONS_JSON = "data/yolo_image_detections.json"

def connect_to_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def extract_message_id(filename):
    """
    Extracts message_id from filenames like 'lobelia4cosmetics_18431.jpg'
    Assumes message_id is always the number after the last underscore.
    """
    try:
        basename = os.path.splitext(filename)[0]
        parts = basename.split("_")
        return int(parts[-1])
    except (ValueError, IndexError):
        return None

def create_table(cursor):
    cursor.execute("""
    CREATE SCHEMA IF NOT EXISTS enriched;

    CREATE TABLE IF NOT EXISTS enriched.image_detections (
        id SERIAL PRIMARY KEY,
        message_id BIGINT NOT NULL,
        detected_object_class TEXT NOT NULL,
        confidence_score FLOAT NOT NULL,
        image_path TEXT NOT NULL,
        bbox JSONB NOT NULL,
        detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

def load_detections():
    if not os.path.exists(DETECTIONS_JSON):
        print(f"❌ Detection file {DETECTIONS_JSON} not found.")
        return

    with open(DETECTIONS_JSON, "r") as f:
        detections = json.load(f)

    conn = connect_to_db()
    cur = conn.cursor()
    create_table(cur)

    inserted = 0

    for det in detections:
        message_id = extract_message_id(det["image_file"])
        if message_id is None:
            print(f"⚠️ Skipping {det['image_file']} — No message_id found.")
            continue
        else:
            print(f"✅ Extracted message_id {message_id} from {det['image_file']}")

        cur.execute("""
            INSERT INTO enriched.image_detections 
            (message_id, detected_object_class, confidence_score, image_path, bbox)
            VALUES (%s, %s, %s, %s, %s);
        """, (
            message_id,
            det["class_name"],
            det["confidence"],
            det["image_file"],
            json.dumps(det["bbox"])
        ))

        inserted += 1

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Loaded {inserted} valid detections into enriched.image_detections.")

if __name__ == "__main__":
    load_detections()
