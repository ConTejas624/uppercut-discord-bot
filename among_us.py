import discord, time, threading, screenshots

# runs Among Us mode code

class AmongUs:
    running = True
    screenshot = screenshots.Screenshots()

    async def main(self, message):
        if message.author.voice is None:    # Checks that the user who called the command is in a voice channel
            await message.channel.send("Error: join a voice channel in the server first")
            return

        v_channel = message.author.voice.channel
        server = message.guild

        await message.channel.send("Among Us mode initialized")

        #t = time.time()
        while self.running == True:
            last_mode = "first run"
            await self.screenshot.main(message)
            mode = self.screenshot.mode
            print(mode)
           
            if mode == "silence" and last_mode != mode:
                await v_channel.set_permissions(server.default_role, speak = False)
                print("silence")
            elif mode == "talk" and last_mode != mode:
                await v_channel.set_permissions(server.default_role, overwrite = None)
                print("talk")
            elif mode == "finish":
                self.running == False
                print("finish")
                break
            last_mode = mode
            # await discord.utils.sleep_until(time.gmtime(time.time()+1))
            # time.sleep(1-time.monotonic()%1)
        
        await v_channel.set_permissions(server.default_role, overwrite = None)

    async def stop(self):
        self.running = False
        await self.screenshot.endGame()
