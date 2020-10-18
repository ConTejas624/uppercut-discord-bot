# uppercut-discord-bot
Uppercut is designed to automatically mute and unmute users in a voice channel on discord while they are playing Among Us, built from the discord.py library

## Libraries Used
- discord.py:	https://discordpy.readthedocs.io/en/latest/
- pyautogui:	https://pyautogui.readthedocs.io/en/latest/
- pytesseract:	https://github.com/madmaze/pytesseract

## Features
- Uses pyautogui to capture the host's primary screen
- The image is then passed to pytesseract
- pytesseract is used to process the image into the words on screen, and checks for keywords
- Those keywords are used to determine whether users should be muted or talking
- The channel @everyone permissions are altered to allow users to speak when allowed

## Future Improvements
- Recognize dead crewmates and keep them muted during discussions -> in progress
- Improve loops for better bot performance while running among_us.py
- Easier to export: make the bot more accessible for others to download and use
- Increase bot's ability to adapt to different resolutions and screen sizes.
- Not sure if it is possible to override this behavior but server owners are unaffected by the mute permissions
