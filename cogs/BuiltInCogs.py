# NOTE: BuiltInCogs.py is the Built In Cog. Pretty self-explanatory.
"""
BuiltInCogs.py is the Built In Cog, as seen above. It is automatically loaded when you run community_bot.py.
Without it, the bot would be severely crippled, and there would be no functionality.
BuiltInCogs.py is made up of SEVEN different classes, which are:
    - DebugAndEvents. This class contains all the events for the bot, as well as some commands to debug the bot.
    - OwnerOnly. This class can only be used by the server/guild owner. Pretty self-explanatory.
    - FunCommands. This  class is mostly used by P E A S E N T S, which contains several fun commands.
    - MathCommands. This class contains some basic arithmetic operations, and if you want more cmds, import MoreMathCommands.
    - ModeratorCommands. This class contains some very useful commands for the moderators of your discord server.
    - MiscellaneousCommands. This class contains miscellaneous commands. WOW!
    - Tasks. This class has some core tasks, like the audit log updater, as well as some tasks-related functions.

I won't go into details about this, because then it would be way too long, to find out more, go to BuiltInCogs_doc.txt.
made with ♥ with discord.py.
"""

# NOTE: Modules that I barely use
import random
import time
import os

from configparser import ConfigParser
from playsound import playsound
import sys

# NOTE: Modules that I kinda use
import asyncio
import math as m
import datetime
import logging
import json
import contextlib
from win10toast import ToastNotifier
# from threading import Thread

# NOTE: THE HOLY DISCORD PACKAGES
from discord.ext import commands, tasks
import discord

logging.basicConfig(level=logging.WARNING, format="On %(asctime)s: %(levelname)s: %(message)s", datefmt="%a %b %d %Y, %I:%M:%S %p")
configure = ConfigParser()
toaster = ToastNotifier()
configure.read(r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community '
               r'Bot\cogs\community_bot_info.ini')

# NOTE: BELOW ARE SOME KEY BOOLEANS
debug = True
shutdown = False
going_to_run_debug = True
beta_mode = False
stop_roles_update = False

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

welcome_message = "Welcome to the **`community`** server! This is where we hang out, end relationships, and much more!\nDon't feel like " \
                  "you belong anywhere? Well, you can check out our MANY channels (we just have too much).\nWanna talk about your " \
                  "**`NEW`** favorite game, but you want to hear our beautiful voices? Check out our VOICE CHANNELS??!?!??!\n" \
                  "Finally, want to escape reality, and go play some text-based games? We got you covered! With our many bots, " \
                  "you'll be able to play a wide variety of games, like Pokemon and Villager Bot (?)\n" \
                  "In the end, we just want to make you happy, and have fun in the server!\n" \
                  "**Features** in the server include: \n\t" \
                  "- FRIENDS\n\t" \
                  "- VOICE CHATS\n\t" \
                  "- GAMES\n\t" \
                  "- CHANNELS\n\t" \
                  "- AND THE LIST, goes ON. and ON. and ON. and ON."

goodbye_message = "I hope that you've enjoyed your stay here on the community server. We are going to miss you dearly, and we " \
                  "hope to see you again soon. If you want to join back anytime, click the link in the description :)\n" \
                  "LINK: https://discord.gg/d98xydx4Su\n" \
                  "Goodbye, and see you around!\n\t" \
                  "- Sincerely, Brandon Cui, owner of the server"

version = 'v0.5.5.b1'
moderator_secret_password = 'thispassworddoesnotexist99!'
path_to_user_info_json = r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community Bot\cogs\json files\user_info.json'
path_to_audit_log_json = r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community Bot\cogs\json ' \
                         r'files\ignored_audit_log_id.json '

forbidden_words = ['fuck', 'bitch', 'shit', 'gabe itch', 'penis']  # NOTE: Don't mean it sorry!


# test_forbidden_words = ['cheese', 'yum']  MinorNote: Don't like saying them? Use the tests!

# NOTE: BELOW ARE SOME KEY INTEGER VALUES

# TODO: Make all commands following beta mode patterns. POSTPONED
# TODO: Make all help commands have f""" instead of f"". POSTPONED
# FIXME Make all commands that message someone has an `except Exception as e` block. POSTPONED
# TODOURGENT: Learn Requests so that I can fill in that form
# UPDATE: 0.5.1 will include: a lot of stuff, but most definitely include anti-corruption tools.
# UPDATE, not bot related: I will need to check on some server flaws, so......


