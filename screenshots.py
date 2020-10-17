import pyautogui
import time
import pytesseract
import discord


async def main(message):
    start_game_screenshot()
    await message.channel.send("Screenshot code tested")

async def start_game_screenshot():
    time.sleep(6)
    screenshot = pyautogui.screenshot()
    screenshot.save("openingScreen.png")
    screenshot_to_text = pytesseract.image_to_string(screenshot)
    screenshot_words = set(screenshot_to_text.strip().strip('\n').strip("\\").strip("/").lower().split(" "))
    
    start_game_keywords = {"shhhh", "crewmate", "impostor"}

    if len(screenshot_words.intersection(start_game_keywords)) > 0:
        # mute everyone
        print('')