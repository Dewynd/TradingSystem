import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
from Stream.Data.Data import Data

class Graph:
    def __init__(self, data):
        self.data = data

    def plot_candlestick(self):
        # Допустим, self.data.candle_data — это NumPy-массив формата:
        # [[timestamp, open, high, low, close, volume], ...]

        if isinstance(self.data, Data):
            raw_data = self.data.candle_data.copy()
        else:
            raw_data = self.data.copy()

        # Преобразуем в Pandas DataFrame
        arr = np.array(raw_data, dtype=float)  # или dtype=np.float64
        df = pd.DataFrame(arr, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
        df.set_index("timestamp", inplace=True)

        # График
        mpf.plot(df, type='candle', style='yahoo', volume=True,
                 title='Свечной график', ylabel='Цена', ylabel_lower='Объем')
