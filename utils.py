import csv
import os
import sys
from enum import Enum
from typing import Iterable

from pystreamapi import Stream


class MyEnum(Enum):
    def __str__(self):
        return self.name

    @classmethod
    def value_of(cls, name: str):
        return Stream.of(cls) \
            .filter(lambda item: item.name.lower() == name.lower()) \
            .find_first() \
            .get()

def clear_screen():
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

def parse_date(date_str: str) -> float:
    """
    Преобразует строку вида '25.05.2025' в timestamp (float).
    """
    import datetime
    try:
        dt = datetime.datetime.strptime(date_str.strip(), "%d.%m.%Y")
        return dt.timestamp()
    except Exception:
        raise ValueError("Некорректный формат даты. Используйте дд.мм.гггг")

def read_file(file_path: str) -> list[list[str]]:
    if not os.path.exists(file_path):
        # Создать пустой файл, если не существует
        with open(file_path, 'x', encoding='utf-8'):
            pass
    with open(file_path, 'r', encoding='utf-8') as file:
        return list(csv.reader(file))

def write_to_file(file_path: str, rows: Iterable[list[str]]):
    with open(file_path, 'w+', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
