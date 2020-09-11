from discord.ext import commands
import discord
import time


class MemberPermissionCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def is_guild_owner():
        def predicate(ctx):
            return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
        return commands.check(predicate)

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """- bans someone"""
        roles = ctx.author.roles
        roles.reverse()
        top_role = roles[0]
        if top_role.id >= 730159564078448660:
            # if 730159564078448660 in roles:
            await member.ban(reason=reason)
            await ctx.send(f"banned {member.mention} for {reason}")
            banned_user = self.bot.get_user(member.id)
            await banned_user.send(f"Oh No! {ctx.author.mention} has banned you for {reason}!")

    @commands.command()
    @commands.has_role(695312034627059763)# this role is MODERATOR
    async def unban(self, ctx, *, member):
        """- unbans someone """
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.mention}")
                return

    @commands.command()
    @is_guild_owner()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """- kicks someone"""
        await member.ban(reason=reason)
        await ctx.send(f"kicked {member.mention} for {reason}")

    @commands.command()
    async def giverole(self, ctx, user: discord.Member, role: discord.Role):
        await ctx.send(f"Attempting to add {role.mention} to {user.mention}...")
        time.sleep(0.4)
        await user.add_roles(role)

    @commands.command()
    @commands.has_role(695312034627059763)# this role is MODERATOR
    async def banrole(self, ctx, user: discord.Member):
        await ctx.send(f"Attempting to ban {user.mention}...")
        author_roles = ctx.author.roles
        ban_roles = user.roles

        for ban_role in ban_roles:
            try:
                await user.remove_roles(ban_role)
            except:
                pass
        BANNED_role = discord.utils.get(ctx.author.guild.roles, name="BANNED")
        await user.add_roles(BANNED_role)

    @giverole.error
    async def giverole_handler(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('You cannot give someone a higher role than your social hierarchy level')
        elif isinstance(error, commands.MissingRole):
            await ctx.send('Sorry. You need to be above the TRUSTED role in the social hierarchy level')
        else:
            await ctx.send('**`SUCCESS`**')

    """@ban.error
    async def ban_handler(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry. You do not have the required permission to ban someone')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('You cannot ban someone higher than you on the social hierarchy')"""

    @kick.error
    async def kick_handler(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry. You do not have the required permission to kick someone')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('You cannot kick someone higher than you on the social hierarchy')


def setup(bot):
    bot.add_cog(MemberPermissionCommands(bot))
