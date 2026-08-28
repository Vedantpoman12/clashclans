import os
import sys
from ultralytics import YOLO
import glob

def train():
    print("Initializing YOLOv8 model (yolov8n.pt)...")
    model = YOLO("yolov8n.pt")
    
    data_path = os.path.abspath("data_clean.yaml")
    print(f"Starting training on dataset: {data_path}")
    
    # Train model
    results = model.train(
        data=data_path,
        epochs=30,
        imgsz=640,
        batch=16,
        name="clash_detector",
        device=0, # GPU
        plots=True,
        save=True
    )
    print("Training complete!")
    return model

def predict_sample():
    # Find best or last trained model
    weights_path = "runs/detect/clash_detector/weights/best.pt"
    if not os.path.exists(weights_path):
        weights_path = "runs/detect/clash_detector/weights/last.pt"
    
    if not os.path.exists(weights_path):
        print("No trained weights found to run sample inference.")
        return

    print(f"Loading trained weights from: {weights_path}")
    model = YOLO(weights_path)

    # Pick a sample image from test/images
    test_imgs = glob.glob("clash home manage - dead base detection.v1-mr-bob---dead-locater.yolov8/test/images/*.jpg")
    if not test_imgs:
        test_imgs = glob.glob("clash home manage - dead base detection.v1-mr-bob---dead-locater.yolov8/valid/images/*.jpg")

    if test_imgs:
        sample_img = test_imgs[0]
        print(f"Running inference on sample image: {sample_img}")
        res = model.predict(source=sample_img, save=True, conf=0.25, project="runs/detect", name="sample_output")
        print("\n--- Detection Results ---")
        for r in res:
            for box in r.boxes:
                cls_id = int(box.cls[0].item())
                cls_name = model.names[cls_id]
                conf = float(box.conf[0].item())
                print(f"Detected: {cls_name} (Confidence: {conf:.2f}) at Box: {box.xyxy[0].tolist()}")
        print(f"Annotated result saved to: runs/detect/sample_output/")
    else:
        print("No sample test images found.")

if __name__ == "__main__":
    train()
    predict_sample()
