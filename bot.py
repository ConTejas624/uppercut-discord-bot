import discord, among_us

# reference links
# discord.py API reference: https://discordpy.readthedocs.io/en/latest/api.html#
# discord dev app portal: https://discord.com/developers/applications
# execute another python script: https://stackoverflow.com/questions/3781851/run-a-python-script-from-another-python-script-passing-in-arguments

client = discord.Client()

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author.bot: # does not respond to commands from a bot
        return
    
    if message.content.startswith('$ping'):
        await message.channel.send('pong')
    
    if message.content.startswith('$among start'):
        await among_us.main(message)

    if message.content == '$end':
        await message.channel.send('Goodbye')
        await client.logout()

token_file = open("resources\\token.txt", "r")
token = token_file.read()
token_file.close()

client.run(token)