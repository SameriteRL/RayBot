import discord
from discord.ext import commands
from discord.ext.commands import Context

import random

from src.globals import *

class Miscellaneous(commands.Cog):

    def __init__(self, bot:commands.Bot):
        self.bot = bot

    ### PING ###
    @commands.hybrid_command(description="Get the latency between your client and Discord!",
                             aliases=["latency"])
    async def ping(self, ctx:Context):
        # Retrieves the server latency in milliseconds
        embed_var = discord.Embed(
            title="Pong!",
            description=f"Your message was recieved in {round(self.bot.latency * 1000)}ms.",
            color=0x00C500
        )
        # Sends the embed
        await ctx.send(embed=embed_var)
    
    @ping.error
    async def ping_error(self, ctx, error):
        await sendDefaultError(ctx)

    ### COINFLIP ###
    @commands.hybrid_command(description="Flip a coin!",
                             aliases=["flipcoin", "coin"])
    async def coinflip(self, ctx:Context):
        # Randomly chooses either 0 or 1 as heads or tails
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

    ### WHOIS ###
    @commands.hybrid_command(description="Get the profile info of any user!",
                             aliases=["info", "profile"])
    async def whois(self, ctx:Context, member:discord.Member=None):

        # Determines who the target of the command is based on the presence of an argument
        target_user = (await self.bot.fetch_user(member.id)) if member != None \
                       else (await self.bot.fetch_user(ctx.author.id))
        target_member = (await ctx.guild.fetch_member(member.id)) if member != None \
                         else (await ctx.guild.fetch_member(ctx.author.id))
        
        # Gets various info about the target
        name = target_user.name
        mention = target_user.mention
        avatar_url = target_user.avatar.url
        banner_url = target_user.banner.url if target_user.banner != None else None
        accent_color = target_user.accent_color

        # Creates and sends the profile embed
        embed_var = discord.Embed(
            title=name,
            description=mention,
            color=accent_color
        )
        embed_var.set_thumbnail(url=avatar_url)
        raw_time = target_user.created_at
        creation_time = f"{raw_time.month}/{raw_time.day}/{raw_time.year} at \
                        {raw_time.hour:02}:{raw_time.minute:02}:{raw_time.second:02}"
        embed_var.add_field(
            name="**Joined Discord on:**",
            value=creation_time,
            inline=False
        )
        raw_time = target_member.joined_at
        creation_time = f"{raw_time.month}/{raw_time.day}/{raw_time.year} at \
                        {raw_time.hour:02}:{raw_time.minute:02}:{raw_time.second:02}"
        embed_var.add_field(
            name=f"**Joined {ctx.guild.name} on:**",
            value=creation_time,
            inline=False
        )
        if banner_url != None: embed_var.set_image(url=banner_url)
        await ctx.send(embed=embed_var)
    
    @whois.error
    async def whois_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed_var = discord.Embed(
                title=ERROR_TITLE,
                description=BAD_MEMBER_MSG,
                color=0xC80000
            )
            await ctx.send(embed=embed_var)
        else:
            await sendDefaultError(ctx)
    
    ### AVATAR ###
    @commands.hybrid_command(description="Get the avatar of any user!",
                             aliases=["pfp", "picture"])
    async def avatar(self, ctx:Context, member:discord.Member=None):
        target_user = (await self.bot.fetch_user(member.id)) if member != None \
                       else (await self.bot.fetch_user(ctx.author.id))
        avatar_url = target_user.display_avatar.url
        target_color = target_user.accent_color
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

    ### BANNER ###
    @commands.hybrid_command(description="Get the banner of any user!")
    async def banner(self, ctx:Context, member:discord.Member=None):
        target_user = (await self.bot.fetch_user(member.id)) if member != None \
                       else (await self.bot.fetch_user(ctx.author.id))
        banner_url = target_user.banner.url if target_user.banner != None else None
        target_color = target_user.accent_color
        embed_var = discord.Embed(
            title="This user doesn't have a banner set!" if banner_url == None else None,
            color=target_color
        )
        if banner_url != None: embed_var.set_image(url=banner_url)
        await ctx.send(embed=embed_var)
    
    @banner.error
    async def banner_error(self, ctx, error):
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
        embed_var = discord.Embed(
            title=f"Click Here to Visit the {ctx.guild.get_member(SELF_ID).name} Repository!",
            url='https://github.com/SameriteRL/RayBot-2',
            color=0x0099FF
        )
        await ctx.send(embed=embed_var)
    
    @repo.error
    async def repo_error(self, ctx, error):
        await sendDefaultError(ctx)

async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))