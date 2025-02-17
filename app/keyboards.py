from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Work with files', callback_data='files')],
    [KeyboardButton(text='Security', callback_data='security')]
], resize_keyboard=True)


kb_files = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Change directory', callback_data='chdir')],
    [InlineKeyboardButton(text='List of files', callback_data='filesList')],
    [InlineKeyboardButton(text='Create', callback_data='create'), InlineKeyboardButton(text='Delete', callback_data='delete')]
])

kb_create = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Directory', callback_data='directory'), InlineKeyboardButton(text='File', callback_data='textFile')]
])


kb_security = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Lock screen', callback_data='lock')],
    [InlineKeyboardButton(text='Take a picture', callback_data='picture')],
    [InlineKeyboardButton(text='Shutdown PC', callback_data='shutdown')]
])

kb_shutdown = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Yes', callback_data='shutdown_Yes'), InlineKeyboardButton(text='No', callback_data='shutdown_No')]
])