from send2trash import send2trash
from cv2 import VideoCapture, imwrite
import pyautogui
from config import *
from time import sleep

from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, BotCommand, BotCommandScopeDefault

from app.mouse_tracker import mouse_tracker
import app.autostart_funcs as autostart
from app.utils import get_icon
import app.keyboards as kb
import os
import asyncio

print('- Your bot has been started.')

router = Router()
main_path = os.getcwd()


class files(StatesGroup):
    chdir = State()
    directory = State()
    fileName = State()
    fileContent = State()
    delete = State()

class sec(StatesGroup):
    shutdown = State()
    period = State()
    answer_wait = State()

class settings(StatesGroup):
    admins = State()


async def do_screenshots(chat_id, period, bot):
    global period_screenshot

    while period_screenshot > 0:
        myScreenshot = pyautogui.screenshot()

        if not os.path.exists(f'{main_path}/pic'):
            os.makedirs(f'{main_path}/pic')

        screenshot_path = f'{main_path}/pic/Screenshot.jpg'
        myScreenshot.save(screenshot_path)

        myScreenshot_file = FSInputFile(screenshot_path)

        await bot.send_photo(chat_id, myScreenshot_file)

        await asyncio.sleep(period)



@router.message(CommandStart())
async def cmd_start(message: Message):
    if str(message.from_user.id) in ADMINS:
        await message.bot.set_my_commands([BotCommand(command='start', description='Start'),
                               BotCommand(command='stop_period_screenshot', description='Stop period screenshot')],
                               BotCommandScopeDefault())
                
        await message.reply(f'Hello {message.from_user.full_name}, you can use the control panel.',
                            reply_markup=kb.kb_main(message.from_user.id))
    else:
        await message.answer('You are not on the list of administrators')


@router.message(Command('stop_period_screenshot')) # Command to stop periodic screenshot
async def stop_sacreenshots(message: Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        global period_screenshot
        period_screenshot = 0

        await message.answer('The periodic screenshot function has been stopped.')
        await state.clear()
        await message.answer('Now you can play with you computer', reply_markup=kb.kb_security(message.from_user.id))



@router.message(F.text == '📖 Github')
async def github(message: Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer('Creator: https://github.com/TimeTGame')


    
@router.message(F.text == '📂 Work with files')
async def work_with_files(message: Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer(f'Current working directory is:\n"{os.getcwd()}"')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files(message.from_user.id))
    else:
        await message.answer('You are not on the list of administrators')


@router.callback_query(F.data == 'chdir')
async def chdir_one(callback: CallbackQuery, state: FSMContext):
    await state.set_state(files.chdir)
    await callback.message.edit_text('Write the path to the desired directory')

@router.message(files.chdir)
async def chdir_two(message: Message, state: FSMContext):
    await state.update_data(chdir=message.text)
    data = await state.get_data()

    if os.path.exists(data["chdir"]):
        os.chdir(data["chdir"])
        await message.answer(f'Path successfully changed on:\n"{os.getcwd()}"')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files(message.from_user.id))
    else:
        await message.answer('This path does not exist')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files(message.from_user.id))
    
    await state.clear()


@router.callback_query(F.data == 'filesList')
async def filesList(callback: CallbackQuery):
    files = os.listdir(os.getcwd())
    files_with_icons = [f"{get_icon(file)} {file}" for file in files]
    formatted_list = "\n".join(files_with_icons)

    await callback.message.edit_text(f'List of files in a directory:\n{formatted_list}')
    await callback.message.answer('Now you can work with files', reply_markup=kb.kb_files(callback.from_user.id))


@router.callback_query(F.data == 'create')
async def create_choice(callback: CallbackQuery):
    await callback.message.edit_text('Create directory or text file', reply_markup=kb.kb_create(callback.from_user.id))

@router.callback_query(F.data == 'directory')
async def create_question_dir(callback: CallbackQuery, state: FSMContext):
    await state.set_state(files.directory)
    await callback.message.edit_text('Write the desired name for the new directory')

