import pyautogui, time, pytesseract, discord, deadplayers

# run these for libraries
# py -3 -m pip install -U discord.py
# py -3 -m pip install -U pytesseract
# py -3 -m pip install -U pyautogui
# also need to install tesseract: https://github.com/tesseract-ocr/tesseract

class Screenshots:
    muted = False # are players muted
    gameContinues = True # should the game continue to run
    gameRunning = True # check for endgame
    mode = "first run"
    dead_players = []
    deadplayer = deadplayers.DeadPlayers()
    names = []


    # keywords for the start of the game
    startMuteKeywords = {"imposter", "impostor", "shhhhhhh!", "shhhhhhh", "crewmate" "there", "are", "impostors", "shhh", "shh", "shhhh", "[]mpeostor"}
    # keywords for the end of the game
    endGameUnmuteKeywords = {"defeat", "victory", "quit", "play", "again", "victory\n\n"}
    # keywords for returning from discussion back to the game
    returnToGameMuteKeywords = {"was", "not", "an", "ejected", "(skipped)", "skipped", "no", "one"}             # 'imposter' removed due to overlap
    # keywords for starting the discussion period after a report or emergency meeting
    startDiscussionUnmuteKeywords = {"who", "is", "the", "imposter?", "discuss", "discuss!", "dead", "body", }  # 'imposter' removed due to overlap

    async def main(self, message, players):
        self.names = players
        while (self.muted == False):
            if (self.gameContinues == False):
                self.muted == True # end game
            if (self.muted == False):
                await self.check_screenshot_mute(message, self.startMuteKeywords, "The game has begun. All players muted")
                if (self.mode != "first run"):
                    time.sleep(5) # 5 second delay to prevent switching from start game to discussion too quickly
        while (self.gameContinues == True):
            while (self.muted == True and self.gameContinues): # discussion
                await self.check_screenshot_mute(message, self.startDiscussionUnmuteKeywords, "The discussion has started. Alive players unmuted.")
            while (self.muted == False and self.gameContinues): # back to game
                await self.check_screenshot_mute(message, self.returnToGameMuteKeywords, "Voting has ended. All players muted.")
        await self.sendMessage(message, "The game has ended") # game ended

    async def sendMessage(self, message, prt): # send message in Discord chat
            await message.channel.send(prt)

    async def check_screenshot_mute(self, message, keywords, mutingMessage):

        # take screenshot of user screen with pyautogui
        screenshot = pyautogui.screenshot()
        screenshot.save("resources\\currentScreen.png")

        # convert image to text with pytesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        screenshot_to_text = pytesseract.image_to_string(screenshot, lang = 'eng')
        
        # remove unneccessary characters and split into an array of words
        screenshot_words = set(screenshot_to_text.strip().strip("\n").strip("\\").strip("/").lower().split(" "))
        
        # print (screenshot_words)

        if len(screenshot_words.intersection(self.endGameUnmuteKeywords)) > 0: # end game
           await self.endGame()
           print(self.gameContinues)
           self.mode = "finish"
        else:
            if len(screenshot_words.intersection(keywords)) > 0: # check if any words match keywords
                if (keywords == self.startMuteKeywords):
                    self.mode = "silence"
                elif (keywords == self.startDiscussionUnmuteKeywords):
                    self.mode = "talk"
                    await self.deadplayer.main(self.names)
                    self.dead_players = self.deadplayer.the_dead
                elif (keywords == self.returnToGameMuteKeywords):
                    self.mode = "silence"
                if (mutingMessage == "The game has ended"):
                    self.mode = "finish"
                    self.gameRunning = False
                await self.sendMessage(message, mutingMessage)
                if (self.muted == True): # switch mute
                    self.muted = False
                else:
                    self.muted = True
                #else:
                #   await self.sendMessage(message, "No word found")

    async def endGame(self): # end game
        self.gameContinues = False
        self.muted = True
        self.mode = "finish"

    async def check_end_game(self, message): # check if game should end
        mutingMessage = "The game has ended"
        while (self.gameRunning):
            await self.check_screenshot_mute(message, self.endGameUnmuteKeywords, mutingMessage)
        await self.endGame() # end game