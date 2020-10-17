import discord

# runs Among Us mode code

async def main(message, client):
    if message.author.voice is None:    # Checks that the user who called the command is in a voice channel
        await message.channel.send("Error: join a voice channel in the server first")
        return

    unmuted = message.author.voice.channel
    server = message.guild

    overwrites = {
        server.default_role: discord.PermissionOverwrite(speak = False, deafen_members = True)
    }

    muted_channel = await server.create_voice_channel('muted_channel', overwrites=overwrites)
    await message.channel.send("Among Us mode initialized")


    mode = message.content[13:] # would call screenshots.main() once have that # 'silence' or 'talk'
    if mode == 'silence':
        for user in unmuted.members:
            await user.move_to(muted_channel)
    elif mode == 'talk':
        for user in muted_channel.members:
            await user.move_to(unmuted)
    else:
        await message.channel.send('error')
        print(message.content[13:])

    @client.event
    async def on_message(m):
        if message.author.bot: # does not respond to commands from a bot
            return
        if m.content == '$among end':
            for user in muted_channel.members:
                await user.move_to(muted_channel)
            await m.channel.send('Among Us mode exited')
            return
