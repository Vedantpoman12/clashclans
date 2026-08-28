import cv2
import numpy as np
import pyautogui
from ultralytics import YOLO
import os
import time

def live_screen_detect():
    weights_path = "runs/detect/clash_detector/weights/best.pt"
    if not os.path.exists(weights_path):
        weights_path = r"C:\Users\vedan\runs\detect\clash_detector\weights\best.pt"
        
    if not os.path.exists(weights_path):
        print(f"Error: Could not find model weights at '{weights_path}'.")
        return

    print(f"Loading YOLO model: {weights_path}")
    model = YOLO(weights_path)

    print("=" * 60)
    print(" LIVE SCREEN DETECTION RUNNING")
    print(" -> Switch to your Clash of Clans window.")
    print(" -> Press 'q' on the preview window to exit.")
    print("=" * 60)

    cv2.namedWindow("Clash of Clans - Realtime AI Detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Clash of Clans - Realtime AI Detection", 1020, 580)

    fps_time = time.time()
    frame_count = 0
    fps = 0

    while True:
        try:
            # Capture screen cleanly using pyautogui
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            # Convert RGB to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        except Exception as e:
            time.sleep(0.05)
            continue

        # GPU inference
        results = model.predict(source=frame, conf=0.35, verbose=False, device=0)
        annotated_frame = results[0].plot()

        # Calculate FPS
        frame_count += 1
        curr_time = time.time()
        if curr_time - fps_time >= 1.0:
            fps = frame_count / (curr_time - fps_time)
            fps_time = curr_time
            frame_count = 0

        # Draw FPS on screen
        cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (30, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)

        # Show live annotated frame
        cv2.imshow("Clash of Clans - Realtime AI Detection", annotated_frame)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\nLive detection closed by user.")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    live_screen_detect()
