import discord

# discord.py API reference: https://discordpy.readthedocs.io/en/latest/api.html#
# discord dev app portal: https://discord.com/developers/applications

client = discord.Client()

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

async def on_message(message):
    if message.author == client.user: # makes sure the bot does not trigger itself
        return
    
    if message.content.startswith('$ping'):
        await message.channel.send('pong')

token_file = open("resources\\token.txt", "r")
token = token_file.read()
token_file.close()

client.run(token)