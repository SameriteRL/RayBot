import random

import discord
from discord.ext import commands
from discord.ext.commands import CommandError, Context

from globals import BAD_MEMBER_MSG, send_generic_error


class Miscellaneous(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    ### AVATAR ###
    @commands.hybrid_command(
        description = "Get the avatar of any user."
    )
    async def avatar(self, ctx: Context, member: discord.Member = None):
        # Avatar and color information is only accessible using fetch_user()
        target_user = await self.bot.fetch_user(
            member.id if member is not None else ctx.author.id
        )
        avatar_url = target_user.avatar.url
        target_color = target_user.accent_color
        embed_var = discord.Embed(color=target_color)
        embed_var.set_image(url=avatar_url)
        await ctx.send(embed=embed_var)
    
    @avatar.error
    async def avatar_error(self, ctx: Context, error: CommandError):
        if isinstance(error, commands.MemberNotFound):
            embed_var = discord.Embed(
                title = "Member not found",
                description = BAD_MEMBER_MSG,
                color = discord.Color.red()
            )
            await ctx.send(embed=embed_var)
        else:
            await send_generic_error(ctx, error)
    
    ### BANNER ###
    @commands.hybrid_command(
        description = "Get the banner of any user."
    )
    async def banner(self, ctx: Context, member: discord.Member = None):
        # Banner and color information is only accessible using fetch_user()
        target_user = await self.bot.fetch_user(
            member.id if member is not None else ctx.author.id
        )
        banner_url = target_user.banner.url if target_user.banner is not None else None
        target_color = target_user.accent_color
        embed_var = discord.Embed()
        if banner_url is not None:
            embed_var.color = target_color
            embed_var.set_image(url=banner_url)
        else:
            embed_var.title = "This user doesn't have a banner set!"
        await ctx.send(embed=embed_var)
    
    @banner.error
    async def banner_error(self, ctx: Context, error: CommandError):
        if isinstance(error, commands.MemberNotFound):
            embed_var = discord.Embed(
                title = "Member not found",
                description = BAD_MEMBER_MSG,
                color = discord.Color.red()
            )
            await ctx.send(embed=embed_var)
        else:
            await send_generic_error(ctx, error)

    ### COINFLIP ###
    @commands.hybrid_command(
        description = "Flip a coin!",
        aliases = ["flip", "coin"]
    )
    async def coinflip(self, ctx: Context):
        result = "Heads!" if random.randint(0, 1) == 0 else "Tails!"
        embedVar = discord.Embed(
            title = result,
            description = f"This had a 50% chance of happening.",
            color = discord.Color.green()
        )
        await ctx.send(embed=embedVar)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Miscellaneous(bot))