import pyautogui, discord, pytesseract, time

class DeadPlayers:
    
    async def main(self):
        screenshot = pyautogui.screenshot()
        screenshot.save("discussionScene.png")

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        screenshot_to_text = pytesseract.image_to_boxes(screenshot)

        print(screenshot_to_text)