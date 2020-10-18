import discord, among_us, screenshots

# reference links
# discord.py API reference: https://discordpy.readthedocs.io/en/latest/api.html#
# discord dev app portal: https://discord.com/developers/applications

client = discord.Client()


@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    screenshot = screenshots.Screenshots()
    # if message.author == client.user: # makes sure the bot does not trigger itself
    if message.author.bot: # does not respond to commands from a bot
        return
    
    if message.content.startswith('$ping'):
        await message.channel.send('pong')
    
    if message.content.startswith('$among start'):
        
        await among_us.main(message)
        # await screenshot.check_end_game(message)
        #await screenshot.main(message)

    #if (message.content.startswith('$screenshot test')):
    #    await screenshot.main(message)

    # if (message.content.startswith('$endgame')):
        #await screenshot.check_end_game(message)
    


        
    if message.content.startswith('$among end'):
        await among_us.stop()

    if message.content == '$end':
        await message.channel.send('Goodbye')
        print('logged out from {0.user}'.format(client))
        await client.logout()

token_file = open("resources\\token.txt", "r")
token = token_file.read()
token_file.close()

client.run(token)