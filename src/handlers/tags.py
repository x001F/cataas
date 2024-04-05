from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from src.bot import bot
from src.config.get_logger import *
from src.api import tags

logger = get_logger("main.handlers")
tags_router_cattag = Router()
tags_router_cattagsays = Router()


async def tags_move_back(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tags_lst = data["tags"]
    start, end = data["range"][0]-25 % len(tags_lst), data["range"][1]-25 % len(tags_lst)
    buttons = [[InlineKeyboardButton(text="<", callback_data="tags_move_back")]]
    buttons.extend([[InlineKeyboardButton(text=i_tag, callback_data=f"tag_{i}")] for i, i_tag in enumerate(tags_lst[start:end])])
    buttons.extend([[InlineKeyboardButton(text=">", callback_data="tags_move_forward")]])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await state.update_data({"range": (start, end)})
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                        reply_markup=keyboard)


async def tags_list(callback_query: CallbackQuery, state: FSMContext):
    tags_lst = await tags()
    buttons = [[InlineKeyboardButton(text=i_tag, callback_data=f"tag_{i}")] for i, i_tag in enumerate(tags_lst[:25])]
    buttons.append([InlineKeyboardButton(text=">", callback_data="tags_move_forward")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await state.update_data({"tags": tags_lst, "range": (0, 25)})
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                        reply_markup=keyboard)


async def tags_move_forward(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tags_lst = data["tags"]
    start, end = data["range"][0]+25 % len(tags_lst), data["range"][1]+25 % len(tags_lst)
    buttons = [[InlineKeyboardButton(text="<", callback_data="tags_move_back")]]
    buttons.extend([[InlineKeyboardButton(text=i_tag, callback_data=f"tag_{i_tag}")] for i, i_tag in enumerate(tags_lst[start:end])])
    buttons.extend([[InlineKeyboardButton(text=">", callback_data="tags_move_forward")]])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await state.update_data({"range": (start, end)})
    await bot.edit_message_reply_markup(callback_query.from_user.id,  callback_query.message.message_id,
                                        reply_markup=keyboard)


# If I do decoration with one decorator it'll cause exception
# RuntimeError -> Multiply attaching routers
# (this will attach one router twice to main router though cattagsays, cattag routers)
# RuntimeError: Router is already attached to <Router '...'>
tags_router_cattag.callback_query(F.data == "tags_move_back")(tags_move_back)
tags_router_cattag.callback_query(F.data == "tags_list")(tags_list)
tags_router_cattag.callback_query(F.data == "tags_move_forward")(tags_move_forward)
tags_router_cattagsays.callback_query(F.data == "tags_move_back")(tags_move_back)
tags_router_cattagsays.callback_query(F.data == "tags_list")(tags_list)
tags_router_cattagsays.callback_query(F.data == "tags_move_forward")(tags_move_forward)
# I know that this looks terrible