def is_guild_owner():
    """finds the guild owner of the server"""

    def predicate(ctx):
        """actually returns if the message author, and the guild owner are the same"""
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id

    return commands.check(predicate)


class DebugAndEvents(commands.Cog):
    """
    This is where all the events are stored, like on_message() and on_member_join(). There are also some commands in here that help me
    debug some key aspects (although there is only one so far I use a lot). This is also where the security aspect of the bot goes, like
    anti-corruption and anti-vulgar-language (?). Without this, there would be no automod, no pings, and no automod.
    """

    def __init__(self, bot):
        self.bot = bot
        self.roles_update.start()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        member_id = member.id
        member_user = self.bot.get_user(member_id)
        await member_user.send(welcome_message)
        time.sleep(0.1)
        await member_user.send('Hang on... We gotta add your user ID so that we can punish you based on your number of infractions...')
        with open(path_to_user_info_json) as read_json_file:
            all_infractions = json.load(read_json_file)
            deserialized_infractions = all_infractions['overall infractions']

        temp_dict_of_member_and_no_infraction = {str(member.id): 0}
        deserialized_infractions.update(temp_dict_of_member_and_no_infraction)
        all_infractions['overall infractions'] = deserialized_infractions

        with open(path_to_user_info_json, 'w') as write_json_file:
            json.dump(all_infractions, write_json_file, indent=4)

        read_json_file.close()
        write_json_file.close()

        await member_user.send('Done! Now feel free to explore our wonderful server!')

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        member_id = member.id
        member_user = self.bot.get_user(member_id)
        await member_user.send(goodbye_message)
        await member_user.send('P.S. I\'m not gonna remove ur ID from my bot, cause 99% of the time, ur my friend :)')

    @commands.Cog.listener()
    async def on_error(self, event):
        print(f"Uh oh! Something went wrong. Here's what happened: {event}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        now = datetime.datetime.now()
        if not before.channel and after.channel:
            toaster.show_toast("Voice Channel Update!", f"On {now.strftime('%a %b %d %Y, %I:%M:%S %p')} {str(member)[:-5]} has joined "
                                                        f"voice channel {after.channel}", duration=5,
                               icon_path=r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community '
                                         r'Bot\cogs\img\bot_logo.ico')
        elif before.channel and not after.channel:
            toaster.show_toast("Voice Channel Update!", f"On {now.strftime('%a %b %d %Y, %I:%M:%S %p')}, {str(member)[:-5]} has left "
                                                        f"voice channel {before.channel}", duration=5,
                               icon_path=r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community '
                                         r'Bot\cogs\img\bot_logo.ico')

    """@commands.Cog.listener()
    async def on_message_delete(self, message):
        censored = False
        for forbidden_word in forbidden_words:
            if forbidden_word in message:
                print('Uh Oh! The bot must\'ve picked out a poo poo word, so let\'s CENSOR it.')
                censored = True

        # if not censored:
        print(f"SOMEONE just deleted a message. Here, take a look at this message:\nMESSAGE: {message}")"""

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
            # await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('with Brandon. Duh!'))
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(name='Hunger Games', type=5))
        if not shutdown:
            print(f'The discord bot is now online as {self.bot.user.name}, with user ID {self.bot.user.id}')
        else:
            print('The discord bot is now online, but it is shutdown')

        if not beta_mode:
            print('The discord bot is available to anyone')
        else:
            print('The discord bot is now in beta mode. This means that only a few people can access it')

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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if not debug:
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

    @commands.Cog.listener()
    async def on_disconnect(self):
        print(f"Uh oh! Something went wrong, because your bot disconnected D:")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 753295703077421066:
            return

        community_server = self.bot.get_guild(683869900850200581)

        for forbidden_word in forbidden_words:
            if (forbidden_word in message.content) and 'nsfw' not in str(message.channel).strip():
                await message.delete()
                brandon = self.bot.get_user(683852333293109269)
                author = self.bot.get_user(message.author.id)
                time_of_profanity = datetime.datetime.fromtimestamp(time.time()).strftime('%a %b %d %Y, %I:%M:%S %p')

                with open(path_to_user_info_json) as read_json_file:
                    all_infractions = json.load(read_json_file)
                    deserialized_infractions = all_infractions['overall infractions']

                if not deserialized_infractions:
                    dict_of_writing_to_json = {}

                    for member in message.guild.members:
                        member_id = str(member.id)
                        temp_dict_of_member_id_and_no_infraction = {member_id: 0}
                        dict_of_writing_to_json.update(temp_dict_of_member_id_and_no_infraction)

                    all_infractions['overall infractions'] = dict_of_writing_to_json

                    with open(path_to_user_info_json, 'w') as write_json_file:
                        json.dump(all_infractions, write_json_file, indent=4)

                    with open(path_to_user_info_json) as read_json_file:
                        all_infractions_refresh = json.load(read_json_file)
                        deserialized_infractions_refresh = all_infractions_refresh['overall infractions']

                    await author.send('You have 1 infraction')
                    deserialized_infractions_refresh[str(message.author.id)] += 1
                    all_infractions_refresh['overall infractions'] = deserialized_infractions_refresh

                    with open(path_to_user_info_json, 'w') as write_json_file:
                        json.dump(deserialized_infractions_refresh, write_json_file, indent=4)

                else:

                    with open(path_to_user_info_json) as read_json_file:
                        all_infractions = json.load(read_json_file)
                        deserialized_infractions = all_infractions['overall infractions']

                    deserialized_infractions[str(message.author.id)] += 1
                    all_infractions['overall infractions'] = deserialized_infractions

                    with open(path_to_user_info_json, 'w') as write_json_file:
                        json.dump(all_infractions, write_json_file, indent=4)

                with open(path_to_user_info_json) as read_json_file:
                    deserialized_infractions = json.load(read_json_file)['overall infractions']

                num_infractions = deserialized_infractions[str(message.author.id)]
                member_object = community_server.get_member(message.author.id)
                banned = discord.utils.get(community_server.roles, id=695698885615812638)

                message_to_send_to_offender = f"**`ALERT:`** The moderator team has been informed that on **`{time_of_profanity}`**" \
                                              f", you have used a forbidden word. You have violated Rule **`1`** and Rule **`9`**" \
                                              f" of Article I, and this will not be tolerated. Your punishment will be put under" \
                                              f" consideration. The minimal punishment is to get muted for 5 minutes," \
                                              f" but your roles will be returned. This is rather serious, and if this continues," \
                                              f" the consequences will be more severe. In the future, please refrain from using" \
                                              f" profanity.\nBest Regards,\n\t- The Mod team\n" \
                                              f"{discord_hyphen_separator} **`INFO`** {discord_hyphen_separator}\n" \
                                              f"Forbidden word used: **`{forbidden_word}`**\n" \
                                              f"Date of profanity: **`{time_of_profanity}`**\n" \
                                              f"Channel of used profanity: **`{str(message.channel).strip()}`**\n" \
                                              f"Number of infractions: **`{num_infractions}`**\n" \
                                              f"Punishment: **`!!!punishment!!!`**"

                with open(path_to_user_info_json) as read_json_file:
                    all_user_info = json.load(read_json_file)
                    roles = all_user_info["roles"][str(message.author.id)]

                for role in member_object.roles:
                    with contextlib.suppress():
                        if role.name != '@everyone':
                            await member_object.remove_roles(role)
                await member_object.add_roles(banned)
                self.roles_update.cancel()

                await brandon.send(f"**`WARNING 005:`** {message.author} has used a forbidden word!\n"
                                   f"Forbidden word used: **`{forbidden_word}`**\n"
                                   f"Date of profanity: **`{time_of_profanity}`**\n"
                                   f"Channel of used profanity: **`{str(message.channel).strip()}`**\n"
                                   f"Number of infractions: **`{num_infractions}`**")

                if num_infractions == 1:
                    await author.send(message_to_send_to_offender.replace('!!!punishment!!!', 'None. This is a warning.'))
                elif num_infractions == 2:
                    await author.send(message_to_send_to_offender.replace('!!!punishment!!!', 'Banrole for two minutes'))
                    await asyncio.sleep(5)
                elif 3 <= num_infractions <= 5:
                    await author.send(message_to_send_to_offender.replace('!!!punishment!!!', 'Banrole for 10-15 minutes'))
                    await asyncio.sleep(600)
                elif 6 <= num_infractions <= 10:
                    await author.send(message_to_send_to_offender.replace('!!!punishment!!!', 'Banrole for 20-45 minutes'))
                    await asyncio.sleep(1200)
                elif 11 <= num_infractions <= 15:
                    await author.send(message_to_send_to_offender.replace('!!!punishment!!!', 'Lose all roles and contact the moderators'))
                elif num_infractions > 15:
                    await author.send(message_to_send_to_offender.replace('!!!punishment!!!', 'Ban'))

                for role_id in roles:
                    with contextlib.suppress():
                        actual_role = discord.utils.get(community_server.roles, id=role_id)
                        if actual_role.name != '@everyone':
                            await member_object.add_roles(actual_role)

                self.roles_update.start()

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

    @commands.command(help=no_help_error_message, brief='- whatever I want to test, IS IN HEREEEE')
    @is_guild_owner()
    async def function_test(self, ctx):
        await ctx.send(welcome_message)
        await ctx.send(goodbye_message)

    @tasks.loop(hours=1)
    async def roles_update(self):
        now = datetime.datetime.now()
        if now.hour <= 22 or now.hour >= 8:
            community_server = self.bot.get_guild(683869900850200581)
            with open(path_to_user_info_json) as read_user_info:
                all_user_info = json.load(read_user_info)

            all_user_info["roles"] = {}
            dict_to_write_to_json = {}
            for member in community_server.members:
                list_of_roles_to_write_to_json = []
                specific_member_role = member.roles
                for role in specific_member_role:
                    list_of_roles_to_write_to_json.append(role.id)
                temporary_dictionary = {str(member.id): list_of_roles_to_write_to_json}
                dict_to_write_to_json.update(temporary_dictionary)

            all_user_info["roles"] = dict_to_write_to_json
            with open(path_to_user_info_json, 'w') as write_user_info:
                json.dump(all_user_info, write_user_info, indent=4)

    @roles_update.before_loop
    async def before_roles_update(self):
        await self.bot.wait_until_ready()


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
        # MinorNote: IF I SEE ONE PERSON USING THIS...
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


