__all__ = ['Utils']
__author__ = 'Felipe Amaral'
__version__ = '0.1'

import json

from pathlib import Path
from typing import Union
from datetime import datetime, timedelta


class Utils:


    @staticmethod
    def get_data_from_json(
        path: Union[Path, str]
    ) -> dict:
        """
        Reads and parses a JSON file.

        Parameters:
            - path (Union[Path, str]): Path to the JSON file.

        Returns:
            - dict: Parsed data from the JSON file.
        """

        with open(file=path, mode='r', encoding='utf-8') as file:
            return json.loads(file.read())

    @staticmethod
    def get_unique_filename(
        file_path: Union[Path, str]
    ) -> Path:
        """
        Generates a unique filename by appending a counter if the file already exists.

        Parameters:
            - file_path (Union[Path, str]): Path to the file.

        Returns:
            - Path: Unique file path.
        """

        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        count = 0
        while file_path.exists():
            count += 1
            suffix = file_path.suffix
            base_path = file_path.with_suffix('')
            file_path = Path(f"{base_path}({count}){suffix}")
        return file_path

    @staticmethod
    def get_last_modified_file_path(
        dir_path: Union[Path, str]
    ) -> Path:
        """
        Gets the most recently modified file in a directory.

        Parameters:
            - dir_path (Union[Path, str]): Path to the directory.

        Returns:
            - Path: Path to the most recently modified file.
        """

        if not isinstance(dir_path, Path):
            dir_path = Path(dir_path)

        files_path = list(dir_path.iterdir())
        if not files_path:
            raise FileNotFoundError(f"No files found in {dir_path}")

        return max(files_path, key=lambda f: f.stat().st_mtime)

    @staticmethod
    def format_time(
        seconds: Union[float, int, str]
    ) -> str:
        """
        Converts a duration in seconds into a formatted time string.

        Parameters:
            - seconds (Union[float, int, str]): Duration in seconds.

        Returns:
            - str: Formatted time string (e.g., "01:02:03").
        """

        seconds = int(seconds)
        if seconds < 60:
            return f"00:{seconds:02}"
        elif seconds < 3600:
            return f"{seconds // 60:02}:{seconds % 60:02}"
        else:
            return (
                f"{seconds // 3600:02}:{(seconds % 3600) // 60:02}:{seconds % 60:02}"
            )

    @staticmethod
    def format_compact_number(
        number: Union[float, int, str]
    ) -> str:
        """
        Formats a number into a compact representation (e.g., 1.2M).

        Parameters:
            - number (Union[float, int, str]): Number to format.

        Returns:
            - str: Compact number string.
        """

        number = int(number)
        if number >= 1_000_000_000:
            return f"{number / 1_000_000_000:.1f}B"
        elif number >= 1_000_000:
            return f"{number / 1_000_000:.1f}M"
        elif number >= 1_000:
            return f"{number / 1_000:.1f}k"
        else:
            return str(number)

    @staticmethod
    def is_url(
        value: str
    ) -> bool:
        """
        Checks if a string is a valid URL.

        Parameters:
            - value (str): String to check.

        Returns:
            - bool: True if the string is a valid URL, False otherwise.
        """

        return 'https://' in value

    @staticmethod
    def is_youtube_url(
        value: str
    ) -> bool:
        """
        Checks if a URL is a YouTube URL.

        Parameters:
            - value (str): URL to check.

        Returns:
            - bool: True if the URL is a YouTube URL, False otherwise.
        """

        return 'https://youtube.com' in value

    @staticmethod
    def get_time_ago(
        seconds: Union[float, int]
    ) -> datetime:
        """
        Calculates the datetime a certain number of seconds ago.

        Parameters:
            - seconds (Union[float, int]): Number of seconds.

        Returns:
            - datetime: Datetime object representing the time ago.
        """
        
        return datetime.now() - timedelta(seconds=seconds)
