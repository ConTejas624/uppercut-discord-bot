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
    if message.author.bot:      # does not respond to commands from a bot
        return
    
    amongus = among_us.AmongUs()
    
    if message.content.startswith('$ping'):     # test connection
        await message.channel.send('pong')
    
    if message.content.startswith('$among start'):  # begin Among Us mode
        # first get message author and associated player
        await message.channel.send('State your Among Us name (including capitcalization)')
        def same_user(m):
            return m.author == message.author
        color = await client.wait_for('message', check=same_user)   # wait for same user to respond
        usernames = [message.author]    # Discord users
        players = [color.content]       # Among Us names
        
        await message.channel.send('All players please respond with their exact Among Us name, including capitalization in the format $player <name>')
        await message.channel.send('Once all players have responded, please type \'$player done\'')

        while True:
            def is_color(m):
                return m.content.startswith('$player')
            new_color = await client.wait_for('message', check=is_color)

            if new_color.content == '$player done': # all players have been entered
                break
            else:
                players.append(new_color.content)
                usernames.append(new_color.author)
        await amongus.main(message, usernames, players)     # Call the amoung_us script main method
    
    if message.content.startswith('$help'):     # outputs directions for bot usage
        await message.channel.send('Commands:\n$among start: start a game of Among Us\n$among end: end ongoing Among Us game\n$end: terminate Discord bot')

    if message.content.startswith('$among end'):    # exits Among Us mode
        await amongus.stop()

    if message.content == '$end':   # Disconnects the bot and stops running code
        await message.channel.send('Goodbye! Thank you for using the Uppercut Discord Bot for Among Us!')
        print('logged out from {0.user}'.format(client))
        await client.logout()

token_file = open("resources\\token.txt", "r")  # get bot token from a file
token = token_file.read()                       # file in .gitignore for security
token_file.close()

client.run(token)   # run the bot