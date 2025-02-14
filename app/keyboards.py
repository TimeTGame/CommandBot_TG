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
    [InlineKeyboardButton(text='Create', callback_data='create'), InlineKeyboardButton(text='Delete', callback_data='delete')]
], resize_keyboard=True)

kb_security = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Block screen', callback_data='block')],
    [InlineKeyboardButton(text='Take a picture', callback_data='pictuer')],
    [InlineKeyboardButton(text='Shutdown PC', callback_data='shutdown')]
], resize_keyboard=True)