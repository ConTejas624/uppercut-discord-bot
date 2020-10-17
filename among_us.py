import discord

# runs Among Us mode code

async def main(message):
    # variables
    voice_channel = message.author.voice
    
    if voice_channel is None:    # Checks that the user who called the command is in a voice channel
        await message.channel.send("Error: join a voice channel in the server first")
        return
    
    await message.channel.send("Among Us mode initialized")
    
    mode = 'silence' # would call screenshots.main() once have that # 'silence' or 'talk'
    if mode == 'silence':
        for user in voice_channel.members:
            await user.edit(user.mute(True))
    elif mode == 'talk':
        for user in voice_channel.members:
            await user.edit(user.mute(False))
    
    