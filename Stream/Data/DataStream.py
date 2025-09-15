from Stream.Data.Data import Data, Metadata
import numpy as np
from Stream.Instruments.market import Timeframe


def save_data(data: Data, filepath):
    """
    Сохраняет данные в текстовый файл с заданным форматом.

    Аргументы:
        data (Data): Исходные свечные данные.
        filepath (str): Путь к файлу для сохранения.
    """
    with open(filepath, 'w') as f:
        f.write(f"{data.metadata}\n")  # Записываем метаинформацию
        f.write("timestamp open high low close volume\n")  # Записываем заголовки

        # Записываем строки данных
        np.savetxt(f, data.candle_data, fmt='%s', delimiter=' ')

    print(f"Данные сохранены в {filepath}")


def load_data(filepath, limit=None):
    """
    Загружает данные из текстового файла.

    Аргументы:
        filepath (str): Путь к файлу для загрузки.
        limit (int, optional): Количество строк данных для загрузки с конца файла.

    Возвращает:
        Data: Объект с загруженными свечными данными.
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()

    meta_info = lines[0].strip().split(":")  # Первая строка - метаинформация
    data_lines = lines[2:]  # Пропускаем метаинформацию и заголовки

    if limit is not None:
        data_lines = data_lines[-limit:]

    # Загружаем данные в numpy-массив
    data_array = np.loadtxt(data_lines, dtype=float)

    return Data(data_array, Metadata(meta_info[0], meta_info[1], Timeframe(meta_info[2])))
