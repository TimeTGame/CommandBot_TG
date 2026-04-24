__all__ = [
    'kb_main',
    'kb_files',
    'kb_create',
    'kb_security',
    'kb_screenshot',
    'kb_shutdown_agree',
    'kb_settings',
]

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from config import ADMINS


def kb_main(user_telegram_id: int):
    main_list = []

    if str(user_telegram_id) in ADMINS:
        main_list.append([KeyboardButton(text='📖 Github')])
        main_list.append([KeyboardButton(text='📂 Work with files')])
        main_list.append([KeyboardButton(text='🔐 Security')])
        main_list.append([KeyboardButton(text='⚙ Settings')])

    keyboard = ReplyKeyboardMarkup(keyboard=main_list, resize_keyboard=True)
    return keyboard


def kb_files(user_telegram_id: int):
    files_list = []

    if str(user_telegram_id) in ADMINS:
        files_list.append(
            [
                InlineKeyboardButton(
                    text='Change directory',
                    callback_data='chdir',
                ),
            ],
        )
        files_list.append(
            [
                InlineKeyboardButton(
                    text='List of files',
                    callback_data='filesList',
                ),
            ],
        )
        files_list.append(
            [
                InlineKeyboardButton(text='Create', callback_data='create'),
                InlineKeyboardButton(text='Delete', callback_data='delete'),
            ],
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=files_list)
    return keyboard


def kb_create(user_telegram_id: int):
    create_list = []

    if str(user_telegram_id) in ADMINS:
        create_list.append(
            [
                InlineKeyboardButton(
                    text='Directory',
                    callback_data='directory',
                ),
                InlineKeyboardButton(text='File', callback_data='textFile'),
            ],
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=create_list)
    return keyboard


def kb_security(user_telegram_id: int):
    security_list = []

    if str(user_telegram_id) in ADMINS:
        security_list.append(
            [
                InlineKeyboardButton(
                    text='Take a pic from the camera',
                    callback_data='picture',
                ),
                InlineKeyboardButton(
                    text='Take a screenshot',
                    callback_data='screenshot',
                ),
            ],
        )
        security_list.append(
            [
                InlineKeyboardButton(text='Lock screen', callback_data='lock'),
                InlineKeyboardButton(
                    text='Shutdown PC',
                    callback_data='shutdown',
                ),
            ],
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=security_list)
    return keyboard


def kb_screenshot(user_telegram_id: int):
    screenshot_list = []

    if str(user_telegram_id) in ADMINS:
        screenshot_list.append(
            [
                InlineKeyboardButton(
                    text='One-time screenshot',
                    callback_data='oneTimeScreen',
                ),
            ],
        )
        screenshot_list.append(
            [
                InlineKeyboardButton(
                    text='Set screenshot period',
                    callback_data='screenshot_period',
                ),
            ],
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=screenshot_list)
    return keyboard


def kb_shutdown_agree(user_telegram_id: int):
    shutdown_list = []

    if str(user_telegram_id) in ADMINS:
        shutdown_list.append(
            [
                InlineKeyboardButton(text='Yes', callback_data='shutdown_Yes'),
                InlineKeyboardButton(text='No', callback_data='shutdown_No'),
            ],
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=shutdown_list)
    return keyboard


def kb_settings(user_telegram_id: int):
    settings_list = []

    if str(user_telegram_id) in ADMINS:
        settings_list.append(
            [
                InlineKeyboardButton(
                    text='Update admins',
                    callback_data='update_admins',
                ),
            ],
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=settings_list)
    return keyboard
