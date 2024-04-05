from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo

# Image filters (/catfilter)
filters_button = [
    [InlineKeyboardButton(text='mono', callback_data='mono')],
    [InlineKeyboardButton(text='negate', callback_data='negate')],
    [InlineKeyboardButton(text='custom', callback_data='custom')]
]
filters_keyboard = InlineKeyboardMarkup(inline_keyboard=filters_button)

# Color palette (/catfilter)
color_palette_button = [[
    InlineKeyboardButton(text='Color palette', web_app=WebAppInfo(url='https://ya.ru/search/?text=rgb'))
]]
color_palette_keyboard = InlineKeyboardMarkup(inline_keyboard=color_palette_button)

# Image types (/cattype)
type_buttons = [
    [InlineKeyboardButton(text='xsmall', callback_data='xsmall')],
    [InlineKeyboardButton(text='small', callback_data='small')],
    [InlineKeyboardButton(text='medium', callback_data='medium')],
    [InlineKeyboardButton(text='square', callback_data='square')]
]
types_keyboard = InlineKeyboardMarkup(inline_keyboard=type_buttons)
