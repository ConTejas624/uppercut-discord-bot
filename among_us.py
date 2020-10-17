import discord, time, threading

# runs Among Us mode code

running = True

async def main(message):
    if message.author.voice is None:    # Checks that the user who called the command is in a voice channel
        await message.channel.send("Error: join a voice channel in the server first")
        return

    v_channel = message.author.voice.channel
    server = message.guild

    await message.channel.send("Among Us mode initialized")


    myThread = threading.Timer(1, set_mode)
    myThread.start(message, v_channel, server)
    t = time.time()
    while running == True:
        await message.channel.send('clock')

        last_mode = 'first run'
        mode = message.content[13:] # would call screenshots.main() once have that # 'silence' or 'talk'
        if mode == 'silence' and last_mode != mode:
            await v_channel.set_permissions(server.default_role, speak = False)
        elif mode == 'talk' and last_mode != mode:
            await v_channel.set_permissions(server.default_role, overwrite = None)
        last_mode = mode
        time.sleep(1-time.monotonic()%1)
    
    await v_channel.set_permissions(server.default_role, overwrite = None)

async def stop():
    running = False