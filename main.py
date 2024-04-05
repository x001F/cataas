from src.config import *
from src.handlers import *
from src.bot import dp, bot
from src.other.commands import set_commands
import asyncio

logger = get_logger("main")
# You can disable sending logs in console by deleting "console" handler from every logger
# (cataas/config/config.yaml - data in logging it's logging settings)


async def run():
    dp.include_routers(*routers)
    logger.info(f"START bot polling")
    await set_commands()
    await dp.start_polling(bot, polling_timeout=5)
    logger.info(f"END bot polling")


if __name__ == "__main__":
    asyncio.run(run())
