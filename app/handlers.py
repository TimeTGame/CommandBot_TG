__all__ = ['router']

import asyncio
import os
import subprocess
from pathlib import Path

import pyautogui
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    BotCommand,
    BotCommandScopeDefault,
    CallbackQuery,
    FSInputFile,
    Message,
)
from cv2 import VideoCapture, imwrite
import app.keyboards as kb
from config import ADMINS
from core.functions import (
    create_dir_or_file,
    delete_path_to_trash,
    get_camera_image_path,
    get_directory_contents,
    get_screenshot_path,
    save_admins_to_config,
)


router = Router()
periodic_screenshot_task: asyncio.Task | None = None


class Files(StatesGroup):
    chdir_path = State()
    create_path = State()
    delete_path = State()


class Security(StatesGroup):
    screenshot_period = State()


class Settings(StatesGroup):
    admin_id = State()


def is_admin(user_telegram_id: int) -> bool:
    return str(user_telegram_id) in ADMINS


async def deny_access(message: Message) -> None:
    await message.answer('You are not on the list of administrators')


async def deny_callback(callback: CallbackQuery) -> None:
    await callback.answer(
        'You are not on the list of administrators',
        show_alert=True,
    )


async def show_files_menu(message: Message, user_telegram_id: int) -> None:
    await message.answer(
        'Now you can work with files',
        reply_markup=kb.kb_files(user_telegram_id),
    )


async def show_security_menu(message: Message, user_telegram_id: int) -> None:
    await message.answer(
        'Security command list',
        reply_markup=kb.kb_security(user_telegram_id),
    )


async def send_periodic_screenshots(
    chat_id: int,
    period: int,
    bot,
) -> None:
    while True:
        screenshot_path = get_screenshot_path()
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)

        await bot.send_photo(chat_id, FSInputFile(screenshot_path))
        await asyncio.sleep(period)


# ---------- START COMMAND ----------


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    if not is_admin(message.from_user.id):
        await deny_access(message)
        return

    await message.bot.set_my_commands(
        [
            BotCommand(
                command='start',
                description='Start',
            ),
            BotCommand(
                command='stop_period_screenshot',
                description='Stop period screenshot',
            ),
        ],
        BotCommandScopeDefault(),
    )

    await message.reply(
        (
            f'Hello {message.from_user.full_name}, '
            'you can use the control panel.'
        ),
        reply_markup=kb.kb_main(message.from_user.id),
    )


@router.message(Command('stop_period_screenshot'))
async def stop_period_screenshot(
    message: Message,
    state: FSMContext,
) -> None:
    if not is_admin(message.from_user.id):
        await deny_access(message)
        return

    global periodic_screenshot_task

    if periodic_screenshot_task and not periodic_screenshot_task.done():
        periodic_screenshot_task.cancel()
        periodic_screenshot_task = None
        await message.answer('The periodic screenshot function has stopped.')
    else:
        await message.answer('Periodic screenshot function is not running.')

    await state.clear()
    await show_security_menu(message, message.from_user.id)


# ---------- GITHUB LINK ----------


@router.message(F.text == '📖 Github')
async def github(message: Message) -> None:
    if not is_admin(message.from_user.id):
        await deny_access(message)
        return

    await message.answer('Creator: https://github.com/TimeTGame')


# ---------- WORK WITH FILES ----------


@router.message(F.text == '📂 Work with files')
async def work_with_files_mode(message: Message) -> None:
    if not is_admin(message.from_user.id):
        await deny_access(message)
        return

    await message.answer(f'Current working directory is:\n"{os.getcwd()}"')
    await show_files_menu(message, message.from_user.id)


