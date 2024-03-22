import logging

import discord
from discord import Interaction
from discord.ext.commands import CommandError, Context


async def send_generic_error(ctx: Context | Interaction, error: CommandError = None) -> None:
    """
    Standard error message for any unhandled or unexpected command errors.
    """
    embed_var = discord.Embed(
        title = ERROR_TITLE,
        description = "Unknown error. This is probably the dev's fault, sorry!",
        color = discord.Color.red()
    )
    if isinstance(ctx, Context):
        await ctx.send(embed=embed_var)
    else:
        await ctx.response.send_message(embed=embed_var)
    if error is not None:
        logging.error(
            msg = f'Error from command "{ctx.command}" in extension'
                  + f'"{ctx.cog.qualified_name}"',
            exc_info = True
        )

ERROR_TITLE = "Something went wrong"
NO_PERM_MSG = "You don't have permissions to do that."
BAD_MEMBER_MSG = "Member not found. Nicknames and usernames are case sensitive, or" \
                 + "maybe you spelled it wrong?"