from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from src.api import cat
from src.bot import bot
from src.config.get_logger import *
from aiogram.utils.chat_action import ChatActionSender

logger = get_logger('main.handlers')
cat_router = Router()


@cat_router.message(Command(commands=['cat']))
async def cat_handler(message: Message):
    async with ChatActionSender.upload_photo(message.chat.id, bot):
        await message.reply_photo(await cat())
    logger.info(f'/cat - @{message.from_user.username}')
