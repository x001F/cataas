from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from src.bot import bot
from src.config.get_logger import *
from aiogram.utils.chat_action import ChatActionSender
from src.api import cat_gif

logger = get_logger('main.handlers')
cat_gif_router = Router()


@cat_gif_router.message(Command(commands=['catgif']))
async def cat_gif_handler(message: Message):
    async with ChatActionSender.upload_video(message.chat.id, bot):
        await message.reply_animation(await cat_gif())
    logger.info(f'/catgif - @{message.from_user.username}')
