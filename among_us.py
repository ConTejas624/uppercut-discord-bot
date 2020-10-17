import discord

# runs Among Us mode code

async def main(message, client):
    if message.author.voice is None:    # Checks that the user who called the command is in a voice channel
        await message.channel.send("Error: join a voice channel in the server first")
        return

    v_channel = message.author.voice.channel
    server = message.guild

    unmuted_overwrites = v_channel.overwrites_for(server.default_role)
    muted_overwrites = {
        server.default_role: discord.PermissionOverwrite(speak = False)
    }

    await message.channel.send("Among Us mode initialized")


    mode = message.content[13:] # would call screenshots.main() once have that # 'silence' or 'talk'
    if mode == 'silence':
        await v_channel.set_permissions(server.default_role, overwrite=muted_overwrites)
    elif mode == 'talk':
        pass
    else:
        await message.channel.send('error')
        print(message.content[13:])

    @client.event
    async def on_message(m):
        if message.author.bot: # does not respond to commands from a bot
            return
        if m.content == '$among end':
            pass
            await m.channel.send('Among Us mode exited')
            return
