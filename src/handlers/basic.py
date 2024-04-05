from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Router
from src.other import unid
from src.config.get_logger import *

logger = get_logger('main.handlers')
basic_router = Router()


@basic_router.message(CommandStart())
async def start_handler(message: Message):
    text = (f"Hello, {message.from_user.username}!\n"
            "This is bot CatFather\n"
            "I will send you a lot of cats if you ask me to!\n"
            "Send me /help to see more.")
    await message.reply(text)
    logger.info(f'/start - @{message.from_user.username}')
    await unid(message)


@basic_router.message(Command(commands=['help']))
async def help_handler(message: Message):
    text = (
        f"Hello, {message.from_user.username}!\n"
        f"Here are commands that I have:\n"
        f"/start - Restarts the bot\n"
        f"/help - Help\n\n"
        f"/cat - Sends a random cat\n"
        f"/catgif - Sends a random cat gif\n"
        # f"/cattag - Sends a random cat with a :tag\n"
        f"/catsays - Sends a random cat saying :text\n"
        f"/catsaysmore - Sends a random cat saying :text with :text parameters\n"
        f"/catgifsays - Sends a random gif cat saying :text\n"
        f"/catgifsaysmore - Sends a random gif cat saying :text with :text parameters\n"
        # f"/cattagsays - Sends a random cat with a :tag and saying :text\n"
        f"/cattype - Sends a random cat with image :type (xsmall, small, medium, or square)\n"
        f"/catfilter - Sends a random cat with image filters (mono, negate, custom (rgb))\n"
        f"/catsize - Sends a random cat with :width or :height (numbers)")
    await message.reply(text)
    logger.info(f'/help - @{message.from_user.username}')
    await unid(message)
