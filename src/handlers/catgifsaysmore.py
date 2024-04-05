from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from src.bot import bot
from src.config.get_logger import *
from aiogram.utils.chat_action import ChatActionSender
from src.api import cat_gif_says_more
from src.states import TextColorSizeGifForm

logger = get_logger('main.handlers')
cat_gif_says_more_router = Router()


@cat_gif_says_more_router.message(Command(commands=['catgifsaysmore']))
async def cat_says_more_handler(message: Message, state: FSMContext):
    async with ChatActionSender.typing(message.chat.id, bot):
        text = f'Hey, {message.from_user.username}, send me text for the gif image (length<50)'
        await message.reply(text)
    await state.set_state(TextColorSizeGifForm.text)
    logger.info(f'/catgifsaysmore - waiting for the text - {message.from_user.username}')


@cat_gif_says_more_router.message(TextColorSizeGifForm.text)
async def cat_says_more_text_get(message: Message, state: FSMContext):
    if len(message.text) > 50:
        async with ChatActionSender.typing(message.chat.id, bot):
            text = f"{message.from_user.username}, this text is too big. Try again (text length can't be bigger than 50)"
            await message.reply(text)
        logger.warning(f'/catsaysmore - too big text - {message.text} - @{message.from_user.username}')
    else:
        async with ChatActionSender.typing(message.chat.id, bot):
            text = 'To continue send me font color for the text (like red, black, ...)'
            await message.reply(text)
        await state.update_data({'text': message.text})
        await state.set_state(TextColorSizeGifForm.fontColor)


@cat_gif_says_more_router.message(TextColorSizeGifForm.fontColor)
async def cat_says_more_font_color_get(message: Message, state: FSMContext):
    if not message.text.isalpha():
        async with ChatActionSender.typing(message.chat.id, bot):
            text = (f"{message.from_user.username}, this color isn't correct. "
                    f"Try again (red/black/white or another existing color is correct)")
            await message.reply(text)
        logger.warning(f'/catsaysmore - incorrect fontColor - {message.text} - @{message.from_user.username}')
    else:
        text = "For end send me font size for the text (0 < size < 1000, set >200 isn't recommended)"
        await message.reply(text)
        await state.update_data({'color': message.text})
        await state.set_state(TextColorSizeGifForm.fontSize)


@cat_gif_says_more_router.message(TextColorSizeGifForm.fontSize)
async def cat_says_more_get_size(message: Message, state: FSMContext):
    if not message.text.isdigit() and 0 < int(message.text) < 1000:
        async with ChatActionSender.typing(message.chat.id, bot):
            text = (f"{message.from_user.username}, this size isn't a number "
                    f"or it's less then 0 or bigger then 1000. Try again (0 < size < 1000)")
            await message.reply(text)
        logger.warning(f'/catsaysmore - incorrect fontSize - {message.text} - @{message.from_user.username}')
    else:
        data = await state.get_data()
        async with ChatActionSender.upload_video(message.chat.id, bot):
            await message.reply_animation(await cat_gif_says_more(data['text'], data['color'], message.text))
        await state.clear()
        logger.info(f'/catgifsaysmore - {data["text"]} - {data["color"]} - {message.text} - @{message.from_user.username}')