class MathCommands(commands.Cog):
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
            return str(author_check.content).lower() == 'yes'

        if not shutdown and not beta_mode:
            brandon = self.bot.get_user(683852333293109269)
            author = ctx.author

            await ctx.send(
                "**`WARNING 002:`** Are you SURE you want to lockdown the server? This is a pretty big deal.")
            await brandon.send(f"**`WARNING 002:`** {author} is going to lockdown the server! Did you let him?")
            print(f"WARNING 002: {ctx.author} is going to shutdown the server. Did you let him?", file=sys.stderr)

            try:
                await self.bot.wait_for('message', check=check, timeout=5)
            except asyncio.TimeoutError:
                await ctx.send('**`MISCERROR 001:`** Sorry! You took too long! Come back later.')
            else:
                await ctx.send(f"Sending alarm sound to owner...")
                playsound(
                    r"C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord Code\Community Bot\Misc things "
                    r"for Community Bot\Alarm Sound 1.mp3")

                await ctx.send('Locking down server...')
                await brandon.send(f"**`ALERT:`** {author} has shut down the server!")
                guild_members = ctx.guild.members
                guild_members.reverse()
                estimated_time = len(guild_members) * 3
                await ctx.send(f"ESTIMATED TIME: {estimated_time}")
                time.sleep(3)

                for member in guild_members:
                    if not member.bot:
                        roles = member.roles
                        roles.reverse()
                        for role in roles:
                            with contextlib.suppress():
                                await member.remove_roles(role)
                        banned_role = discord.utils.get(ctx.author.guild.roles, name="BANNED")
                        await member.add_roles(banned_role)
                        await member.send(f"{ctx.author.name} just locked the server!")

                await ctx.send('Finished banning people!')

            if shutdown and not beta_mode:
                await ctx.send(f" **`ERROR 0001:`** {bot_shutdown_message}")
            else:
                await ctx.send(f"You dare try to use this command, {ctx.author}? I'm telling THE OWNER.")

    # TODOURGENT: Make the roles update thingy, and REMOVE THIS or something...
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

    @commands.command(help=no_help_error_message, brief='sets a channel\'s slow mode to _ seconds')
    @is_guild_owner()
    async def set_slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slow mode delay in this channel to {seconds} seconds!")

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
                await ctx.send('You are Aidan, so therefore you can\'t use this')
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
        await ctx.send(file=discord.File(r"C:\Users\Admin\AppData\Local\Programs\Python\Python38\Discord "
                                         r"Code\Community Bot\cogs\todo_things.txt"))

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


