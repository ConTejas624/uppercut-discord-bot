import pyautogui, time, pytesseract, discord

# run these for libraries
# py -3 -m pip install -U discord.py
# py -3 -m pip install -U pytesseract
# py -3 -m pip install -U pyautogui

class Screenshots:
    muted = False # are players muted
    gameContinues = True # should the game continue to run
    gameRunning = True # check for endgame
    startMuteKeywords = {"imposter", "impostor", "shhhhhhh!", "shhhhhhh", "crewmate" "there", "are", "impostors", "shhh", "shh", "shhhh", "[]mpeostor"}
    endGameUnmuteKeywords = {"defeat", "victory", "quit", "play", "again", "victory\n\n"}
    returnToGameMuteKeywords = {"was", "not", "an", "impostor", "ejected", "(skipped)", "skipped", "no", "one"}
    startDiscussionUnmuteKeywords = {"who", "is", "the", "impostor", "imposter?", "discuss", "discuss!", "dead", "body", "reported"}

    async def main(self, message):
        while (self.muted == False):
            if (self.gameContinues == False):
                self.muted == True
            if (self.muted == False):
                await self.check_screenshot_mute(message, self.startMuteKeywords, "The game has begun. All players muted")
                time.sleep(5)
        while (self.gameContinues == True):
            while (self.muted == True and self.gameContinues):
                await self.check_screenshot_mute(message, self.startDiscussionUnmuteKeywords, "The discussion has started. Alive players unmuted.")
            while (self.muted == False and self.gameContinues):
                await self.check_screenshot_mute(message, self.returnToGameMuteKeywords, "Voting has ended. All players muted.")
        await self.sendMessage(message, "The game has ended")

    async def sendMessage(self, message, print):
            await message.channel.send(print)

    async def check_screenshot_mute(self, message, keywords, mutingMessage):
        time.sleep(.5)
        screenshot = pyautogui.screenshot()
        screenshot.save("currentScreen.png")
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        screenshot_to_text = pytesseract.image_to_string(screenshot, lang = 'eng')
        
        screenshot_words = set(screenshot_to_text.strip().strip("\n").strip("\\").strip("/").lower().split(" "))
        
        print (screenshot_words)

        if len(screenshot_words.intersection(self.endGameUnmuteKeywords)) > 0:
           await self.endGame()
           print(self.gameContinues)
        else:
            if len(screenshot_words.intersection(keywords)) > 0:
                if (mutingMessage == "The game has ended"):
                    self.gameRunning = False
                await self.sendMessage(message, mutingMessage)
                if (self.muted == True):
                    self.muted = False
                else:
                    self.muted = True
                #else:
                #   await self.sendMessage(message, "No word found")

    async def endGame(self):
        self.gameContinues = False
        self.muted = True

    async def check_end_game(self, message):
        mutingMessage = "The game has ended"
        while (self.gameRunning):
            await self.check_screenshot_mute(message, self.endGameUnmuteKeywords, mutingMessage)
        await self.endGame()