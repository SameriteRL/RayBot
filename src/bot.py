import discord
from discord.ext import commands

import os
import sys

from src.globals import *

# Must take in a directory (folder), path cannot be a simple file
async def load_cogs(path:str, bot:commands.Bot):
    if not os.path.isdir(path):
        print(f"\n{path} is not a directory! Aborting cog loading.")
        return
    for file_name in os.listdir(path):
        new_path = os.path.join(path, file_name)
        if os.path.isdir(new_path):
            await load_cogs(new_path, bot)
        else:
            if file_name.endswith(".py"):
                cog = new_path[2:-3].replace("\\", ".")
                try: await bot.load_extension(cog)
                except commands.NoEntryPointError:
                    print(f"\n{cog} has no 'setup' function, ignoring file.")
                except Exception as err:
                    print(f"\n{err}")
                else: bot.loaded_cogs.add(cog)

class Bot(commands.Bot):

    def __init__(self, prefix:str, intents:discord.Intents):
        super().__init__(command_prefix=prefix, intents=intents)
        self.token = open("TOKEN.txt").read().strip()
        self.loaded_cogs = set()

    async def setup_hook(self):
        await load_cogs(".\src\cogs", self)
    
    async def on_ready(self):
        python_ver = ".".join(str(ver) for ver in sys.version_info[:3])
        num_synced = len(await self.tree.sync())
        print("\n==================================")
        print(">>" + f"Logged in as {self.user.name}#{self.user.discriminator}".center(30) + "<<")
        print(">>" + f"Discord.py version {discord.__version__}".center(30) + "<<")
        print(">>" + f"Python version {python_ver}".center(30) + "<<")
        print(f"{num_synced} command(s) synced!".center(34))
        print("==================================\n")
        print(f"Loaded {len(self.loaded_cogs)} extension(s):")
        for cog in self.loaded_cogs: print(f" - {cog}")
        print("\n==================================\n")
        print(f"Deployed in {len(self.guilds)} guild(s):")
        for guild in self.guilds: print(f" - {guild.name}")
        print("\n==================================\n")