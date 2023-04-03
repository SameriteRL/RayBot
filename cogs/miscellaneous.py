import discord
from discord.ext import commands
from globals import *
import datetime as dt
import random

class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    ### PING ###
    @commands.hybrid_command(description="Get the latency between your client and Discord!",
                             aliases=["latency"])
    async def ping(self, ctx):
        # Retrieves the server latency in milliseconds
        embedVar = discord.Embed(title="Pong!",
                                 description=f"Your message was recieved in {round(self.bot.latency * 1000)}ms.",
                                 color=0x00C500,
                                 timestamp=dt.datetime.now())
        if ctx.author.nick != None: invoker_name = ctx.author.nick
        else: invoker_name = ctx.author.name
        embedVar.set_footer(text=f"\u200bPing checked by {invoker_name}")
        await ctx.send(embed=embedVar)
    
    @ping.error
    async def ping_error(self, ctx):
        await sendDefaultError(ctx)
    
    ### AVATAR ###
    @commands.hybrid_command(description="Get the avatar of any user!",
                             aliases=["pfp, picture"])
    async def avatar(self, ctx, member:discord.Member=None):
        if (member == None):
            await ctx.send(ctx.author.display_avatar)
        else:
            await ctx.send(member.display_avatar)
    
    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed_var = discord.Embed(title=ERROR_TITLE,
                                      description=BAD_MEMBER_MSG,
                                      color=0xC80000)
            await ctx.send(embed=embed_var)
        else:
            await sendDefaultError(ctx)

    ### COINFLIP ###
    @commands.hybrid_command(description="Flip a coin!",
                             aliases=["flipcoin", "coin"])
    async def coinflip(self, ctx):
        # Calls a random float between 0 and 0.99 inclusive. Returns heads if 0 - 0.48 and tails if 0.49 - 0.99
        result = "Heads!" if random.randint(0, 1) == 0 else "Tails!"
        embedVar = discord.Embed(title="Flipping a coin...",
                                 description=f"{result}",
                                 color=0x00C500)
        await ctx.send(embed=embedVar)
    
    @coinflip.error
    async def coinflip_error(self, ctx):
        await sendDefaultError(ctx)

    ### REPO ###
    @commands.hybrid_command(description="Check out my GitHub repository!",
                             aliases=["repository"])
    async def repo(self, ctx):
        embedVar = discord.Embed(title=f"Click here to visit the {ctx.guild.get_member(980203562485317652).name} repository!",
                                 url='https://github.com/SameriteRL/RayBot-2',
                                 color=0x0099FF)
        await ctx.send(embed=embedVar)
    
    @repo.error
    async def repo_error(self, ctx):
        await sendDefaultError(ctx)

async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))