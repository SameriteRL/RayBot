import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot

import random
import datetime as dt

from src.globals import *

class Miscellaneous(commands.Cog):

    def __init__(self, bot:Bot):
        self.bot = bot

    ### PING ###
    @commands.hybrid_command(description="Get the latency between your client and Discord!",
                             aliases=["latency"])
    async def ping(self, ctx:Context):
        # Retrieves the server latency in milliseconds
        embed_var = discord.Embed(
            title="Pong!",
            description=f"Your message was recieved in {round(self.bot.latency * 1000)}ms.",
            color=0x00C500,
            timestamp=dt.datetime.now()
        )
        # Determines the name displayed in the embed footer
        if ctx.author.nick != None: invoker_name = ctx.author.nick
        else: invoker_name = ctx.author.name
        embed_var.set_footer(text=f"\u200bPing checked by {invoker_name}")
        # Sends the embed
        await ctx.send(embed=embed_var)
    
    @ping.error
    async def ping_error(self, ctx, error):
        await sendDefaultError(ctx)

    ### COINFLIP ###
    @commands.hybrid_command(description="Flip a coin!",
                             aliases=["flipcoin", "coin"])
    async def coinflip(self, ctx:Context):
        # Calls a random number either 0 or 1 as heads and tails
        result = "Heads!" if random.randint(0, 1) == 0 else "Tails!"
        # Creates and sends an embed
        embed_var = discord.Embed(
            title=result,
            color=0x00C500
        )
        await ctx.send(embed=embed_var)
    
    @coinflip.error
    async def coinflip_error(self, ctx, error):
        await sendDefaultError(ctx)
    
    ### AVATAR ###
    @commands.hybrid_command(description="Get the avatar of any user!",
                             aliases=["pfp, picture"])
    async def avatar(self, ctx:Context, member:discord.Member=None):
        # Sends the command invoker's avatar if no member is specified
        if (member == None):
            avatar_url = ctx.author.display_avatar.url
            target_color = (await self.bot.fetch_user(ctx.author.id)).accent_color
        # Otherwise sends the specified member's avatar
        else:
            avatar_url = member.display_avatar.url
            target_color = (await self.bot.fetch_user(member.id)).accent_color
        embed_var = discord.Embed(
            color=target_color
        )
        embed_var.set_image(url=avatar_url)
        await ctx.send(embed=embed_var)
    
    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed_var = discord.Embed(
                title=ERROR_TITLE,
                description=BAD_MEMBER_MSG,
                color=0xC80000
            )
            await ctx.send(embed=embed_var)
        else:
            await sendDefaultError(ctx)

    ### REPO ###
    @commands.hybrid_command(description="Check out my GitHub repository!",
                             aliases=["repository"])
    async def repo(self, ctx:Context):
        file_var = discord.File("./icon.png", filename="icon.png")
        embed_var = discord.Embed(
            title=f"Click Here to Visit the {ctx.guild.get_member(SELF_ID).name} Repository!",
            # description="A highly experimental Discord bot aimed for general-purpose use.",
            url='https://github.com/SameriteRL/RayBot-2',
            color=0x0099FF
        )
        # embed_var.set_thumbnail(url="attachment://icon.png")
        await ctx.send(file=file_var, embed=embed_var)
    
    @repo.error
    async def repo_error(self, ctx, error):
        await sendDefaultError(ctx)

async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))