from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from src.other import filters_keyboard, color_palette_keyboard
from src.bot import bot
from src.config.get_logger import *
from aiogram.utils.chat_action import ChatActionSender
from src.api import cat_filter, cat_filter_custom
from src.states import FiltersForm
import re

logger = get_logger('main.handlers')
cat_filter_router = Router()


@cat_filter_router.message(Command(commands=['catfilter']))
async def cat_filter_handler(message: Message, state: FSMContext):
    async with ChatActionSender.typing(message.chat.id, bot):
        text = f"Hey, {message.from_user.username}, choose filter for the image from list below"
        await message.reply(text, reply_markup=filters_keyboard)
    await state.set_state(FiltersForm.wait)
    logger.info(f'/catfilter - waiting for filter choose - @{message.from_user.username}')


@cat_filter_router.callback_query(lambda c: c.data in ('mono', 'negate'), FiltersForm.wait)
async def cat_filter_handler(callback_query: CallbackQuery, state: FSMContext):
    async with ChatActionSender.upload_photo(callback_query.from_user.id, bot):
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_photo(callback_query.from_user.id, await cat_filter(callback_query.data))
    await state.clear()
    logger.info(f'/catfilter - {callback_query.data} - @{callback_query.from_user.username}')


@cat_filter_router.callback_query(F.data == 'custom', FiltersForm.wait)
async def cat_custom_filter_get_handler(callback_query: CallbackQuery, state: FSMContext):
    async with ChatActionSender.typing(callback_query.from_user.id, bot):
        text = f"Send me RGB color for the image (example: 255,255,255 - white, 0,0,0 - black)"
        await bot.edit_message_text(text, callback_query.from_user.id, callback_query.message.message_id,
                                    reply_markup=color_palette_keyboard)
    await state.set_state(FiltersForm.rgb)


@cat_filter_router.message(FiltersForm.rgb)
async def cat_custom_filter_handler(message: Message, state: FSMContext):
    if not re.match(r'\d{1,3},\d{1,3},\d{1,3}', message.text):
        async with ChatActionSender.typing(message.chat.id, bot):
            text = f"{message.from_user.username}, this is incorrect color. Try again"
            await message.reply(text, reply_markup=color_palette_keyboard)
        logger.warning(f"/catfilter - unknown color - {message.text} - @{message.from_user.username}")
    else:
        async with ChatActionSender.upload_photo(message.chat.id, bot):
            await message.reply_photo(await cat_filter_custom(*map(int, message.text.split(','))))
        await state.clear()
        logger.info(f"/catfilter - {message.text} - @{message.from_user.username}")
