# NOTE: BuiltInCogs.py is the Built In Cog. Pretty self-explanatory.
"""
BuiltInCogs.py is the Built In Cog, as seen above. It is automatically loaded when you run community_bot.py.
Without it, the bot would be severely crippled, and there would be no functionality.
BuiltInCogs.py is made up of FIVE different classes, which are:
    - DebugAndEvents. This class contains all the events for the bot, as well as some commands to debug the bot.
    - OwnerOnly. This class can only be used by the server/guild owner. Pretty self-explanatory.
    - FunCommands. This  class is mostly used by P E A S E N T S, which contains several fun commands.
    - Math. This class contains some basic arithmetic operations, and if you want more cmds, import MoreMathCommands.
    - ModeratorCommands. This class contains some very useful commands for the moderators of your discord server.
    - MiscellaneousCommands. This class contains miscellaneous commands. WOW!

I won't go into details about this, because then it would be way too long, to find out more, go to BuiltInCogs_doc.txt.

"""

import random
import time
import math as m
import os
import asyncio
from configparser import ConfigParser
import datetime
import logging
import json
from threading import Thread

from playsound import playsound
import sys

from discord.ext import commands
import discord

logging.basicConfig(level=logging.WARNING)
configure = ConfigParser()
configure.read(r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community '
               r'Bot\cogs\community_bot_info.ini')

# NOTE: BELOW ARE SOME KEY BOOLEANS
debug = True
shutdown = False
going_to_run_debug = True
beta_mode = False

# NOTE: BELOW ARE SOME KEY STRING VALUES
bot_shutdown_message = 'Sorry! The bot is shut down by the owner! Try again later!'
beta_testing_message = 'Sorry! The bot is only available for selected beta testers! Try again later!'
discord_hyphen_separator = '------------------------------------------------'
no_help_error_message = "DOESN'T WORK.\nSORRY! This command doesn't work, so there is no reason to give it a full " \
                        "command\nYou will see this message ever time there is an incomplete command "
no_help_simple_message = "This command does not have a complete help message for some reason.\nONE: The message is " \
                         "too simple, and there will be too much work to implement a full help command.\nTWO: The " \
                         "message is too similar to another help command, so we are just too lazy to add " \
                         "them.\nTHREE: The message's help command will be implemented, but not right now. "
version = 'v0.5.0.b2'


# NOTE: BELOW ARE SOME KEY INTEGER VALUES

# TODO: Make all commands following beta mode patterns
# FIXME Make all commands that message someone has a `except Exception as e` block
# TODO: Make all help commands have f""" instead of f""

# UPDATE: 0.5.0 will include... too many things to list (see community_bot_changelog.txt)

def is_guild_owner():
    """finds the guild owner of the server"""

    def predicate(ctx):
        """actually returns if the message author, and the guild owner are the same"""
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id

    return commands.check(predicate)


