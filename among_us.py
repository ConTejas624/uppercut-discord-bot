import discord, screenshots, deadplayers

# runs Among Us mode code

class AmongUs:
    running = True
    screenshot = screenshots.Screenshots()
    deadplayer = deadplayers.DeadPlayers()

    async def main(self, message, usernames, player_names):
        if message.author.voice is None:    # Checks that the user who called the command is in a voice channel
            await message.channel.send("Error: join a voice channel in the server first")
            return

        # vars for reference with less typing later
        v_channel = message.author.voice.channel
        t_channel = message.channel
        server = message.guild
        running = True

        my_role = None
        has_unmuted_role = False
        for role in server.roles:   # checks if the role already exists in the server
            if role.name == 'unmuted-Uppercut':
                has_unmuted_role = True
                my_role = role
        if not has_unmuted_role:    # if the role does not exist, creates it
            my_role = await server.create_role()
            await my_role.edit(name = 'unmuted-Uppercut')

        await t_channel.send("Among Us mode initialized")   # let users know it is ready for the game to start

        while running == True:
            last_mode = 'first run'

            await self.screenshot.main(message)     # call main from screenshot to process the screen
            mode = self.screenshot.mode             # set mode

            await v_channel.set_permissions(server.default_role, speak = False) # disables talking in channel for @everyone

            for member in usernames:            # adds the 'unmuted-Uppercut' role to each discord user that is also a player
                await member.add_roles(my_role)
            
            # based on mode, changes role permissions in each channel
            # last_mode helps make sure we don't keep executing code that was previously executed for no reason
            if mode == 'silence' and last_mode != mode:
                await v_channel.set_permissions(my_role, speak = False) # disable speaking for alive players
            elif mode == 'talk' and last_mode != mode:
                dead_players = await self.deadplayer.main(player_names)
                if not dead_players == None:
                    for player in player_names:
                        for dead in dead_players:
                            if player == dead:
                                disc_user = usernames[player_names.index(player)]
                                await disc_user.remove_roles(my_role)
                
                await v_channel.set_permissions(my_role, overwrite = None) # enable talking for alive players
            elif mode == 'finish':
                await v_channel.set_permissions(my_role, overwrite = None) # enable talking for alive players
                break
            last_mode = mode
    
        await v_channel.set_permissions(server.default_role, overwrite = None)  # enable talking for @everyone
        
        for member in usernames:        #  remove custom role from everyone
            await member.remove_roles(my_role)

    async def stop(self):
        running = False
        await self.screenshot.endGame()