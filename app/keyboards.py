from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Change directory', callback_data='move')],
    [KeyboardButton(text='Block screen', callback_data='block'), KeyboardButton(text='Take a photo', callback_data='photo')]
], resize_keyboard=True)