@router.message(files.directory)
async def create_directory(message: Message, state: FSMContext):
    await state.update_data(directory = message.text)
    data = await state.get_data()

    if not os.path.exists(data["directory"]):
        os.makedirs(data["directory"])
        await message.answer(f'Directory {data["directory"]} created')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files(message.from_user.id))
    else:
        await message.answer('A directory with this name already exists')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files(message.from_user.id))
    
    await state.clear()


@router.callback_query(F.data == 'textFile')
async def create_question_fileName(callback: CallbackQuery, state: FSMContext):
    await state.set_state(files.fileName)
    await callback.message.edit_text('Write the desired name for the new text file')

@router.message(files.fileName)
async def create_queston_fileContent(message: Message, state: FSMContext):
    await state.update_data(fileName = message.text)
    await state.set_state(files.fileContent)
    await message.answer('Write the desired content for the new text file')

@router.message(files.fileContent)
async def create_textFile(message: Message, state: FSMContext):
    await state.update_data(fileContent = message.text)
    data = await state.get_data()

    if not os.path.exists(data["fileName"]):
        with open(str(data["fileName"]), "w") as file:
            file.write(str(data['fileContent']))
        await message.answer(f'Text file {data["fileName"]} created')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files(message.from_user.id))
    else:
        await message.answer('A text file with this name already exists')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files(message.from_user.id))
    
    await state.clear()


@router.callback_query(F.data =='delete')
async def delete_question(callback: CallbackQuery, state: FSMContext):
    await state.set_state(files.delete)
    await callback.message.edit_text('Write the path to the directory or file you want to delete')

@router.message(files.delete)
async def delete_this(message: Message, state: FSMContext):
    await state.update_data(delete = message.text)
    data = await state.get_data()

    if os.path.exists(str(data['delete'])):
        send2trash(str(data["delete"]))
        await message.answer(f'"{str(data["delete"])}"\nhas been deleted')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files(message.from_user.id))
        print('LolYES')
    else:
        await message.answer(f'"{str(data["delete"])}"\ndoes not exist')
        await message.answer('Now you can work with files', reply_markup=kb.kb_files(message.from_user.id))
        print('LolNO')
    
    await state.clear()



