import os
import sys
import discord
from discord.ext.commands import Context

# Prefix for all bot commands
CMD_PREFIX = "?"

# The bot's user ID
SELF_ID = 980203562485317652

# For use in commands that check for owner status
OWNER_IDS = {230003732836909056} # Raymond

# For use in temporary messages
DEL_DELAY = 3

# For use in error handlers
ERROR_TITLE = "Something went wrong."
NO_PERM_MSG = "You don't have permissions to do that."
BAD_MEMBER_MSG = "Member not found. Nicknames and usernames are case sensitive, or maybe you spelled it wrong?"

# When running a one-file build, any resource files used by the program are unpacked
# into a temp directory referenced by sys._MEIPASS. This function is necessary to
# translate paths used during development into paths usable by the build.
def getResourcePath(rel_path:str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        return rel_path
    return os.path.join(base_path, rel_path)

async def sendDefaultError(ctx:Context):
    embed_var = discord.Embed(
        title=ERROR_TITLE,
        description="Unknown error. Contact an admin for more details.",
        color=0xC80000
    )
    embed_var.set_footer(text=f"\u200bCommand attempted by {ctx.author.name}#{ctx.author.discriminator}")
    await ctx.send(embed=embed_var)
