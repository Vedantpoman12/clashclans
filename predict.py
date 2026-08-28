import sys
import os
import glob
from ultralytics import YOLO

def run_prediction(image_path=None, conf_threshold=0.25):
    # Locate the best weights
    weights_path = "runs/detect/clash_detector/weights/best.pt"
    if not os.path.exists(weights_path):
        weights_path = "runs/detect/clash_detector/weights/last.pt"
    
    if not os.path.exists(weights_path):
        print(f"Error: Model weights not found at '{weights_path}'. Ensure training is complete first.")
        return

    print(f"Loading model weights: {weights_path}")
    model = YOLO(weights_path)

    # Determine image to predict
    if not image_path:
        # Default sample image from test set
        sample_imgs = glob.glob("clash home manage - dead base detection.v1-mr-bob---dead-locater.yolov8/test/images/*.jpg")
        if not sample_imgs:
            sample_imgs = glob.glob("clash home manage - dead base detection.v1-mr-bob---dead-locater.yolov8/valid/images/*.jpg")
        
        if sample_imgs:
            image_path = sample_imgs[0]
            print(f"No image supplied. Using sample test image: {image_path}")
        else:
            print("No test images found. Please provide an image path: python predict.py <path_to_image>")
            return

    if not os.path.exists(image_path):
        print(f"Error: Image '{image_path}' does not exist.")
        return

    # Run YOLO prediction
    print(f"Running detection on '{image_path}' with confidence threshold {conf_threshold}...")
    results = model.predict(
        source=image_path,
        conf=conf_threshold,
        save=True,
        project="runs/detect",
        name="predictions",
        exist_ok=True
    )

    print("\n" + "="*50)
    print("DETECTION SUMMARY:")
    print("="*50)
    for r in results:
        boxes = r.boxes
        if len(boxes) == 0:
            print("No objects detected.")
        for i, box in enumerate(boxes):
            cls_id = int(box.cls[0].item())
            class_name = model.names[cls_id]
            conf = float(box.conf[0].item())
            xyxy = [round(coord, 1) for coord in box.xyxy[0].tolist()]
            print(f"[{i+1}] {class_name:<20} | Confidence: {conf*100:.1f}% | Coordinates: {xyxy}")
            
    print("="*50)
    print(f"Annotated result image saved in: runs/detect/predictions/")

if __name__ == "__main__":
    img_arg = sys.argv[1] if len(sys.argv) > 1 else None
    run_prediction(img_arg)
