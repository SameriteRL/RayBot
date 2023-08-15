import os
import sys
import discord
from discord.ext import commands
from globals import *

class RayBot(commands.Bot):
    def __init__(self, prefix:str, intents:discord.Intents, tokenpath:str, cogspath:str):
        super().__init__(command_prefix=prefix, intents=intents)
        self.cogs_dir = cogspath
        self.token = self.readToken(tokenpath)
        self.loaded_cogs = set()

        python_ver = ".".join(str(ver) for ver in sys.version_info[:3])
        print(
            "Bot client initialized",
            f"Discord.py version {discord.__version__} | Python version {python_ver}",
            sep="\n"
        )

    async def setup_hook(self):
        print("Loading cogs")
        await self.loadCogs(getResourcePath(self.cogs_dir))
    
    async def on_ready(self):
        await self.consoleHandler()

    def readToken(self, path:str) -> str:
        with open(path) as file:
            token = file.read().strip()
        return token
    
    # Path argument must be a directory
    async def loadCogs(self, path:str) -> None:
        if not os.path.isdir(path):
            print(f"\n{path} is not a directory! Aborting cog loading.")
            return
        for file_name in os.listdir(path):
            new_path = os.path.join(path, file_name)
            if os.path.isdir(new_path):
                await self.loadCogs(new_path)
            else:
                if file_name.endswith(".py"):
                    # NOTE: Make the path to cog conversion below "smarter" somehow
                    cog = new_path[2:-3].replace("\\", ".").replace("..", "")
                    try:
                        await self.load_extension(cog)
                    except commands.NoEntryPointError:
                        print(f"{cog} has no 'setup' function, ignoring file.")
                    except Exception as err:
                        print(f"{err}")
                    else: self.loaded_cogs.add(cog)
    
    async def consoleHandler(self) -> None:
        num_synced = len(await self.tree.sync())
        print(f"Logged in as {self.user.name}#{self.user.discriminator}")
        if len(self.loaded_cogs) == 0:
            print("WARNING: No extensions were loaded")
        else:
            print(f"Loaded {len(self.loaded_cogs)} extension(s), {num_synced} commands synced:")
            for cog in self.loaded_cogs:
                print(f"\t{cog}")
        if len(self.guilds) == 0:
            print("WARNING: Bot is not currently in any guilds")
        else:
            print(f"Deployed in {len(self.guilds)} guild(s):")
            for guild in self.guilds:
                print(f"\t{guild.name}")
    
    async def vroom_vroom(self) -> None:
        await self.start(self.token)