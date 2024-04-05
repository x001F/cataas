from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from src.bot import bot
from src.config.get_logger import *
from aiogram.utils.chat_action import ChatActionSender
from src.api import cat_gif_says
from src.states import TextGifForm

logger = get_logger("main.handlers")
cat_gif_says_router = Router()


@cat_gif_says_router.message(Command(commands=["catgifsays"]))
async def cat_says_get_text(message: Message, state: FSMContext):
    async with ChatActionSender.typing(message.chat.id, bot):
        text = f'Hey, {message.from_user.username}, send me text for the gif image (length<50)'
        await message.reply(text)
    await state.set_state(TextGifForm.text)
    logger.info(f'/catgifsays - waiting for the text - @{message.from_user.username}')


@cat_gif_says_router.message(TextGifForm.text)
async def cat_says_end(message: Message, state: FSMContext):
    if len(message.text) > 50:
        async with ChatActionSender.typing(message.chat.id, bot):
            text = f"{message.from_user.username}, this text is too big. Try again (text length can't be bigger than 50)"
            await message.reply(text)
        logger.warning(f'/catsays - too big text - {message.text} - @{message.from_user.username}')
    else:
        async with ChatActionSender.upload_video(message.chat.id, bot):
            await message.reply_animation(await cat_gif_says(message.text))
        await state.clear()
        logger.info(f"/catsays - {message.text} - @{message.from_user.username}")