from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from .tags import tags_router_cattag
from src.bot import bot
from src.config.get_logger import *
from aiogram.utils.chat_action import ChatActionSender
from src.api import cat_tag
from src.states import TagTextForm
import random

logger = get_logger("main.handlers")
cat_tag_router = Router()
cat_tag_router.include_router(tags_router_cattag)


# It is useless because of the site problem with tags system
@cat_tag_router.message(Command(commands=["cattag"]))
async def cat_tag_handler(message: Message, state: FSMContext):

    text = f"Hey, {message.from_user.username}, choose the :tag for image from list below"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='See tags', callback_data='tags_list')]
    ])
    async with ChatActionSender.typing(message.chat.id, bot):
        await message.reply(text, reply_markup=keyboard)
    await state.set_state(TagTextForm.tag)
    logger.info(f'/catsize - waiting for tag - @{message.from_user.username}')


@cat_tag_router.callback_query(F.data.startswith('tag_'), TagTextForm.tag)
async def cat_tag_get_tag(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    async with ChatActionSender.upload_photo(callback_query.chat.id, bot):
        await bot.send_photo(callback_query.from_user.id,
                             await cat_tag(callback_query.data[4:]),
                             has_spoiler=random.randint(0, 1))
    await state.clear()
    logger.info(f'/cattag - :{F.data[4:]} - @{callback_query.from_user.username}')
