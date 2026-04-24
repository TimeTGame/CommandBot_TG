__all__ = [
    'create_dir_or_file',
    'delete_path_to_trash',
    'get_camera_image_path',
    'get_directory_contents',
    'get_screenshot_path',
    'save_admins_to_config',
]

import os
from pathlib import Path
from typing import Sequence

from send2trash import send2trash
from config import TOKEN


BASE_DIR = Path(__file__).resolve().parent.parent
PIC_DIR = BASE_DIR / 'pic'
CONFIG_PATH = BASE_DIR / 'config.py'


def get_directory_contents(path: str | Path | None = None) -> str:
    """
    Returns formatted list of contents in the selected directory.
    """
    directory = Path(path or os.getcwd()).expanduser().resolve()

    if not directory.exists():
        return f'Path does not exist:\n"{directory}"'

    if not directory.is_dir():
        return f'Path is not a directory:\n"{directory}"'

    try:
        files = sorted(item.name for item in directory.iterdir())
    except PermissionError:
        return f'No permission to read directory:\n"{directory}"'

    return f'List of contents in a directory:\n{files}'


def create_dir_or_file(path: str | Path) -> Path:
    """
    Creates a directory or a file.

    If the path has a suffix, it is treated as a file.
    Otherwise, it is treated as a directory.
    """
    target_path = Path(path).expanduser().resolve(strict=False)

    if target_path.suffix:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.touch(exist_ok=True)
    else:
        target_path.mkdir(parents=True, exist_ok=True)

    return target_path


def delete_path_to_trash(path: str | Path) -> Path:
    """
    Moves a file or directory to trash.
    """
    target_path = Path(path).expanduser().resolve(strict=False)

    if not target_path.exists():
        raise FileNotFoundError(f'Path does not exist: {target_path}')

    send2trash(str(target_path))
    return target_path


def get_screenshot_path() -> Path:
    """
    Returns path for saving a screenshot.
    """
    PIC_DIR.mkdir(parents=True, exist_ok=True)
    return PIC_DIR / 'Screenshot.jpg'


def get_camera_image_path() -> Path:
    """
    Returns path for saving a camera image.
    """
    PIC_DIR.mkdir(parents=True, exist_ok=True)
    return PIC_DIR / 'CameraImage.jpg'


def save_admins_to_config(admins: Sequence[str]) -> None:
    """
    Saves updated admin list to config.py.
    """
    normalized_admins = [str(admin_id) for admin_id in admins]

    CONFIG_PATH.write_text(
        f'TOKEN = {TOKEN!r}\n'
        f'ADMINS = {normalized_admins!r}\n',
        encoding='utf-8',
    )