class Tasks(commands.Cog):
    # TODOURGENT: Configure tasks so that this will be able to handle internet errors
    # NOTE: The role update task is in DebugAndEvents because the on_message() automod needs it

    def __init__(self, bot):
        self.bot = bot
        self.audit_log_update.start()

    @commands.command(help='COMING SOON', brief='- turns off the audit log updater')
    @is_guild_owner()
    async def cancel_audit_log_update(self, ctx):
        self.audit_log_update.cancel()
        await ctx.send('Successfully paused the audit log updater.')

    @commands.command(help='COMING SOON', brief='- turns on the audit log updater')
    @is_guild_owner()
    async def start_audit_log_update(self, ctx):
        self.audit_log_update.start()
        await ctx.send('Successfully resumed the audit log updater.')

    @tasks.loop(minutes=1)
    async def audit_log_update(self):
        # TODOURGENT: Figure out how to include 7:30 (what am I saying)
        now = datetime.datetime.now()
        if now.hour <= 22 or now.hour >= 8:
            community_server = self.bot.get_guild(683869900850200581)

            with open(path_to_audit_log_json) as ignore_audit_log_id_file:
                ignore_audit_log_id_list = json.load(ignore_audit_log_id_file)

            async for entry in community_server.audit_logs(limit=40):
                entry_action = entry.action
                entry_user_id = entry.user.id

                if str(entry_action) == 'AuditLogAction.channel_delete' and entry.id not in ignore_audit_log_id_list:
                    discord_user = self.bot.get_user(entry_user_id)
                    await discord_user.send(f"Hello, the owner of the server just wants you to know that you have just deleted a channel. "
                                            f"Because of our auto audit log mechanism, we would like for you to type the secret "
                                            f"moderator password. This is to detect if a non-moderator has been exploiting some server "
                                            f"leaks.\nYou will have three attempts, and must answer within 15 seconds (for each one, of "
                                            f"course). Once you fail, you will be banned using a role, and all moderators will be informed "
                                            f"of your situation. They will decide on your punishment later on.\n"
                                            f"{discord_hyphen_separator} **`INFO`** {discord_hyphen_separator}\n"
                                            f"TIME DETECTED: **`{now.strftime('%a %b %d %Y, %I:%M:%S %p')}`**")
                    failed_tries = 0
                    while failed_tries < 3:
                        try:
                            user_input_mod_password = await self.bot.wait_for("message", timeout=15)
                        except asyncio.TimeoutError:
                            await discord_user.send(f"Ran out of time. You have {3 - failed_tries - 1} tries left.")
                            failed_tries += 1
                        else:
                            if user_input_mod_password.content == moderator_secret_password:
                                await discord_user.send("Correct! Either you are a moderator that knows the password, or you just got "
                                                        "really lucky..")
                                break
                            else:
                                await discord_user.send(f"Incorrect... You have {3 - failed_tries - 1} tries left.")
                                failed_tries += 1

                    if failed_tries == 3:
                        await discord_user.send('Sorry, you have run out of guesses. Contacting moderators and adding punishments...')

                        for member in community_server.members:
                            if member.id == entry_user_id:
                                roles = member.roles
                                roles.reverse()
                                for role in roles:
                                    with contextlib.suppress():
                                        await member.remove_roles(role)
                                banned_role = discord.utils.get(community_server, name="BANNED")
                                await member.add_roles(banned_role)

                    ignore_audit_log_id_list.append(entry.id)

                    with open(path_to_audit_log_json, 'w') as ignore_audit_log_id_file_write:
                        json.dump(ignore_audit_log_id_list, ignore_audit_log_id_file_write, indent=4)

    @audit_log_update.before_loop
    async def before_audit_log_update(self):
        await self.bot.wait_until_ready()


def setup(bot):
    # NOTE: This is VERY important. DO NOT mess with this.
    bot.add_cog(DebugAndEvents(bot))
    bot.add_cog(OwnerOnly(bot))
    bot.add_cog(FunCommands(bot))
    bot.add_cog(MathCommands(bot))
    bot.add_cog(MiscellaneousCommands(bot))
    bot.add_cog(ModeratorCommands(bot))
    bot.add_cog(Tasks(bot))
