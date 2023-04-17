import discord

# Prefix for all bot commands
CMD_PREFIX = "?"

# For use in commands that check for owner status
OWNER_IDS = \
{230003732836909056} # Raymond

# For use in temporary messages
DEL_DELAY = 3

# For use in error handlers
ERROR_TITLE = "Something went wrong."
NO_PERM_MSG = "You don't have permissions to do that."
BAD_MEMBER_MSG = "Member not found. Nicknames and usernames are case sensitive, or maybe you spelled it wrong?"

async def sendDefaultError(ctx):
    embed_var = discord.Embed(title=ERROR_TITLE,
                             description="Unknown error. Contact an admin for more details.",
                             color=0xC80000)
    embed_var.set_footer(text=f"\u200bCommand attempted by {ctx.author.name}#{ctx.author.discriminator}")
    await ctx.send(embed=embed_var)
