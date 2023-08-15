import asyncio
from bot import RayBot
from globals import *
# from ui.mainui import RayBotUI

async def main():
    bot = RayBot(
        prefix=CMD_PREFIX,
        intents=discord.Intents.all(),
        tokenpath=getResourcePath(R".\..\TOKEN.txt"),
        cogspath=getResourcePath(R".\cogs")
    )
    await bot.vroom_vroom()
    # gui = RayBotUI(killcmd=bot.close)
    # gui.mainloop()

if __name__ == "__main__":
    asyncio.run(main())