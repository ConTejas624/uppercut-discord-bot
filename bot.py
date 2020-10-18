import discord, among_us

# reference links
# discord.py API reference: https://discordpy.readthedocs.io/en/latest/api.html#
# discord dev app portal: https://discord.com/developers/applications

client = discord.Client()

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author.bot: # does not respond to commands from a bot
        return
    
    amongus = among_us.AmongUs()
    
    if message.content.startswith('$ping'):
        await message.channel.send('pong')
    
    if message.content.startswith('$among start'):
        await message.channel.send('State your Among Us name (including capitcalization)')
        def same_user(m):
            return m.author == message.author
        color = await client.wait_for('message', check=same_user)
        usernames = [message.author]    # Discord users
        players = [color.content]       # Among Us names
        
        await message.channel.send('All players please respond with their exact Among Us name, including capitalization in the format $player <name>')
        await message.channel.send('Once all players have responded, please type \'$player done\'')
        while True:
            def is_color(m):
                return m.content.startswith('$player')
            new_color = await client.wait_for('message', check=is_color)
            if new_color.content == '$player done':
                break
            else:
                players.append(new_color.content)
                usernames.append(new_color.author)
        
        await amongus.main(message, usernames, players)
    if message.content.startswith('$among end'):
        await amongus.stop()

    if message.content == '$end':
        await message.channel.send('Goodbye! Thank you for using the Uppercut Discord Bot for Among Us!')
        print('logged out from {0.user}'.format(client))
        await client.logout()

token_file = open("resources\\token.txt", "r")
token = token_file.read()
token_file.close()

client.run(token)