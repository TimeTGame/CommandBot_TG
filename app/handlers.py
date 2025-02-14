import os
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Hello!\nYour ID: {message.from_user.id}\nName: {message.from_user.full_name}',
                        reply_markup=kb.main)
    
@router.message(F.text == 'Change directory')
async def chdir_message(message: Message):
    await message.answer(f'Current working directory is:\n"{os.getcwd()}"')