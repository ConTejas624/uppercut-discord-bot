import pyautogui
import time
import pytesseract
import discord

@client.event
async def take_first_screenshot():
    time.sleep(6)
    screenshot = pyautogui.screenshot()
    screenshot.save("openingScreen.png")
    screenshot_to_text = pytesseract.image_to_string(screenshot)
    screenshot_words = set(screenshot.strip().strip('\n').strip("\\").strip("/").lower().split(" "))
    
    start_game_keywords = {"shhhh", "crewmate", "impostor"}

    if len(process_screenshot.intersection(start_game_keywords)) > 0:
        # mute everyone