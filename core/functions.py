__all__ = ['get_directory_contents', 'create_dir_or_file']

import os
from pathlib import Path


def get_directory_contents() -> str:
    return f'List of files in a directory:\n{str(os.listdir(os.getcwd()))}'


def create_dir_or_file(path: str) -> Path:
    """
    Creates a directory and files
    """
    valid_path = Path(path).resolve()

    if valid_path.suffix:
        valid_path.parent.mkdir(parents=True, exist_ok=True)
        valid_path.touch(exist_ok=True)
    else:
        valid_path.mkdir(parents=True, exist_ok=True)

    return valid_path