class DebugAndEvents(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # IDEA: Actually fill this in and give the joiner a custom greeting
        with open(r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community Bot\cogs\infractions.json',
                  'r') as read_json_file:
            deserialized_infractions = json.load(read_json_file)

        temp_dict_of_member_and_no_infraction = {str(member.id): 0}
        deserialized_infractions.update(temp_dict_of_member_and_no_infraction)

        with open(r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community Bot\cogs\infractions.json',
                  'w') as write_json_file:
            json.dump(deserialized_infractions, write_json_file)

        read_json_file.close()
        write_json_file.close()

    @commands.Cog.listener()
    async def on_ready(self):

        playsound(r"C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community Bot\Misc things for "
                  r"Community Bot\Notif Sound 1.mp3")

        if beta_mode and shutdown:
            await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Massive '
                                                                                                       'Shutdown'))
        elif not beta_mode and shutdown:
            await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Shut Down'))
        elif beta_mode and not shutdown:
            await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game('In BETA MODE'))
        elif not beta_mode and not shutdown:
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('with Brandon. Duh'))
            # NOTE: In the morning, check if the above code actually works
        if not shutdown:
            print(f'The discord bot is now online')
        else:
            print('The discord bot is now online, but it is shutdown')

        if not beta_mode:
            print('The discord bot is available to anyone')
        else:
            print('The discord bot is now in beta mode. This means that only a few people can access it')

    while going_to_run_debug:
        if not debug:
            print('Debug is set to False. Custom syntax will be used.')

            @commands.Cog.listener()
            async def on_command_error(self, ctx, error):
                if isinstance(error, commands.CheckFailure):
                    await ctx.send('Sorry. It looks like you do not have permission to use that command.')
                elif isinstance(error, commands.MissingRequiredArgument):
                    await ctx.send('Sorry. It looks like you forgot an argument')
                elif isinstance(error, commands.CommandNotFound):
                    await ctx.send('Sorry. That command does not exist')
                else:
                    brandon = self.bot.get_user(683852333293109269)
                    await brandon.send('**`ERROR ???:`** OH NO! Unknown Error!')
                    await ctx.send('**`ERROR ???"`** OH NO! Unknown Error!')

        else:
            print('Debug is set to True. Used for debugging stuff.')
            going_to_run_debug = False

        if not shutdown:
            print('Shutdown is set to False. You can use commands freely.')
        else:
            print('Shutdown is set to True. No one can use the commands.')

    @commands.Cog.listener()
    async def on_message(self, message):
        # IDEA: Continue to fill this to censor words
        if message.author.id == 753295703077421066:
            return

        forbidden_words = ['fuck', 'bitch', 'ass', 'shit', 'gabe itch']  # NOTE: Don't mean it sorry!
        test_forbidden_words = ['cheese', 'yum']  # NOTE: Don't like saying them? Use the tests!
        for forbidden_word in forbidden_words:
            if forbidden_word in message.content and 'nsfw' not in str(message.channel).strip():
                await message.delete()
                brandon = self.bot.get_user(683852333293109269)
                author = self.bot.get_user(message.author.id)
                time_of_profanity = datetime.datetime.fromtimestamp(time.time()).strftime('%a %b %d %Y, %I:%M:%S %p')
                # NOTE: Make it actually able to write stuff

                with open(r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community Bot\cogs\infractions.json', 'r') as read_json_file:
                    deserialized_infractions = json.load(read_json_file)

                if not deserialized_infractions:
                    dict_of_writing_to_json = {}

                    for member in message.guild.members:
                        member_id = str(member.id)
                        temp_dict_of_member_id_and_no_infraction = {member_id: 0}
                        dict_of_writing_to_json.update(temp_dict_of_member_id_and_no_infraction)

                    with open(r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community Bot\cogs\infractions.json', 'w') as write_json_file:
                        json.dump(dict_of_writing_to_json, write_json_file, indent=4)

                    write_json_file.close()

                    with open(r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community Bot\cogs\infractions.json', 'r') as read_json_file:
                        deserialized_infractions_refresh = json.load(read_json_file)

                    await author.send('You have 1 infraction')
                    deserialized_infractions_refresh[str(message.author.id)] += 1

                    with open(r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community Bot\cogs\infractions.json', 'w') as write_json_file:
                        json.dump(deserialized_infractions_refresh, write_json_file, indent=4)
                    read_json_file.close()

                else:

                    with open(r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community Bot\cogs\infractions.json', 'r') as read_json_file:
                        deserialized_infractions = json.load(read_json_file)

                    deserialized_infractions[str(message.author.id)] += 1

                    with open(r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community Bot\cogs\infractions.json', 'w') as write_json_file:
                        json.dump(deserialized_infractions, write_json_file, indent=4)

                    write_json_file.close()

                    with open(r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community Bot\cogs\infractions.json', 'r') as read_json_file:
                        deserialized_infractions = json.load(read_json_file)

                    num_infractions = deserialized_infractions[str(message.author.id)]
                    await author.send(f"You have {num_infractions} infractions.")

                    read_json_file.close()

                with open(r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community Bot\cogs\infractions.json',
                          'r') as read_json_file:
                    deserialized_infractions = json.load(read_json_file)

                num_infractions = deserialized_infractions[str(message.author.id)]

                await author.send(f"**`ALERT:`** The moderator team has been informed that on **`{time_of_profanity}`**"
                                  f", you have used a forbidden word. You have violated Rule **`1`** and Rule **`9`**"
                                  f" of Article I, and this will not be tolerated. Your punishment will be put under"
                                  f" consideration. The minimal punishment is to get muted for 5 minutes,"
                                  f" but your roles will be returned. This is rather serious, and if this continues,"
                                  f" the consequences will be more severe. In the future, please refrain from using"
                                  f" profanity.\nBest Regards,\n\t- The Mod team\n"
                                  f"{discord_hyphen_separator} **`INFO`** {discord_hyphen_separator}\n"
                                  f"Forbidden word used: **`{forbidden_word}`**\n"
                                  f"Date of profanity: **`{time_of_profanity}`**\n"
                                  f"Channel of used profanity: **`{str(message.channel).strip()}`**\n"
                                  f"Number of infractions: **`{num_infractions}`**")
                await brandon.send(f"**`WARNING 004:`** {message.author} has used a forbidden word! **`WORD:`** "
                                   f"{forbidden_word}")

                read_json_file.close()


                # NOTE: Do this in the morning, mostly because then I have Wi-Fi

                """str_to_be_placed_in_ini = '{'
                for member in message.guild.members:
                    str_to_be_placed_in_ini += member.id
                dict_of_user_infractions_STR_version = configure.get('User Info', 'infractions_dictionary')
                user_infractions_dict = json.loads(dict_of_user_infractions_STR_version.strip())
                num_infractions_of_user = user_infractions_dict[str(message.author.id)]
                configure['User Info']['infractions_dictionary'] = '{dfsf}'
                with open('community_bot_info.ini', 'w') as configfile:
                    configure.write(configfile)"""

    @commands.command(help=f"{discord_hyphen_separator} PING {discord_hyphen_separator}\n"
                           f"The ping command is used to debug if the bot is acting slow."
                           f"It is measured in milliseconds, and anything above 100 is severe to critical"
                           f"A.K.A Bot latency\n"
                           f"{discord_hyphen_separator} EXAMPLE {discord_hyphen_separator}\n"
                           f"**`INPUT:`** $ping\n"
                           f"**`OUTPUT:`** Pong! Bot "
                           f"reaction time: (bot latency)", brief='- used for debugging why the bot is acting so slow')
    @commands.has_any_role('MODERATOR', 'Trusted', 'Co-manager', 'Administrator', 'CEO')
    async def ping(self, ctx):
        role = discord.utils.find(lambda r: r.name == 'Trusted', ctx.guild.roles)
        roles = ctx.author.roles
        bot_latency = self.bot.latency * 1000
        if not shutdown and not beta_mode:
            if bot_latency >= 100:
                await ctx.send(f"**`WARNING 004:`** Pong! Bot reaction time: {round(bot_latency)} milliseconds")
            else:
                await ctx.send(f"Pong! Bot reaction time: {round(bot_latency)} milliseconds")
        else:
            if shutdown and not beta_mode:
                await ctx.send(bot_shutdown_message)
            if beta_mode and not shutdown:
                if role in roles:
                    await ctx.send(f"Pong! Bot reaction time: {round(self.bot.latency * 1000)} milliseconds")
                else:
                    await ctx.send(beta_testing_message)

    @commands.command(help=f"{discord_hyphen_separator} ERRORS {discord_hyphen_separator}"
                           f"The errors command is used to DM you a list"
                           f"of potential errors the bot might give to you.\n"
                           f"NOTE: Remember that the error list will be a DM."
                           f"There will be an error if you blocked the bot\n"
                           f"{discord_hyphen_separator} EXAMPLE {discord_hyphen_separator}"
                           f"**`INPUT:`** $errors\n"
                           f"**`OUTPUT:`** (List of Errors)", brief='- used to see all errors. WILL BE DM')
    @commands.has_any_role('MODERATOR', 'TRUSTED', 'Co-manager', 'Administrator', 'CEO')
    async def errors(self, ctx):
        # NOTE Complete this
        if not shutdown:
            author_dm = self.bot.get_user(ctx.author.id)
            await author_dm.send('-------------------------------------------------------- **`ALL ERRORS:`** '
                                 '--------------------------------------------------------')
            await author_dm.send('**`ALERT:`** Just to notify that you have an important message')
            await author_dm.send('**`ERROR 001:`** for bot shutdown messages')
            await author_dm.send('**`ERROR 002:`** Failure to send messages')
            await author_dm.send('**`ERROR 003:`** Irregular usage of $emergency_lockdown')
            await author_dm.send('**`ERROR ???:`** Unknown error')
            await author_dm.send('**`MISC ERRORS:`**')
            await author_dm.send('**`MISCERROR 001:`** Took too long to respond ')
            time.sleep(0.7)
            # SEPARATOR BETWEEN ERRORS AND WARNINGS
            await author_dm.send('\n-------------------------------------------------------- **`ALL WARNINGS:`** '
                                 '--------------------------------------------------------')
            await author_dm.send('**`WARNING 001:`** Irregular usage of $draw')
            await author_dm.send('**`WARNING 002:`** Notification when Member uses $emergency_lockdown')
            await author_dm.send('**`WARNING 003:`** Author used Incomplete Commands')
            await author_dm.send('**`WARNING 004:`** Bot latency too high')
            await author_dm.send('**`WARNING 005:`** Someone has used a forbidden word')
            time.sleep(0.7)
            # SEPARATOR BETWEEN WARNINGS AND PYTHON ERRORS
            await author_dm.send('**`PYTHONERROR 1431:`** Speech Recognition Errors')

    @commands.command(help=no_help_error_message, brief="- used for setting debug to True or False")
    @commands.has_any_role('MODERATOR', 'Trusted', 'Co-manager', 'Administrator', 'CEO')
    async def set_debug(self, ctx, boolean):
        # FIXME: Not working. Please fix.
        global debug, going_to_run_debug
        role = discord.utils.find(lambda r: r.name == 'Trusted', ctx.guild.roles)
        roles = ctx.author.roles
        if not shutdown and not beta_mode:
            if boolean.lower() == 'true':
                # configure.set('debug info', 'debug', True) <-- not in use
                time.sleep(1)
                debug = True
                going_to_run_debug = True
                await ctx.send('Set debug to True')
            elif boolean.lower() == 'false':
                # configure.set('debug info' ,'debug', False) <-- not in use
                time.sleep(1)
                debug = False
                going_to_run_debug = True
                await ctx.send('Set debug to False')
                # await ctx.send('Oh No! The bot developer has restricted this command!')
            else:
                await ctx.send('**`Unsuccessful:`** Oh No! Looks like something has gone wrong! Try again later.')
        else:
            if shutdown and not beta_mode:
                await ctx.send(bot_shutdown_message)
            if beta_mode and not shutdown:
                if role in roles:
                    if boolean.lower() == 'true':
                        # configure.set('debug info', 'debug', True) <-- not in use
                        time.sleep(1)
                        debug = True
                        going_to_run_debug = True
                        await ctx.send('Set debug to True')
                        # await ctx.send('Oh No! The bot developer has restricted this command!')
                    elif boolean.lower() == 'false':
                        # configure.set('debug info' ,'debug', False) <-- not in use
                        time.sleep(1)
                        debug = False
                        going_to_run_debug = True
                        await ctx.send('Set debug to False')
                        # await ctx.send('Oh No! The bot developer has restricted this command!')
                    else:
                        await ctx.send(
                            '**`Unsuccessful:`** Oh No! Looks like something has gone wrong! Try again later.')
                else:
                    await ctx.send(beta_testing_message)

    # TODO: Finish this
    @commands.command(help=no_help_error_message, brief='- copy and paste code. Duh.')
    async def copy_and_paste_code(self, ctx):
        role = discord.utils.find(lambda r: r.name == 'Trusted', ctx.guild.roles)
        roles = ctx.author.roles
        if not shutdown and not beta_mode:
            await ctx.send('**`Copy and paste stuff:`**')
            await ctx.send("@commands.has_any_role('MODERATOR', 'Trusted', 'Co-manager', 'Administrator', 'CEO')")
        else:
            if not shutdown and beta_mode:
                await ctx.send(bot_shutdown_message)
            if beta_mode and not shutdown:
                if role in roles:
                    await ctx.send('**`Copy and paste stuff:`**')
                    await ctx.send(
                        "@commands.has_any_role('MODERATOR', 'Trusted', 'Co-manager', 'Administrator', 'CEO')")
                else:
                    await ctx.send(beta_testing_message)

    @commands.command(help=no_help_error_message, brief='- yay it works')
    @is_guild_owner()
    async def test_remove_role_thingy(self, ctx):
        if not shutdown and not beta_mode:
            roles = ctx.author.roles  # list of roles, the lowest role starts first
            roles.reverse()  # makes roles list reverse to display the highest roles first
            top_role = roles[0]  # first entry of list
            await ctx.author.remove_roles(top_role)
            await ctx.send('top role removed')
        else:
            if not shutdown and beta_mode:
                await ctx.send(bot_shutdown_message)
            if beta_mode and not shutdown:
                await ctx.send(beta_testing_message)


class OwnerOnly(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help=f"{discord_hyphen_separator} DRAW {discord_hyphen_separator}\n"
                           f"The draw command is used to draw a random person out of all the members of the guild"
                           f"This is usually used for a reward draw, and can only be used by the Guild Owner."
                           f"DM the owner if you have a problem with this.\n"
                           f"{discord_hyphen_separator} EXAMPLE {discord_hyphen_separator}\n"
                           f"**`INPUT:`** $draw\n"
                           f"**`Output:`** Drawing... \nPrints, WARNING 0001: (author) has drawn a person!"
                           f"Did you allow them? \nThe lucky winner is (winner)!\n"
                           f"Choosing random reward...\n"
                           f"(winner) won (random reward)!", brief='- draws a person for #random-draw')
    @is_guild_owner()
    async def draw(self, ctx):
        # FIXME: Fix it so that the bots can't win. I KNOW HOW TO. JUST TOO LAZY.
        # NOTE: IF I SEE ONE PERSON USING THIS...
        role = discord.utils.find(lambda r: r.name == 'Trusted', ctx.guild.roles)
        roles = ctx.author.roles
        if shutdown or not beta_mode:
            people_enter = str(ctx.guild.members)
            rand_reward = ['access to a secret category', 'a random role', 'Discord Dungeons Money',
                           'Villager Bot Money', 'the ability to be immune to slow mode (temporary)',
                           'owner of the server for ? hours', 'Myuu PKC']
            people_choice = random.choice(people_enter)
            reward_choice = random.choice(rand_reward)

            await ctx.send('Drawing...')
            print(f"WARNING 0001: {ctx.author} has drawn a person! Did you allow them?")
            time.sleep(1.3)
            await ctx.send(f"The lucky winner is {people_choice}!")
            time.sleep(0.8)
            await ctx.send("Choosing random reward...")
            time.sleep(random.randint(1, 3))
            await ctx.send(f"{people_choice} won {reward_choice}!")
        if not shutdown and beta_mode:
            await ctx.send(f" **`ERROR 0001:`** {bot_shutdown_message}")
        else:
            if role in roles:
                people_enter = ctx.guild.members
                rand_reward = ['access to a secret category', 'a random role', 'Discord Dungeons Money',
                               'Villager Bot Money', 'the ability to be immune to slow mode (temporary)',
                               'owner of the server for ? hours', 'Myuu PKC']
                people_choice = random.choice(people_enter)
                reward_choice = random.choice(rand_reward)

                await ctx.send('Drawing...')
                print(f"WARNING 0001: {ctx.author} has drawn a person! Did you allow them?")
                time.sleep(1.3)
                await ctx.send(f"The lucky winner is {people_choice}!")
                time.sleep(0.8)
                await ctx.send("Choosing random reward...")
                time.sleep(random.randint(1, 3))
                await ctx.send(f"{people_choice} won {reward_choice}!")
            else:
                await ctx.send(beta_testing_message)

    @commands.command(help=f"{discord_hyphen_separator} LOAD_COG {discord_hyphen_separator}\n"
                           f"The load_cog command is one of the most essential commands for loading specific modules."
                           f"You can use it to load a specific cog, like cogs.ExtraCommands. If there is an error,"
                           f"it will give you the error so that you can debug it.\n"
                           f"{discord_hyphen_separator} EXAMPLE {discord_hyphen_separator}\n"
                           f"**`INPUT:`** $draw (specific .py script that is in ./cogs)\n"
                           f"**`OUTPUT:`**\n"
                           f"(IF SUCCESS): Load Cog, message (Successfully imported (cog))\n"
                           f"(IF FAIL): message (ERROR: (error msg))", brief='- command which loads a module.')
    @is_guild_owner()
    async def load_cog(self, ctx, *, cog: str):
        role = discord.utils.find(lambda r: r.name == 'Trusted', ctx.guild.roles)
        roles = ctx.author.roles
        if not shutdown and not beta_mode:
            try:
                self.bot.load_extension(cog)
            except Exception as e:
                await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
            else:
                await ctx.send(f"**`SUCCESS:`** Successfully imported {cog}")
        if not shutdown and beta_mode:
            await ctx.send(f" **`ERROR 0001:`** {bot_shutdown_message}")
        else:
            if role in roles:
                try:
                    self.bot.load_extension(cog)
                except Exception as e:
                    await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
                else:
                    await ctx.send(f"**`SUCCESS:`** Successfully imported {cog}")
            else:
                await ctx.send(beta_testing_message)

    @commands.command(help=no_help_simple_message, brief='- command that unloads a module')
    @is_guild_owner()
    async def unload_cog(self, ctx, *, cog: str):
        if not shutdown:

            try:
                if cog != 'cogs.BuiltInCogs':
                    self.bot.unload_extension(cog)
                else:
                    await ctx.send('**`ERROR:`** You cannot unload BuiltInCogs')
            except Exception as e:
                await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
            else:
                if cog != 'cogs.BuiltInCogs':
                    await ctx.send(f"**`SUCCESS:`** Successfully unloaded {cog}")
                else:
                    pass
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(help=no_help_simple_message, brief='- command that reloads a module')
    @is_guild_owner()
    async def reload_cog(self, ctx, *, cog: str):
        if not shutdown:

            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except Exception as e:
                await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            else:
                await ctx.send(f"**`SUCCESS:`** Successfully reloaded {cog}")
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(help=f"{discord_hyphen_separator} LOAD_ALL_COGS {discord_hyphen_separator}\n"
                           f"The load_all_cogs is kind of like load_cog, but it loads all cogs."
                           f"This allows for faster loading if you want to load a bunch of modules."
                           f"Plus, load_all_cogs is just easier to type (JK)\n"
                           f"{discord_hyphen_separator} EXAMPLE {discord_hyphen_separator}\n"
                           f"**`INPUT:`** $load_all_cogs\n"
                           f"**`OUTPUT:`** \n"
                           f"(IF SUCCESS): Load all cogs, message (Successfully loaded all cogs)\n"
                           f"(IF FAIL): message (ERROR: (Error Msg)", brief='- command that loads all modules')
    @is_guild_owner()
    async def load_all_cogs(self, ctx):
        # TODO: Make this better
        if not shutdown:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    try:
                        self.bot.load_extension(f"cogs.{filename[:-3]}")
                    except Exception as e:
                        await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
                        # await ctx.send(f"**`ERROR:`** {e}") NOTE: If want Full Error, uncomment this out.
                    else:
                        await ctx.send(f'**`SUCCESS:`** Successfully loaded cogs.{filename[:-3]}')

    @commands.command(help='COMING SOON!', brief='- command that unloads all modules')
    @is_guild_owner()
    async def unload_all_cogs(self, ctx):
        # TODO: Make this better
        if not shutdown:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    try:
                        if filename != 'BuiltInCogs.py':
                            self.bot.unload_extension(f"cogs.{filename[:-3]}")
                    except Exception as e:
                        await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
                    else:
                        if filename != 'BuiltInCogs.py':
                            await ctx.send(f'**`SUCCESS:`** Successfully unloaded cogs.{filename[:-3]}')
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(help='COMING SOON!', brief='- command that reloads all modules')
    @is_guild_owner()
    async def reload_all_cogs(self, ctx):
        # TODO: Make this better
        if not shutdown:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    try:
                        if filename != 'BuiltInCogs.py':
                            self.bot.unload_extension(f"cogs.{filename[:-3]}")
                            self.bot.load_extension(f"cogs.{filename[:-3]}")
                    except Exception as e:
                        await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
                    else:
                        if filename != 'BuiltInCogs.py':
                            await ctx.send(f'**`SUCCESS:`** Successfully reloaded cogs.{filename[:-3]}')
        else:
            await ctx.send(bot_shutdown_message)


class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['8ball', 'eightball'],
                      help=f"{discord_hyphen_separator} 8BALL {discord_hyphen_separator}\n"
                           f"This fun command is used to pick a random answer for your question you asked."
                           f"It will answer either yes, no, or maybe (it chooses yes the most)\n"
                           f"P.S I don't like people who uses this command.\n"
                           f"{discord_hyphen_separator} EXAMPLE {discord_hyphen_separator}\n"
                           f"**`INPUT:`** $8ball (question)\n"
                           f"**`OUTPUT:`** Question:(question). Answer:(answer)",
                      brief='- fun command that possesses the power of 8')
    async def _8ball(self, ctx, *, question):
        """- fun command that possesses the power of 8"""
        if not shutdown:
            answers = ['It is certain.', 'It is decidedly so.',
                       'without a doubt.', 'Yes - definitely.',
                       'You may rely on it.', 'As I see it, yes.',
                       'Most likely.', 'Outlook good.',
                       'Yes.', 'Signs point to yes.',
                       'Reply hazy, try again', 'Ask again later.',
                       'Better not tell you now.', 'Cannot predict now.',
                       'Concentrate and ask again.', 'Don\'t count on it.',
                       'My reply is no.', 'My sources say no.',
                       'Outlook not so good.', 'Very doubtful.',
                       'Signs point to no.', 'The answer is no.']
            time.sleep(0.6)
            await ctx.send(f"Question: {question}\nAnswer: {random.choice(answers)}")
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(aliases=['roll'], help='rolls a dice. Very simple.', brief='- fun command that rolls a dice for '
                                                                                 'you')
    async def dice(self, ctx):
        if not shutdown:
            await ctx.send(f"You get {random.randint(1, 6)}.")
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(help=no_help_simple_message, brief='- fun command that chooses a random number you specify')
    async def randnum(self, ctx, a: int, b: int):
        if not shutdown:
            await ctx.send(f"The random number is {random.randint(a, b)}")
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(help=no_help_simple_message, brief='- fun command that chooses outcomes that you specify')
    async def choice(self, ctx, *choices):
        if not shutdown:
            await ctx.send(f"The random outcome is {random.choice(choices)}")
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(help="Flips a coin. It's that easy.", brief='- fun command that flips a coin')
    async def coinflip(self, ctx):
        if not shutdown:
            await ctx.send('Flipping a coin...')
            flip_side = random.randint(0, 1)
            if flip_side == 0:
                await ctx.send('It is...')
                time.sleep(random.random())
                await ctx.send('Heads!')
            else:
                await ctx.send('It is...')
                time.sleep(random.random())
                await ctx.send('Tails!')
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(help=f"{discord_hyphen_separator} GUESS {discord_hyphen_separator}\n"
                           f"This command lets you play a fun, but boring guessing game. "
                           f"Just guess the number, and you WIN! A downside is that this is SO outdated, that"
                           f"the developer doesn't even want to update it."
                           f"Feel free to contact me if you want more game  stuff!\n"
                           f"{discord_hyphen_separator} EXAMPLE {discord_hyphen_separator}\n"
                           f"**`INPUT:`** $guess\n"
                           f"**`OUTPUT:`**\n"
                           f"Bot: I am guessing a number between 1 and 10. What number is it?\n"
                           f"You: (chooses number)\n"
                           f"IF take > 5 seconds, abort command.\n"
                           f"ELSE, (check if answer is right)\n"
                           f"IF (answer is right), Bot say: You are right!\n"
                           f"IF (answer is wrong), Bot say: You is the worst at guessing. It is actually (number).",
                      brief='- fun guessing game')
    async def guess(self, ctx):
        # IDEA: Add extra guesses.
        def is_correct(author_check):
            return author_check.author == ctx.author and author_check.content.isdigit()

        answer = random.randint(1, 10)
        await ctx.send('I am guessing a number between 1 and 10. What number is it?')
        try:
            guess = await self.bot.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await ctx.send('Sorry, you took too long. It was {}.'.format(answer))

        if int(guess.content) == answer:
            await ctx.send('You are right!')
        else:
            await ctx.send('You is the worst at guessing. It is actually {}.'.format(answer))


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help=no_help_simple_message, brief='- adds. Pretty self-explanatory')
    async def add(self, ctx, x: int, y: int):
        if not shutdown:
            await ctx.send(f"The sum of {x} and {y} is {x + y}")
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(help=no_help_simple_message, brief='- subtracts. Pretty self-explanatory')
    async def subtract(self, ctx, x: int, y: int):
        if not shutdown:
            await ctx.send(f"The difference of {x} and {y} is {x - y}")
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(help=no_help_simple_message, brief='- multiplies. Pretty self-explanatory')
    async def multiply(self, ctx, x: int, y: int):
        if not shutdown:
            await ctx.send(f"The product of {x} and {y} is {x * y}")
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(help=no_help_simple_message, brief='- divides. Pretty self-explanatory')
    async def divide(self, ctx, x: int, y: int):
        if not shutdown:
            await ctx.send(f"The quotient of {x} and {y} is {x / y}")
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(help=no_help_simple_message, brief='- takes the exponents of x and y')
    async def exponent(self, ctx, x: int, y: int):
        if not shutdown:
            await ctx.send(f"The exponent of {x} and {y} is {x ** y}")
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(help=no_help_simple_message, brief='- takes the square root of x')
    async def sqrt(self, ctx, x: int):
        if not shutdown:
            await ctx.send(f"The square root of {x} is about {round(m.sqrt(x), 3)}")
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(help=no_help_simple_message, brief='- takes the square of x')
    async def square(self, ctx, x: int):
        if not shutdown:
            await ctx.send(f"The square of {x} is about {x ** 2}")
        else:
            await ctx.send(bot_shutdown_message)

    @exponent.error
    async def exponent_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Sorry. This function does not allow decimals")


class ModeratorCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help=f"{discord_hyphen_separator} EMERGENCY_LOCKDOWN {discord_hyphen_separator}\n"
                           f"This command is made so that the moderators can handle discord raids."
                           f"This works by getting everyone in the server, removing all their roles, and "
                           f"replacing them with the BANNED role. Because the BANNED role has no permissions, "
                           f"your discord server is safe of raids.\n"
                           f"NOTE: After verifying that you want to do this, THERE IS NO GOING BACK. Sorry.\n"
                           f"{discord_hyphen_separator} EXAMPLE {discord_hyphen_separator}\n"
                           f"**`INPUT:`** $emergency_lockdown\n"
                           f"**`OUTPUT:`**\n"
                           f"Bot: **`WARNING 002:`** Are you SURE you want to ......\n"
                           f"You: (If want to lock say yes. Otherwise, wait for 5 seconds)\n"
                           f"Bot: (plays alarm sound to owner, then starts initializing lockdown sequence)\n"
                           f"Bot: (Lockdowns the server and sends personalized message))",
                      brief='- DO NOT USE THIS. If we see you doing this, there will be consequences.')
    @is_guild_owner()
    # NOTE: There are few things to fix. 1. Make initialization easier by adding user to say "no".
    # NOTE: 2. make the try statement, and the playsound run at the same time.
    async def emergency_lockdown(self, ctx):
        global shutdown
        global beta_mode

        def check(author_check):
            return author_check.content == 'yes'

        if not shutdown and not beta_mode:
            brandon = self.bot.get_user(683852333293109269)
            author = ctx.author

            await ctx.send(
                "**`WARNING 002:`** Are you SURE you want to lockdown the server? This is a pretty big deal.")
            await brandon.send(f"**`WARNING 002:`** {author} is going to lockdown the server! Did you let him?")
            print(f"WARNING 002: {ctx.author} is going to shutdown the server. Did you let him?", file=sys.stderr)

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=5)
            except asyncio.TimeoutError:
                await ctx.send('**`MISCERROR 001:`** Sorry! You took too long! Come back later.')
            else:
                await ctx.send(f"Sending alarm sound to owner...")
                playsound(
                    r"C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community Bot\Misc things "
                    r"for Community Bot\Alarm Sound 1.mp3")

                await ctx.send('Locking down server...'.format(msg))
                await brandon.send(f"**`ALERT:`** {author} has shut down the server!")
                guild_members = ctx.guild.members
                guild_members.reverse()
                estimated_time = len(guild_members) * 3
                await ctx.send(f"ESTIMATED TIME: {estimated_time}")
                time.sleep(3)

                for member in guild_members:
                    # if str(member).split() not in ['Carl-bot#1536', 'Test Bot-Community edition#9493', 'BoxBot#7194',
                    # 'Villager Bot#6423', 'Myuu#9942', 'DiscordRPG#0366', 'Statbot#3472', 'TriviaBot#7948']:
                    if not member.bot:
                        roles = member.roles
                        roles.reverse()
                        for role in roles:
                            try:
                                await member.remove_roles(role)
                            except:
                                pass
                        banned_role = discord.utils.get(ctx.author.guild.roles, name="BANNED")
                        await member.add_roles(banned_role)
                        await member.send(f"{ctx.author.name} just locked the server!")

                await ctx.send('Finished banning people!')

            if shutdown and not beta_mode:
                await ctx.send(f" **`ERROR 0001:`** {bot_shutdown_message}")
            else:
                await ctx.send(f"You dare try to use this command, {ctx.author}? I'm telling THE OWNER.")

    # FIXME: FIX THIS DARN THING
    @commands.command(help=no_help_error_message, brief='- give back normal roles to everyone')
    @is_guild_owner()
    async def giverole_lockdown(self, ctx):
        if not shutdown and not beta_mode:
            """daniel_m = await self.bot.get_user(622179028069122068)
            daniel_c = await self.bot.get_user(697487963545927696)
            anna_a = await self.bot.get_user(541402251202134035)
            aidan_c = await self.bot.get_user(683864011959435380)
            robert_b = await self.bot.get_user(724986646382116946)
            garrick_w = await self.bot.get_user(745997390116421679)
            lucas_j = await self.bot.get_user(694667608557092894)
            tom_l = await self.bot.get_user(740682401700774018)
            jason_m = await self.bot.get_user(682717716507000865)
            test_acc = await self.bot.get_user(728361350878855229)
            for member in ctx.guild.members:
                if str(member).strip() == daniel_m.name:
                    await ctx.send('dm')
                if str(member).strip() == daniel_c.name:
                    await ctx.send('dc')"""
            await ctx.send('Sorry! Work in Progress! We\'ll notify you when we fix it!')
            brandon = self.bot.get_user(683852333293109269)
            # TODO: Finish this
            await brandon.send(f"**`WARNING 003:` {ctx.author.name} has used an INCOMPLETE command. Uh Oh!")

    @commands.command(help=no_help_simple_message, brief='- Notifies everyone in the server with a message')
    @commands.has_role(695312034627059763)  # This is MODERATOR
    async def message_all(self, ctx, *, message):
        brandon = self.bot.get_user(683852333293109269)
        await ctx.send('Sending Message...')
        for member in ctx.guild.members:
            if not member.bot and str(member).strip() != 'Mr. Code#0194':
                await member.send(f"--------------- **`INCOMING MESSAGE`** from {ctx.author.name} ---------------")
                time.sleep(1)
                try:
                    await member.send(message)
                    await brandon.send(f"**`SUCCESS:`** Successfully sent message to {member.name}")
                except:
                    await brandon.send(f"**`ERROR 002:`** Failed to send message to {member.name}")

    @commands.command(help=no_help_simple_message, brief='- messages the server owner')
    @commands.has_role(695757699161260104)  # This is GEMBER
    async def message_owner(self, ctx, *, message):
        # brandon = self.bot.get_user(683852333293109269)
        owner = self.bot.get_user(ctx.guild.owner_id)
        author = self.bot.get_user(ctx.author.id)
        await ctx.send('Sending Message...')
        try:
            await owner.send(f"--------------- **`INCOMING MESSAGE`** from {ctx.author.name} ---------------")
            await owner.send(message)
        except:
            await author.send(f"**`ERROR 002:`** Failed to send message to {owner.name}")
        else:
            await author.send(f"**`SUCCESS:`** Successfully sent message to {owner.name}")

    """@emergency_lockdown.error
    async def emergency_lockdown_handler(self, ctx, error):
        if isinstance(error, discord.ext.commands.CheckFailure):
            brandon = self.bot.get_user(683852333293109269)
            await ctx.send(f"You dare try to use this command, {ctx.author.mention}? I'm telling THE OWNER.")
            await brandon.send(f"**`ERROR 003:`**{ctx.author} is trying to use the EMERGENCY LOCKDOWN command.")
            time.sleep(0.9)
            await ctx.send('P.S. You are getting a consequence.')
            roles = ctx.author.roles
            roles.reverse()
            for role in roles:
                try:
                    await ctx.author.remove_roles(role)
                except:
                    pass
            banned_role = discord.utils.get(ctx.author.guild.roles, name="BANNED")
            await ctx.author.add_roles(banned_role)
        else:
            await ctx.send('AHA JUST WHAT I THOUGHT IT IS')"""


class MiscellaneousCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help=f"{discord_hyphen_separator} RULES {discord_hyphen_separator}\n"
                           f"This command just sends a list of rules, the EXACT ones from $rules."
                           f"Beware that this will take some time, because the Discord API is not always reliable.\n"
                           f"{discord_hyphen_separator} EXAMPLE {discord_hyphen_separator}\n"
                           f"**`INPUT:`** $rules\n"
                           f"**`OUTPUT:`** Bot: (sends rules one by one)", brief='- Shows the rules')
    async def rules(self, ctx):
        if not shutdown:
            await ctx.send("Rules:")
            await ctx.send("1. Do not use inappropriate or vulgar language. Do so and you will be banned.")
            await ctx.send("2. Do not exploit people for resources, such as Discord Dungeons Money, Villager Bot "
                           "Money, etc.")
            await ctx.send("3. Never spam TTS messages. Doing so will bet you banned.")
            await ctx.send("4. Do not spam, period. Exception lies in the #spam channel, but even there, slow mode is "
                           "on.")
            await ctx.send("5. Obey the Moderators. They are moderators for a reason.")
            await ctx.send("6. USE COMMON SENSE.")
            await ctx.send("7. When accessing rewards, do not use the rewards to abuse each other for any reason. "
                           "Doing so will get you banned and possibly reported")
            await ctx.send("8. Do not create a discord raid. We have defenses against it.")
            await ctx.send("9th and last one. This server is for getting to know each other. "
                           "Being rude/imprudent will get you kicked.")
            await ctx.send("You're Welcome!")
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(help=no_help_simple_message, brief='- Clears messages, Require Manage Messages')
    @commands.has_permissions(manage_messages=True)
    # @commands.has_any_role('MODERATOR', 'Trusted', 'Co-manager', 'Administrator', 'CEO')
    # MinorNote: Uncomment above line to restrict access to most people
    async def clear(self, ctx, amount: int):
        if not shutdown:
            aidan = self.bot.get_user(683864011959435380)
            # MinorNote: Comment below and remove tabs to make aidan actually able to do that
            if str(ctx.author.name).strip() != aidan.name:
                roles = ctx.author.roles
                roles.reverse()
                # top_role = roles[0]
                # if top_role.id >= 730159564078448660: # this is flawed because discord message id is kinda weird.
                # else:
                # await ctx.send('OOF! You do not have a high enough role!')
                await ctx.channel.purge(limit=amount)
            else:
                await ctx.send('You are Mlem, so therefore you can\'t use this')
        else:
            await ctx.send(bot_shutdown_message)

    @commands.command(help='COMING SOON!', brief='- shows all the cogs in the cogs folder')
    @commands.has_any_role('Trusted', 'MODERATOR', 'Co-manager', 'Das Dictator')
    async def cogs(self, ctx):
        await ctx.send('**`Cogs:`**')
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await ctx.send(f"cogs.{filename[:-3]}")

    @commands.command(help='COMING SOON!', brief='- gives some important files in the format of a .txt')
    async def files(self, ctx):
        await ctx.send('------------------------------ **`CHANGELOGS `** ------------------------------')
        await ctx.send(file=discord.File(r"C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord "
                                         r"Code\Community Bot\cogs\community_bot_changelog.txt"))
        await ctx.send(file=discord.File(r"C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord "
                                         r"Code\Community Bot\cogs\Doc\BuiltInCogs_doc.txt"))

    @commands.command(help='COMING SOON!', brief='- a command that has commands inside it :o')
    async def bot(self, ctx, parameters=None):
        brandon = self.bot.get_user(683852333293109269)
        if parameters is not None:
            if str(parameters).lower() == '-v':
                await ctx.send(f"**`VERSION:`** {version}")
            elif str(parameters).lower() == '-i':
                mod_time = os.path.getmtime(r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord '
                                            r'Code\Community Bot')
                list_of_num_chars = []
                only_files_cog = [f for f in os.listdir(r"C:\Users\Admin\AppData\Local\Programs\Python\Python38"
                                                        r"\Discord Code\Community Bot\cogs") if os.path.isfile(
                    os.path.join(r"C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community "
                                 r"Bot\cogs", f))]
                only_files_comm = [f for f in os.listdir(r"C:\Users\Admin\AppData\Local\Programs\Python\Python38"
                                                         r"\Discord Code\Community Bot") if os.path.isfile(
                    os.path.join(r"C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community "
                                 r"Bot", f))]

                for file_cog in only_files_cog:
                    the_file_cog = open(
                        rf"C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord "
                        rf"Code\Community Bot\cogs\{file_cog}")
                    the_file_cog_data = the_file_cog.read()
                    num_characters_cog = len(the_file_cog_data)
                    list_of_num_chars.append(num_characters_cog)
                for file_comm in only_files_comm:
                    the_file_comm = open(rf"C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord "
                                         rf"Code\Community Bot\{file_comm}")
                    the_file_comm_data = the_file_comm.read()
                    num_characters_comm = len(the_file_comm_data)
                    list_of_num_chars.append(num_characters_comm)
                await ctx.send(f"{discord_hyphen_separator} **`INFO`** {discord_hyphen_separator}\n"
                               f"**`VERSION:`** {version}\n"
                               f"**`OWNER OF BOT:`** {brandon.name}\n"
                               f"**`LAST MODIFIED:`** {datetime.datetime.fromtimestamp(mod_time).strftime('%a %b %d %Y, %I:%M:%S %p')}\n"
                               f"**`NUMBER OF CHARACTERS:`** {sum(list_of_num_chars)}")
            elif str(parameters).lower() == '--help':
                await ctx.send(f"COMING SOON!")
        else:
            await ctx.send(f"COMING SOON!")

    @clear.error
    async def clear_handler(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the manage message permission.')


def setup(bot):
    # NOTE: This is VERY important. DO NOT mess with this.
    bot.add_cog(DebugAndEvents(bot))
    bot.add_cog(OwnerOnly(bot))
    bot.add_cog(FunCommands(bot))
    bot.add_cog(Math(bot))
    bot.add_cog(MiscellaneousCommands(bot))
    bot.add_cog(ModeratorCommands(bot))
