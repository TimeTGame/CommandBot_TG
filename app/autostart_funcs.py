import os
import platform

_system = platform.system()

def add_autostart():    
    app_dir = os.getcwd()
    app_path = os.path.join(app_dir, 'startTGBot.bat')

    if _system == 'Windows':
        import winshell
        startup_folder = winshell.startup()

        shortcut_path = os.path.join(startup_folder, 'startTGBot.lnk')

        winshell.CreateShortcut(
            Path=shortcut_path,
            Target=app_path,
            StartIn=app_dir,
            Description='Telegram Bot autostart'
        )

    elif _system == 'Linux':
        desktop_file = os.path.expanduser('~/.config/autostart/startTGBot.desktop')
        os.makedirs(os.path.dirname(desktop_file), exist_ok=True)
        
        with open(desktop_file, 'w') as f:
            f.write(f"""[Desktop Entry]
Type=Application
Name=startTGBot
Exec=startTGBot
X-GNOME-Autostart-enabled=true
""")
    print("Готово! Приложение добавлено в автозагрузку.")


def delete_autostart():
    if _system == "Windows":
        import winshell

        startup_folder = winshell.startup()
        shortcut_path = os.path.join(startup_folder, "startTGBot.lnk")

        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
            print("Ярлык удален из автозагрузки")
        else:
            print("Ярлык не найден в автозагрузке")

    elif _system == 'Linux':
        desktop_file = os.path.expanduser('~/.config/autostart/startTGBot.desktop')
        
        if os.path.exists(desktop_file):
            os.remove(desktop_file)
            print("Ярлык удален из автозагрузки")
        else:
            print("Ярлык не найден в автозагрузке")


def check_autostart():
    if _system == "Windows":
        import winshell
        
        startup_folder = winshell.startup()
        shortcut_path = os.path.join(startup_folder, "startTGBot.lnk")

    elif _system == 'Linux':
        shortcut_path = os.path.expanduser('~/.config/autostart/startTGBot.desktop')

    return os.path.exists(shortcut_path)