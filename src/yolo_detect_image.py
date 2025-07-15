from ultralytics import YOLO
from pathlib import Path
import json

# Define paths
IMAGE_DIR = Path(r"D:/kaimtenx/project/week7/Shipping_Data_Product_Telegram/data/images")
OUTPUT_JSON = Path("data/yolo_image_detections.json")

# Load pre-trained YOLOv8 nano model
model = YOLO("yolov8n.pt")

def get_all_images(directory):
    """Scan for all .jpg and .png images in the directory"""
    if not directory.exists():
        print(f"❌ Error: Image directory {directory} does not exist.")
        return []
    images = list(directory.rglob("*.jpg")) + list(directory.rglob("*.png"))
    print(f"✅ Found {len(images)} images to process.")
    return images

def detect_objects_in_images(images):
    """Run YOLO detection on each image and collect results"""
    detection_results = []
    for img_path in images:
        print(f"🔍 Running detection on: {img_path.name}")
        try:
            result = model(img_path, verbose=False)[0]
            for box in result.boxes:
                detection_results.append({
                    "image_file": img_path.name,
                    "class_id": int(box.cls[0]),
                    "class_name": model.model.names[int(box.cls[0])],
                    "confidence": round(float(box.conf[0]), 4),
                    "bbox": [round(float(x), 2) for x in box.xyxy[0].tolist()]
                })
        except Exception as e:
            print(f"⚠️ Error processing {img_path.name}: {e}")
    return detection_results

def save_detections_to_json(detections, output_file):
    """Save detection results to JSON"""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(detections, f, indent=2)
    print(f"✅ Saved {len(detections)} detections to {output_file}")

if __name__ == "__main__":
    images = get_all_images(IMAGE_DIR)
    if images:
        detections = detect_objects_in_images(images)
        save_detections_to_json(detections, OUTPUT_JSON)
    else:
        print("⚠️ No images found. Nothing to detect.")

