import pyautogui, discord, pytesseract, time

# Notes on sizing/spacing
# Player card is ~ 621 x 107 pixels
# Player card arrangement is ~ 1278 x 657
# Player card vertical spacing is ~ 31 px
# Player card horizontal spacing is ~ 36 px

class DeadPlayers:
    the_dead = []   # list of dead players
    column = 2 # 0 for first iteration, then 1 for left and 2 for right
    corner = (271, 212, 1278, 657)
    horiz_offset = (657, 0, 0, 0)
    vert_offset = (-657, 138, 0, 0)
    bounds = [928, 764, 621, 107]
    locations = (761, 623, 486, 350, 212)
    dead_pixel_color = (146, 73, 50)
    
    async def main(self, players):
        #skip_vote_loc = pyautogui.locateOnScreen('reference\\skip_vote.png')    # this will take 1-2 sec ona 1920x1080 screen
        x = 10
        while x > 0:
            x = x - 1           
            if x <= len(players):
                if x%2==0:
                    self.bounds[0] = 929
                else:
                    self.bounds[0] = 271
                index = int(x/2)
                self.bounds[1] = self.locations[index]
                dead = await self.is_dead(self.bounds)
                if dead:
                    tup_bound = tuple(self.bounds)
                    self.the_dead.append(await self.read_name(tup_bound))
                else:
                    self.the_dead = None
                    return 

            
    
    async def read_name(self, bounds):
        # take screenshot of user screen with pyautogui
        screenshot = pyautogui.screenshot(region=bounds)
        screenshot.save("resources\\player-card-current.png")


        # convert image to text with pytesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        screenshot_to_text = pytesseract.image_to_string(screenshot, lang = 'eng')
        
        # remove unneccessary characters and split into an array of words
        screenshot_words = set(screenshot_to_text.strip().strip("\n").strip("\\").strip("/").lower().split(" "))
    
    async def is_dead(self, bounds):
        x = bounds[0] + 53
        y = bounds[1] + 53
        print(pyautogui.pixel(x, y))
        return pyautogui.pixelMatchesColor(x, y, self.dead_pixel_color)
         