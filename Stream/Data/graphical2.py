import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
from Stream.Data.Data import Data
import pandas as pd

class Graph:
    def __init__(self, data):
        self.data = data

    def plot_candlestick(self):
        # Определяем количество столбцов (есть ли объем)
        num_columns = self.data.shape[1]
        if num_columns == 6:
            columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        elif num_columns == 5:
            columns = ['Date', 'Open', 'High', 'Low', 'Close']
        else:
            raise ValueError(f"Unexpected number of columns: {num_columns}")

        # Преобразуем numpy в DataFrame
        df = pd.DataFrame(self.data, columns=columns)

        # Преобразуем столбец Date в формат datetime и установим индекс
        df['Date'] = pd.to_datetime(df['Date'], unit='ms')
        df.set_index('Date', inplace=True)

        # Определяем, есть ли объем
        volume_present = 'Volume' in df.columns

        # Создаем фигуру и оси
        fig, (ax, ax_volume) = plt.subplots(2, gridspec_kw={'height_ratios': [3, 1]}, figsize=(10, 6), sharex=True)

        # Рисуем график
        mpf.plot(df, type='candle', ax=ax, volume=ax_volume if volume_present else None, style='yahoo')

        # Функция для отображения координат
        def format_coord(x, y):
            try:
                index = int(round(x))  # Приводим x к целому числу
                if 0 <= index < len(df):
                    candle = df.iloc[index]  # Доступ к строке по позиции
                    return (f"ind={x:.2f}, prc={y:.2f} | "
                            f"time={candle.name} | "  # Дата будет в name, так как индекс — datetime
                            f"opn={candle['Open']:.2f}, cls={candle['Close']:.2f}, "
                            f"pch={np.round((candle['Close'] - candle['Open']) / candle['Open'] * 100, 3)}%")
                else:
                    return f"x={x:.2f}, y={y:.2f}"
            except Exception as e:
                return f"x={x:.2f}, y={y:.2f} (Error: {str(e)})"

        ax.format_coord = format_coord

        plt.show()

    def pldot_candlestick(self):



        if isinstance(self.data, Data):
            df = self.data.candle_data
        else:
            df = self.data
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        # Создаем фигуру и оси
        fig, (ax, ax_volume) = plt.subplots(2, gridspec_kw={'height_ratios': [3, 1]}, figsize=(10, 6), sharex=True)

        # Рисуем свечной график
        mpf.plot(pd.DataFrame(df, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume']),
                 type='candle', ax=ax, volume=ax_volume, style='yahoo')

        candles_data = df

        def format_coord(x, y):
            try:
                index = int(round(x))
                if 0 <= index < len(candles_data):
                    candle = candles_data[index]
                    return (f"x={x:.2f}, y={y:.2f} | "
                            f"Time={candle[0]} | "
                            f"Open={candle[1]:.2f}, Close={candle[4]:.2f}, "
                            f"Pch={np.round((candle[4] - candle[1]) / candle[1] * 100, 3)}%")
                else:
                    return f"x={x:.2f}, y={y:.2f}"
            except:
                return f"x={x:.2f}, y={y:.2f}"

        ax.format_coord = format_coord
        plt.show()
