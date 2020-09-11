import discord
from discord.ext import commands  # Imports discord extensions.

# NOTE: The below code verifies the "client".
bot = commands.Bot(command_prefix='$')


def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)


# NOTE: EMERGENCY CMD
@bot.command()
async def load(ctx, extension):
    """- loads a module. Use in case of emergency"""
    bot.load_extension(f"cogs.{extension}")


@bot.command()
async def unload(ctx, extension):
    """- unloads a module. Use in case of emergency"""
    bot.unload_extension(f"cogs.{extension}")


@bot.command()
async def changestatus(ctx, status):
    """- changes the bot status"""
    if status.lower() == 'invisible':
        await bot.change_presence(status=discord.Status.invisible)
        await ctx.send('Bot status set to invisible')
    elif status.lower() == 'online':
        await bot.change_presence(status=discord.Status.online)
        await ctx.send('Bot status set to online')
    elif status.lower() == 'dnd' or status.lower() == 'do_not_disturb':
        await bot.change_presence(status=discord.Status.dnd)
        await ctx.send('Bot status set to do not disturb')
    elif status.lower() == 'idle':
        await bot.change_presence(status=discord.Status.idle)
        await ctx.send('Bot status set to idle')

# @bot.command()
# async def commands(ctx, request):
#     if request == 'load':
#         await ctx.send('```Load\nThis commmand loads a cog. \n\nExample: (pref)load cogs.(cog name)') 

# for filename in os.listdir('./cogs'):
#    if filename.endswith('.py'):
#        bot.load_extension(f"cogs.{filename[:-3]}")

bot.load_extension('cogs.BuiltInCogs')

# NOTE: runs this program. VERY IMPORTANT FOR MEEEE.
# UPDATE: If possible, will deprecate this and switch to Brandon Owned Bot
# bot.run('OLD TOKEN') # NOTE Aidan's BOT

bot.run('YOUR TOKEN HERE')
