from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from src.bot import bot
from src.config.get_logger import *
from aiogram.utils.chat_action import ChatActionSender
from src.api import cat_size
from src.states import CommonForm
import re

logger = get_logger('main.handlers')
cat_size_router = Router()


@cat_size_router.message(Command(commands=['catsize']))
async def cat_size_handler(message: Message, state: FSMContext):
    async with ChatActionSender.typing(message.chat.id, bot):
        text = f"Hey, {message.from_user.username}, send me :size of the image in px (:height x :width - 640x280)"
        await message.reply(text)
    await state.set_state(CommonForm.size)
    logger.info(f'/catsize - waiting for size - @{message.from_user.username}')


@cat_size_router.message(CommonForm.size)
async def cat_size_get_size(message: Message, state: FSMContext):
    if not re.match(r'\d{1,4}x\d{1,4}', message.text):
        async with ChatActionSender.typing(message.chat.id, bot):
            text = f"{message.from_user.username}, this is incorrect size. Try again"
            await message.reply(text)
        logger.warning(f'/catsize - incorrect image size - {message.text} - @{message.from_user.username}')
    else:
        async with ChatActionSender.upload_photo(message.chat.id, bot):
            await message.reply_photo(await cat_size(*map(int, message.text.split('x'))))
        await state.clear()
        logger.info(f'/catsize - {message.text} - @{message.from_user.username}')
