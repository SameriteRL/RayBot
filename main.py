import asyncio
from src.bot import Bot
from src.globals import *

async def main():
    bot = Bot(CMD_PREFIX, discord.Intents.all())
    await bot.start(bot.token)

if __name__ == "__main__":
    asyncio.run(main())