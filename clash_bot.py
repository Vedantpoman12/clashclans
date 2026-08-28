import time
import random
import sys
import pyautogui
import numpy as np
import cv2
from PIL import ImageGrab
from ultralytics import YOLO
import os

# PyAutoGUI safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

class ClashBot:
    def __init__(self, model_path="runs/detect/clash_detector/weights/best.pt"):
        if not os.path.exists(model_path):
            model_path = r"C:\Users\vedan\runs\detect\clash_detector\weights\best.pt"
            
        print(f"Loading YOLO Model from: {model_path}")
        self.model = YOLO(model_path)
        print("Bot initialized successfully!\n")

    def capture_screen(self):
        """Captures full desktop screen."""
        try:
            img = pyautogui.screenshot()
            frame = np.array(img)
            return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        except Exception:
            try:
                img = ImageGrab.grab()
                frame = np.array(img)
                return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            except Exception as e:
                print(f"Error capturing screen: {e}")
                return None

    def scan_screen(self, conf=0.25):
        """Scans current screen and returns all detected game elements."""
        frame = self.capture_screen()
        if frame is None:
            return []
            
        # Run YOLO detection on GPU (device=0)
        results = self.model.predict(source=frame, conf=conf, verbose=False, device=0)
        detections = []
        
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0].item())
                class_name = self.model.names[cls_id]
                score = float(box.conf[0].item())
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                detections.append({
                    "name": class_name,
                    "conf": score,
                    "bbox": [x1, y1, x2, y2],
                    "center": (center_x, center_y)
                })
        return detections

    def click_target(self, target_names, conf=0.25, click_delay=0.8):
        """Finds any of the specified targets on screen and clicks it."""
        if isinstance(target_names, str):
            target_names = [target_names]
            
        detections = self.scan_screen(conf=conf)
        for det in detections:
            if det["name"] in target_names:
                x, y = det["center"]
                print(f"🎯 [FOUND] {det['name']} ({det['conf']*100:.1f}%) at ({x}, {y}) -> CLICKING!")
                pyautogui.moveTo(x, y, duration=0.3)
                pyautogui.click()
                time.sleep(click_delay)
                return True
        return False

    def auto_attack_routine(self, max_searches=15):
        """Full automated attack sequence."""
        print("\n======================================")
        print("⚔️  STARTING ATTACK CYCLE")
        print("======================================")
        
        # 1. Click Attack Button on home screen
        print("Looking for 'Attack' button...")
        clicked_attack = self.click_target(["attack_button", "attack"], conf=0.25)
        
        if not clicked_attack:
            print("⚠️ Attack button not recognized via AI. Trying bottom-left fallback click...")
            # Fallback bottom-left attack area
            w, h = pyautogui.size()
            pyautogui.click(int(w * 0.08), int(h * 0.90))
            time.sleep(1.0)
            
        time.sleep(1.2)
        
        # 2. Click 'Find a Match'
        print("Looking for 'Find a Match' button...")
        clicked_find = self.click_target(["find_a_match_button", "confirm_button"], conf=0.20)
        if not clicked_find:
            print("Clicking center-right 'Find a Match' area...")
            w, h = pyautogui.size()
            pyautogui.click(int(w * 0.75), int(h * 0.72))
            
        print("Searching for opponent bases...")
        time.sleep(4.0)

        # 3. Scouting Bases
        for search_idx in range(max_searches):
            print(f"\n[Base #{search_idx + 1}] Analyzing defenses...")
            time.sleep(1.5)
            detections = self.scan_screen(conf=0.20)
            names_detected = [d["name"] for d in detections]
            print(f"Detected elements: {names_detected}")

            # Check if this base has empty eagle/inferno (dead base) or if we want to attack
            is_dead_base = any(name in ["eagle_empty", "inferno_empty"] for name in names_detected)
            has_next = any(name == "next_button" for name in names_detected)

            if is_dead_base:
                print("💎 Dead Base Identified (Empty Defenses)! Launching attack...")
                self.deploy_army()
                return True
            elif has_next and search_idx < (max_searches - 1):
                print("Skipping to next base...")
                self.click_target("next_button", conf=0.20)
                time.sleep(3.0)
            else:
                # Attack anyway or deploy
                print("Deploying army on this base...")
                self.deploy_army()
                return True

        print("Finished scouting sequence.")
        return False

    def deploy_army(self):
        """Deploys troops around the map edges."""
        print("🚀 Deploying troops on map boundaries...")
        w, h = pyautogui.size()
        
        # Select troop slots from bottom troop bar
        troop_bar_y = int(h * 0.93)
        troop_start_x = int(w * 0.20)
        
        for slot in range(4):
            # Select troop icon
            slot_x = troop_start_x + (slot * int(w * 0.065))
            pyautogui.click(slot_x, troop_bar_y)
            time.sleep(0.15)
            
            # Spam click around bottom corners of the battlefield
            for _ in range(6):
                rx = random.randint(int(w * 0.18), int(w * 0.82))
                ry = random.randint(int(h * 0.72), int(h * 0.82))
                pyautogui.click(rx, ry)
                time.sleep(0.08)
                
        print("Troops deployed! Waiting 15s for battle...")
        time.sleep(15)
        
        # End battle and return home
        print("Ending battle and returning home...")
        if self.click_target(["end_battle_button", "surrender"], conf=0.20):
            time.sleep(1.0)
            self.click_target("confirm_button", conf=0.20)
            time.sleep(2.0)
            
        self.click_target(["return_home", "okay"], conf=0.20)
        time.sleep(2.0)
        print("Returned to Home Village!")

    def auto_upgrade_walls(self):
        """Attempts to click suggested upgrades / walls and spend gold/elixir."""
        print("\n======================================")
        print("🧱 STARTING AUTO UPGRADE ROUTINE")
        print("======================================")
        
        # Check for builder suggestion icon at the top
        if self.click_target(["suggested_upgrade_1", "builder_status_text"], conf=0.25):
            time.sleep(1.0)
            if self.click_target(["upgrade_button", "upgrade", "upgrade_gold", "upgrade_elixer"], conf=0.25):
                print("✅ Upgrade initiated!")
                time.sleep(0.8)
                self.click_target("confirm_button", conf=0.25)
                return True
                
        print("No pending upgrade menus detected on screen.")
        return False

def main():
    bot = ClashBot()
    print("Select Bot Mode:")
    print(" [1] Auto Attack (Search, Deploy Troops, Return Home)")
    print(" [2] Auto Upgrade (Suggested upgrades/walls)")
    print(" [3] Infinite Loop (Attack -> Return Home -> Upgrade -> Repeat)")
    
    choice = input("\nEnter choice (1, 2, or 3): ").strip()
    
    print("\n⏳ Starting in 4 seconds! Make sure your Clash of Clans window is on screen...")
    print("💡 EMERGENCY STOP: Move your mouse cursor into the very TOP-LEFT corner of your screen.\n")
    time.sleep(4)
    
    if choice == "1":
        bot.auto_attack_routine()
    elif choice == "2":
        bot.auto_upgrade_walls()
    elif choice == "3":
        while True:
            bot.auto_attack_routine()
            time.sleep(4)
            bot.auto_upgrade_walls()
            print("\nWaiting 20 seconds before next raid...")
            time.sleep(20)
    else:
        print("Invalid option selected.")

if __name__ == "__main__":
    main()
