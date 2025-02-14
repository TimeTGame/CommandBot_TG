from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Work with files', callback_data='files')],
    [KeyboardButton(text='Security', callback_data='security')]
], resize_keyboard=True)

kb_files = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Change directory', callback_data='move')],
    [InlineKeyboardButton(text='List of files', callback_data='filesList')],
    [KeyboardButton(text='Create', callback_data='create'), KeyboardButton(text='Delete', callback_data='delete')]
], resize_keyboard=True)