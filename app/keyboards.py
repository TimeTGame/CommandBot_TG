from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from config import ADMINS


def kb_main(user_telegram_id: int):
    main_list = []

    if str(user_telegram_id) in ADMINS:
        main_list.append([KeyboardButton(text='📖 Github')])
        main_list.append([KeyboardButton(text='📂 Work with files')])
        main_list.append([KeyboardButton(text='🔐 Security')])

    keyboard = ReplyKeyboardMarkup(keyboard=main_list, resize_keyboard=True)
    return keyboard


def kb_files(user_telegram_id: int):
    files_list = []

    if str(user_telegram_id) in ADMINS:
        files_list.append([InlineKeyboardButton(text='Change directory', callback_data='chdir')])
        files_list.append([InlineKeyboardButton(text='List of files', callback_data='filesList')])
        files_list.append([InlineKeyboardButton(text='Create', callback_data='create'),
                           InlineKeyboardButton(text='Delete', callback_data='delete')])
        
    keyboard = InlineKeyboardMarkup(inline_keyboard=files_list)
    return keyboard

def kb_create(user_telegram_id: int):
    create_list = []

    if str(user_telegram_id) in ADMINS:
        create_list.append([InlineKeyboardButton(text='Directory', callback_data='directory'),
                           InlineKeyboardButton(text='File', callback_data='textFile')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=create_list)
    return keyboard



def kb_security(user_telegram_id: int):
    security_list = []

    if str(user_telegram_id) in ADMINS:
        security_list.append([InlineKeyboardButton(text='Take a picture', callback_data='picture')])
        security_list.append([InlineKeyboardButton(text='Lock screen', callback_data='lock'),
                             InlineKeyboardButton(text='Shutdown PC', callback_data='shutdown')])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=security_list)
    return keyboard

def kb_shutdown(user_telegram_id: int):
    shutdown_list = []

    if str(user_telegram_id) in ADMINS:
        shutdown_list.append([InlineKeyboardButton(text='Yes', callback_data='shutdown_Yes'),
                              InlineKeyboardButton(text='No', callback_data='shutdown_No')])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=shutdown_list)
    return keyboard