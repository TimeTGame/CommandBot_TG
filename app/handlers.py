__all__ = []

import os
from pathlib import Path

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message,
    CallbackQuery,
    BotCommand,
    BotCommandScopeDefault,
)
import app.keyboards as kb
from config import ADMINS
from core.functions import get_directory_contents


router = Router()


class Files(StatesGroup):
    chdir_path = State()
    create_path = State()


# ---------- START COMMAND ----------
@router.message(CommandStart())
async def cmd_start(message: Message):
    if str(message.from_user.id) in ADMINS:
        await message.bot.set_my_commands(
            [
                BotCommand(
                    command='start',
                    description='Start',
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
    else:
        await message.answer('You are not on the list of administrators')


# ---------- GITHUB LINK ----------
@router.message(F.text == '📖 Github')
async def github(message: Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer('Creator: https://github.com/TimeTGame')


# ---------- WORK WITH FILES ----------
@router.message(F.text == '📂 Work with files')
async def work_with_files_mode(message: Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer(f'Current working directory is:\n"{os.getcwd()}"')
        await message.answer(
            'Now you can work with files',
            reply_markup=kb.kb_files(message.from_user.id),
        )
    else:
        await message.answer('You are not on the list of administrators')


# < Change directory >
@router.callback_query(F.data == 'chdir')
async def chdir_parse_path(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Files.chdir_path)
    await callback.message.edit_text('Write the path to the desired directory')
    await callback.message.answer(
        get_directory_contents(),
    )


@router.message(Files.chdir_path)
async def chdir_change_path(message: Message, state: FSMContext):
    await state.update_data(path=message.text)
    data = await state.get_data()
    path_to_move = str(data['path'])
    valid_path = Path(path_to_move).resolve()

    if Path(valid_path).exist():
        os.chdir(valid_path)
        await message.answer(f'Path successfully changed on:\n"{os.getcwd()}"')
    else:
        await message.answer('This path does not exist')

    await state.clear()


# < Get files list >
@router.callback_query(F.data == 'filesList')
async def files_list(callback: CallbackQuery):
    await callback.message.edit_text(
        f'List of files in a directory:\n{str(os.listdir(os.getcwd()))}',
    )
    await callback.message.answer(
        'Now you can work with files',
        reply_markup=kb.kb_files(callback.from_user.id),
    )


# < Create driectory/file >
@router.callback_query(F.data == 'create')
async def create_parse_path(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Files.chdir_path)
    await callback.message.edit_text(f'You\'r path:\n"{os.getcwd()}"')
    await callback.message.answer(
        'Specify the path to the directory/file to create',
    )


@router.message(Files.create_path)
async def create_dir_or_file(message: Message, state: FSMContext):
    await state.update_data(path=message.text)
    data = await state.get_data()
    path_to_move = str(data['path'])

    if Path(path_to_move).exist():
        create_dir_or_file(path_to_move)
        await message.answer(f'Successfully created:\n"{os.getcwd()}"')
    else:
        await message.answer('This path does not exist')

    await state.clear()

    await message.answer(
        'Now you can work with files',
        reply_markup=kb.kb_files(message.from_user.id),
    )


# ---------- SECURITY ----------
@router.message(F.text == '🔐 Security')
async def security_mode(message: Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer(
            'Security command list',
            reply_markup=kb.kb_security(message.from_user.id),
        )
    else:
        await message.answer('You are not on the list of administrators')


print('- Your bot has been started.')
