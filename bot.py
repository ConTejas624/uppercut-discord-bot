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
        # get discord users
        await message.channel.send('Please list each discord user who is playing Among Us in the server\ndo so by mentioning each applicable discord user in your next message. Do not mention yourself or any other users or roles')
        def same_user(m):
            return m.author == message.author
        m2 = await client.wait_for('message', check=same_user)   # wait for same user to respond
        
        usernames = [m2.author]     # add message author to list first
        for user in m2.mentions:    # add each of the mentioned users to the list
            usernames.append(user)

        if len(usernames) > 10:
            await m2.channel.send("Error, too many players for Among Us")
            return
        await amongus.main(message, usernames)     # Call the amoung_us script main method
    
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