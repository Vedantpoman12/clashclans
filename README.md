# ⚔️ Clash of Clans YOLOv8 AI Detection & Auto Bot

An autonomous AI-powered computer vision system and bot for **Clash of Clans** built using **Ultralytics YOLOv8**, OpenCV, and PyAutoGUI.

---

## 🌟 Features
- **YOLOv8 Object Detection**: Trained to detect Town Halls (TH9–TH12), Attack buttons, Next buttons, Resource counters, and Defenses.
- **Dead Base Recognition**: Detects empty Eagle Artillery and empty Inferno Towers for high-loot raids.
- **Autonomous Attack Bot**: Automatically clicks Attack, finds matches, detects dead bases, deploys armies along the borders, and returns home.
- **Auto Upgrader**: Automatically triggers wall and suggested building upgrades.
- **Real-Time Live Overlay**: Fast screen preview with real-time bounding boxes and FPS monitor.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Vedantpoman12/clashclans.git
   cd clashclans
   ```

2. **Install dependencies:**
   ```bash
   pip install ultralytics torch torchvision opencv-python pyautogui pillow pywin32
   ```

---

## 🚀 Usage

### 1. Run the Autonomous Bot
```bash
python clash_bot.py
```
- Select `1` for Auto Attack (Scout & Deploy).
- Select `2` for Auto Upgrade.
- Select `3` for Continuous Raiding Loop.

*💡 Emergency Stop: Move your mouse cursor into the very top-left corner of the monitor (`0,0`).*

### 2. Run Real-Time Screen Detection
```bash
python live_detect.py
```
*(Press `q` on the preview window to exit).*

### 3. Test Detection on a Single Image
```bash
python predict.py "path_to_image.png"
```

### 4. Train the Model
```bash
python train.py
```
---

## 📊 Dataset Classes
Trained across 26 labels including:
`TH_9`, `TH_10`, `TH_11`, `TH_12`, `attack_button`, `builder_status_text`, `confirm_button`, `cross`, `dark_elixir_label`, `eagle_empty`, `eagle_loaded`, `elixier_label`, `end_battle_button`, `find_a_match_button`, `gold_label`, `hero_hall`, `hero_upgrade`, `inferno_empty`, `inferno_loaded`, `lab_status_text`, `my_dark_elixir_label`, `my_elixir_label`, `my_gold_label`, `next_button`, `suggested_upgrade_1`, `upgrade_button`.