@router.callback_query(F.data == 'chdir')
async def chdir_parse_path(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if not is_admin(callback.from_user.id):
        await deny_callback(callback)
        return

    await state.set_state(Files.chdir_path)
    await callback.message.edit_text('Write the path to the desired directory')
    await callback.message.answer(get_directory_contents())
    await callback.answer()


@router.message(Files.chdir_path)
async def chdir_change_path(message: Message, state: FSMContext) -> None:
    if not is_admin(message.from_user.id):
        await deny_access(message)
        return

    path_to_move = Path(message.text).expanduser().resolve(strict=False)

    if not path_to_move.exists():
        await message.answer('This path does not exist')
    elif not path_to_move.is_dir():
        await message.answer('This path is not a directory')
    else:
        os.chdir(path_to_move)
        await message.answer(f'Path successfully changed to:\n"{os.getcwd()}"')

    await state.clear()
    await show_files_menu(message, message.from_user.id)


@router.callback_query(F.data == 'filesList')
async def files_list(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await deny_callback(callback)
        return

    await callback.message.edit_text(get_directory_contents())
    await callback.message.answer(
        'Now you can work with files',
        reply_markup=kb.kb_files(callback.from_user.id),
    )
    await callback.answer()


@router.callback_query(F.data == 'create')
async def create_parse_path(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if not is_admin(callback.from_user.id):
        await deny_callback(callback)
        return

    await state.set_state(Files.create_path)
    await callback.message.edit_text(f'Your path:\n"{os.getcwd()}"')
    await callback.message.answer(
        'Specify the path to the directory or file to create',
    )
    await callback.answer()


@router.message(Files.create_path)
async def create_path(message: Message, state: FSMContext) -> None:
    if not is_admin(message.from_user.id):
        await deny_access(message)
        return

    created_path = create_dir_or_file(message.text)

    await message.answer(f'Successfully created:\n"{created_path}"')
    await state.clear()
    await show_files_menu(message, message.from_user.id)


@router.callback_query(F.data == 'delete')
async def delete_parse_path(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if not is_admin(callback.from_user.id):
        await deny_callback(callback)
        return

    await state.set_state(Files.delete_path)
    await callback.message.edit_text(
        'Write the path to the directory or file you want to delete',
    )
    await callback.answer()


@router.message(Files.delete_path)
async def delete_path(message: Message, state: FSMContext) -> None:
    if not is_admin(message.from_user.id):
        await deny_access(message)
        return

    try:
        deleted_path = delete_path_to_trash(message.text)
    except FileNotFoundError:
        await message.answer(f'"{message.text}"\ndoes not exist')
    else:
        await message.answer(f'"{deleted_path}"\nhas been moved to trash')

    await state.clear()
    await show_files_menu(message, message.from_user.id)


# ---------- SECURITY ----------


@router.message(F.text == '🔐 Security')
async def security_mode(message: Message) -> None:
    if not is_admin(message.from_user.id):
        await deny_access(message)
        return

    await show_security_menu(message, message.from_user.id)


@router.callback_query(F.data == 'lock')
async def lock_screen(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await deny_callback(callback)
        return

    await callback.message.edit_text('Your PC is now locked')
    await callback.message.answer(
        'Security command list',
        reply_markup=kb.kb_security(callback.from_user.id),
    )

    subprocess.Popen(
        'rundll32.exe user32.dll,LockWorkStation',
        shell=True,
    )
    await callback.answer()


@router.callback_query(F.data == 'picture')
async def take_picture(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await deny_callback(callback)
        return

    camera = VideoCapture(0)
    result, image = camera.read()
    camera.release()

    if not result:
        await callback.message.answer(
            'At the moment it is not possible to take photos from the camera',
        )
    else:
        image_path = get_camera_image_path()
        imwrite(str(image_path), image)

        await callback.message.answer_photo(
            FSInputFile(image_path),
            caption='Camera photo',
        )

    await callback.message.answer(
        'Security command list',
        reply_markup=kb.kb_security(callback.from_user.id),
    )
    await callback.answer()


@router.callback_query(F.data == 'screenshot')
async def screenshot_question(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await deny_callback(callback)
        return

    await callback.message.edit_text(
        'What screenshot do you want to take?',
        reply_markup=kb.kb_screenshot(callback.from_user.id),
    )
    await callback.answer()


@router.callback_query(F.data == 'oneTimeScreen')
async def one_time_screenshot(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await deny_callback(callback)
        return

    screenshot_path = get_screenshot_path()
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)

    await callback.message.answer_photo(
        FSInputFile(screenshot_path),
        caption='Screenshot',
    )
    await callback.message.answer(
        'Security command list',
        reply_markup=kb.kb_security(callback.from_user.id),
    )
    await callback.answer()


@router.callback_query(F.data == 'screenshot_period')
async def screenshot_period_parse(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if not is_admin(callback.from_user.id):
        await deny_callback(callback)
        return

    await callback.message.edit_text(
        'Write the period between screenshots in seconds',
    )
    await state.set_state(Security.screenshot_period)
    await callback.answer()


@router.message(Security.screenshot_period)
async def screenshot_period_set(
    message: Message,
    state: FSMContext,
) -> None:
    if not is_admin(message.from_user.id):
        await deny_access(message)
        return

    global periodic_screenshot_task

    try:
        period = int(message.text)
    except ValueError:
        await message.answer('Period must be an integer number of seconds')
        return

    if period <= 0:
        await message.answer('Period must be greater than zero')
        return

    if periodic_screenshot_task and not periodic_screenshot_task.done():
        periodic_screenshot_task.cancel()

    periodic_screenshot_task = asyncio.create_task(
        send_periodic_screenshots(
            chat_id=message.chat.id,
            period=period,
            bot=message.bot,
        ),
    )

    await message.answer(
        f'Periodic screenshot function has started. Period: {period} sec.',
    )
    await state.clear()
    await show_security_menu(message, message.from_user.id)


@router.callback_query(F.data == 'shutdown')
async def shutdown_question(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await deny_callback(callback)
        return

    await callback.message.edit_text(
        'Are you sure you want to turn it off?',
        reply_markup=kb.kb_shutdown_agree(callback.from_user.id),
    )
    await callback.answer()


@router.callback_query(F.data == 'shutdown_No')
async def shutdown_cancel(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await deny_callback(callback)
        return

    await callback.message.edit_text('Shutdown has been canceled.')
    await callback.message.answer(
        'Security command list',
        reply_markup=kb.kb_security(callback.from_user.id),
    )
    await callback.answer()


@router.callback_query(F.data == 'shutdown_Yes')
async def shutdown(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await deny_callback(callback)
        return

    await callback.message.answer('Your PC will be turned off')
    await callback.message.answer(
        'Security command list',
        reply_markup=kb.kb_security(callback.from_user.id),
    )

    subprocess.Popen('shutdown /s /t 1', shell=True)
    await callback.answer()


# ---------- SETTINGS ----------


@router.message(F.text == '⚙ Settings')
async def settings_mode(message: Message) -> None:
    if not is_admin(message.from_user.id):
        await deny_access(message)
        return

    await message.answer(
        'Settings',
        reply_markup=kb.kb_settings(message.from_user.id),
    )


@router.callback_query(F.data == 'update_admins')
async def update_admins_parse(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if not is_admin(callback.from_user.id):
        await deny_callback(callback)
        return

    await state.set_state(Settings.admin_id)
    await callback.message.edit_text(f'Current list of admins:\n{ADMINS}')
    await callback.message.answer(
        'Enter the user ID you want to add or remove.',
    )
    await callback.answer()


@router.message(Settings.admin_id)
async def update_admins(message: Message, state: FSMContext) -> None:
    if not is_admin(message.from_user.id):
        await deny_access(message)
        return

    admin_id = message.text.strip()

    if admin_id in ADMINS:
        ADMINS.remove(admin_id)
        await message.answer(f'{admin_id} has been deleted from admin list.')
    else:
        ADMINS.append(admin_id)
        await message.answer(f'{admin_id} has been added to admin list.')

    save_admins_to_config(ADMINS)

    await message.answer(
        f'Current list of admins:\n{ADMINS}',
        reply_markup=kb.kb_settings(message.from_user.id),
    )
    await state.clear()
