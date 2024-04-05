from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Router, F
from .tags import tags_router_cattagsays
from src.bot import bot
from src.config.get_logger import *
from aiogram.utils.chat_action import ChatActionSender
from src.api import cat_tagsays
from src.states import TagAndTextForm
import random

logger = get_logger('main.handlers')
cat_tagsays_router = Router()
cat_tagsays_router.include_router(tags_router_cattagsays)


# It is useless because of the site problem with tags system
@cat_tagsays_router.message(Command(commands=['cattagsays']))
async def cat_tagsays_handler(message: Message, state: FSMContext):
    async with ChatActionSender.typing(message.chat.id, bot):
        text = f'Hey, {message.from_user.username}, send me :text'
        await message.reply(text)
    await state.set_state(TagAndTextForm.text)
    logger.info(f'/catsize - waiting for text - @{message.from_user.username}')


@cat_tagsays_router.message(TagAndTextForm.text)
async def cat_tagsays_get_text(message: Message, state: FSMContext):
    if len(message.text) > 50:
        async with ChatActionSender.typing(message.chat.id, bot):
            text = f'{message.from_user.username}, this text is too big. Try again'
            await message.reply(text)
        logger.warning(f'/cattagsays - too big text - {message.text[:50]}. - @{message.from_user.username}')
    else:
        text = f'Hey, {message.from_user.username}, choose the :tag for image from list below'
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='See tags', callback_data='tags_list')]
        ])
        async with ChatActionSender.typing(message.chat.id, bot):
            await message.reply(text, reply_markup=keyboard)
        await state.set_state(TagAndTextForm.tag)


@cat_tagsays_router.callback_query(F.data.startswith('tag_'), TagAndTextForm.tag)
async def cat_tagsays_get_tag(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    async with ChatActionSender.upload_photo(callback_query.chat.id, bot):
        await bot.send_photo(callback_query.from_user.id,
                             await cat_tagsays(callback_query.data[4:], data['text']),
                             has_spoiler=random.randint(0, 1))
    await state.clear()
    logger.info(f'/cattagsays - {callback_query.text} - {data["text"]} - @{callback_query.from_user.username}')
