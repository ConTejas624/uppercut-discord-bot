import discord, time, screenshots

# runs Among Us mode code

running = True

async def main(message, usernames, player_names):
    if message.author.voice is None:    # Checks that the user who called the command is in a voice channel
        await message.channel.send("Error: join a voice channel in the server first")
        return

    v_channel = message.author.voice.channel
    t_channel = message.channel
    server = message.guild
    my_role = None

    has_unmuted_role = False
    for role in server.roles:
        if role.name == 'unmuted:Uppercut':
            has_unmuted_role = True
            my_role = role
    if not has_unmuted_role:
        my_role = await server.create_role('unmuted:Uppercut')

    await t_channel.send("Among Us mode initialized")

    #t = time.time()
    while running == True:
        last_mode = 'first run'
        await v_channel.set_permissions(server.default_role, speak = False)
        for member in usernames:
            await member.add_roles(my_role)
        mode = screenshots.main() # 'silence', 'talk', or 'finish'
        if mode == 'silence' and last_mode != mode:
            await v_channel.set_permissions(server.my_role, speak = False)
        elif mode == 'talk' and last_mode != mode:
            await v_channel.set_permissions(server.my_role, overwrite = None)
        elif mode == 'finish':
            await v_channel.set_permissions(server.my_role, overwrite = None)
            break
        last_mode = mode
        await discord.utils.sleep_until(time.time()+1)
        #time.sleep(1-time.monotonic()%1)
    
    await v_channel.set_permissions(server.default_role, overwrite = None)
    for member in usernames:
        await member.remove_roles(my_role)

async def stop():
    running = False