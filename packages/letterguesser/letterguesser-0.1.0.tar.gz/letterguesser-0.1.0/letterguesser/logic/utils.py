"""
Utility functions for the LetterGuesser application.

Contains helper functions for resource loading and text file operations.
"""

import sys
from pathlib import Path


def get_resource_path(relative_path: str | Path) -> Path:
    """
    Get the absolute path for a resource, compatible with PyInstaller.

    :param relative_path: Path relative to the project root.
    :return: Absolute path to the resource.
    """
    if hasattr(sys, '_MEIPASS'):
        base_path = Path(sys._MEIPASS) / 'letterguesser'
    else:
        base_path = Path(__file__).resolve().parent.parent
    return base_path / relative_path


def load_texts(lang_code: str) -> str:
    """
    Load text data for a specific language from a text file.

    :param lang_code: Language code, such as 'en' or 'uk'.
    :return: Text data as a single string with specific formatting.
    """
    file_path = get_resource_path(f'assets/texts/{lang_code}.txt')

    with open(file_path, 'r', encoding='utf-8') as file:
        text_data = file.read()
    return text_data.replace('\n', '_').replace(' ', '_')