@router.message(F.text == '🔐 Security')
async def securityMessage(message: Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer('Now you can play with you computer', reply_markup=kb.kb_security(message.from_user.id))
    else:
        await message.answer('You are not on the list of administrators')


@router.callback_query(F.data == 'lock')
async def lock_screen(callback: CallbackQuery):
    await callback.message.edit_text('Your PC is now locked')
    await callback.message.answer('Now you can play with you computer', reply_markup=kb.kb_security(callback.from_user.id))

    os.system("rundll32.exe user32.dll, LockWorkStation")


@router.callback_query(F.data == 'picture')
async def picture(callback: CallbackQuery):
    result, image = VideoCapture(0).read()
    if result:
        if not os.path.exists(f'{main_path}/pic'):
            os.makedirs(f'{main_path}/pic')

        imwrite(f'{main_path}/pic/CameraImage.jpg', image)
        photo = FSInputFile(f'{main_path}/pic/CameraImage.jpg')

        await callback.message.edit_media(InputMediaPhoto(media=photo, caption="Hi again"))
        await callback.message.answer('Now you can play with you computer', reply_markup=kb.kb_security(callback.from_user.id))
    else:
        await callback.message.answer('At the moment it is not possible to take photos from the camera')
        await callback.message.answer('Now you can play with you computer', reply_markup=kb.kb_security(callback.from_user.id))


@router.callback_query(F.data == 'screenshot')
async def screenshot_question(callback: CallbackQuery):
    await callback.message.edit_text('What screenshot do you want to take?', reply_markup=kb.kb_screenshot(callback.from_user.id))

@router.callback_query(F.data == 'oneTimeScreen')
async def oneTimeScreen(callback: CallbackQuery):
    myScreenshot = pyautogui.screenshot()

    if not os.path.exists(f'{main_path}/pic'):
        os.makedirs(f'{main_path}/pic')

    myScreenshot.save(f'{main_path}/pic/Screenshot.jpg')
    myScreenshot = FSInputFile(f'{main_path}/pic/Screenshot.jpg')

    await callback.message.edit_media(InputMediaPhoto(media=myScreenshot, caption="Screenshot"))
    await callback.message.answer('Now you can play with you computer', reply_markup=kb.kb_security(callback.from_user.id))

@router.callback_query(F.data == 'screenshot_period')
async def screenshot_period(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Write the period between screenshots (in seconds)')
    await state.set_state(sec.period)

@router.message(sec.period)
async def screenshot_period_set(message: Message, state: FSMContext):
    await state.update_data(period = message.text)
    data = await state.get_data()

    global period_screenshot
    period_screenshot = int(data["period"])

    if period_screenshot > 0:
        asyncio.create_task(do_screenshots(message.chat.id, period_screenshot, message.bot))
    else:
        await message.answer('The periodic screenshot function has been stopped.')
        await state.clear()
        await message.answer('Now you can play with you computer', reply_markup=kb.kb_security(message.from_user.id))


@router.callback_query(F.data == 'shutdown')
async def shutdown_question(callback: CallbackQuery):
    await callback.message.edit_text('Are you sure you want to turn it off?', reply_markup=kb.kb_shutdown(callback.from_user.id))

@router.callback_query(F.data == 'shutdown_No')
async def securityCallback(callback: CallbackQuery):
    await callback.message.edit_text('Now you can play with you computer', reply_markup=kb.kb_security(callback.from_user.id))

@router.callback_query(F.data == 'shutdown_Yes')
async def shutdown(callback: CallbackQuery):
    await callback.message.answer('Your PC will be turned off')
    await callback.message.answer('Now you can play with you computer', reply_markup=kb.kb_security(callback.from_user.id))

    os.system("shutdown /s /t 1")



@router.message(F.text == '⚙ Settings')
async def github(message: Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer('Settings', reply_markup=kb.kb_settings(message.from_user.id))
    else:
        await message.answer('You are not on the list of administrators')


@router.callback_query(F.data == 'update_admins')
async def update_admins(callback: CallbackQuery, state: FSMContext):
    await state.set_state(settings.admins)

    await callback.message.edit_text(f'current list of admins:\n{ADMINS}')
    await callback.message.answer('Enter the user ID of the user you want to make an admin or remove from the admin list.')

@router.message(settings.admins)
async def add_admin_func(message: Message, state: FSMContext):
    await state.update_data(admins = message.text)
    data = await state.get_data()

    if str(data["admins"]) in ADMINS:
        ADMINS.remove(str(data["admins"]))
        await message.answer(f'{data["admins"]} has been deleted form admin list.')
    else:
        ADMINS.append(str(data["admins"]))
        await message.answer(f'{data["admins"]} has been added in admin list.')
    
    with open(f'{main_path}/config.py', 'w') as file:
        file.writelines([f'TOKEN = \'{TOKEN}\'\n', f'ADMINS = {ADMINS}'])
    
    await message.answer(f'current list of admins:\n{ADMINS}', reply_markup=kb.kb_settings(message.from_user.id))
    
    await state.clear()

@router.callback_query(F.data == 'update_autostart')
async def update_autostart(callback: CallbackQuery, state: FSMContext):
    if autostart.check_autostart():
        autostart.delete_autostart()
        await callback.message.edit_text("🚮 Autostart was deleted")
    else:
        autostart.add_autostart()
        await callback.message.edit_text("✅ Autostart now is working")

    await state.clear()

@router.callback_query(F.data == 'update_mouse_tracker')
async def update_mouse_tracker(callback: CallbackQuery, bot: Bot):    
    if not mouse_tracker.is_tracking:
        chat_id = callback.message.chat.id
        
        mouse_tracker.start(chat_id=chat_id, bot=bot)
        await callback.message.edit_text("✅ Start mouse tracking")
    else:
        mouse_tracker.stop()
        await callback.message.edit_text(f"🔴 Shutdown mouse tracking")