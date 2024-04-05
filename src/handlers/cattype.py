from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from src.other import types_keyboard
from src.bot import bot
from src.config.get_logger import *
from aiogram.utils.chat_action import ChatActionSender
from src.api import cat_type
from src.states import CommonForm
import random

logger = get_logger('main.handlers')
cat_type_router = Router()


@cat_type_router.message(Command(commands=['cattype']))
async def cat_type_handler(message: Message, state: FSMContext):
    async with ChatActionSender.typing(message.chat.id, bot):
        text = f'Hey, {message.from_user.username}, choose image type from list below\n'
        await message.reply(text, reply_markup=types_keyboard)
    await state.set_state(CommonForm.image_type)
    logger.info(f'/catsize - waiting for type - @{message.from_user.username}')


@cat_type_router.callback_query(lambda c: c.data in ('xsmall', 'small', 'medium', 'square'), CommonForm.image_type)
async def cat_type_get_type(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    async with ChatActionSender.upload_photo(callback_query.from_user.id, bot):
        await bot.send_photo(callback_query.from_user.id, await cat_type(callback_query.data))
    await state.clear()
    logger.info(f'/cattype - {callback_query.data} - @{callback_query.from_user.username}')
