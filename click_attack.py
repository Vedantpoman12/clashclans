import time
import pyautogui
from clash_bot import ClashBot

pyautogui.FAILSAFE = False

def click_attack_button():
    print("Initializing bot to find and click the attack button...")
    bot = ClashBot()
    
    print("\n⏳ Make sure your Clash of Clans window is on screen. Searching in 3 seconds...")
    time.sleep(3)
    
    print("Looking for 'Attack' button...")
    clicked_attack = bot.click_target(["attack_button", "attack"], conf=0.25)
    
    if not clicked_attack:
        print("⚠️ Attack button not recognized via AI. Trying bottom-left fallback click...")
        w, h = pyautogui.size()
        pyautogui.click(int(w * 0.08), int(h * 0.90))
        print("Fallback click executed.")
    else:
        print("Attack button clicked successfully via AI!")
        
    time.sleep(1.2) # Wait for the next screen to load
    
    print("Looking for 'Find a Match' button...")
    clicked_find = bot.click_target(["find_a_match_button", "confirm_button"], conf=0.20)
    
    if not clicked_find:
        print("⚠️ 'Find a Match' button not recognized via AI. Trying center-right fallback click...")
        w, h = pyautogui.size()
        pyautogui.click(int(w * 0.75), int(h * 0.72))
        print("Fallback click executed for Find a Match.")
    else:
        print("'Find a Match' button clicked successfully via AI!")

if __name__ == "__main__":
    click_attack_button()
