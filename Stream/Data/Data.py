import numpy as np
from Stream.Data.Candle import Candle
from Stream.Instruments.market import Timeframe


class Metadata:
    def __init__(self, currency_1, currency_2, timeframe: Timeframe):
        self.__currency_1 = currency_1
        self.__currency_2 = currency_2
        self.__timeframe = timeframe

    @property
    def timeframe(self):
        return self.__timeframe

    @property
    def currency_1(self):
        return self.__currency_1

    @property
    def currency_2(self):
        return self.__currency_2

    def __str__(self):
        return f"{self.__currency_1}:{self.__currency_2}:{self.__timeframe}"


class Data:
    """
    Класс хранящий свечную информацию
    """

    def __init__(self, candle_data: np.ndarray, metadata: Metadata = None):
        self.__candle_data = candle_data
        self.__metadata = metadata

    def __len__(self):
        return len(self.__candle_data)

    def __getitem__(self, item):
        return self.__candle_data[item]

    def __setitem__(self, item, value):
        self.__candle_data[item] = value

    def remove(self, i):
        self.__candle_data = np.delete(self.__candle_data, i, axis=0)

    def remove_last(self, x: int):
        """
        Removing last x candlestick data's rows
        """
        self.__candle_data = self.__candle_data[:-x]

    def candle(self, item) -> Candle:
        return Candle(self.__candle_data[item])

    @property
    def metadata(self):
        return self.__metadata

    @property
    def candle_data(self):
        return self.__candle_data

    def expand_data(self, data):
        self.__candle_data = np.vstack([self.__candle_data, data])


class DataManager:
    @classmethod
    def convert_to_data(cls, data: Data, timeframe: Timeframe):
        if timeframe.seconds < data.metadata.timeframe.seconds:
            raise TypeError("Impossible to convert data from higher to lower timeframe.")
        elif timeframe.seconds % data.metadata.timeframe.seconds != 0:
            raise TypeError("Impossible to convert data from non multiplies timeframes")

        factor = timeframe.seconds // data.metadata.timeframe.seconds
        if factor <= 1:
            return data

        df = data.candle_data.copy()
        df[:, 0] = (df[:, 0] // (timeframe.seconds * 1000)) * (timeframe.seconds * 1000)

        unique_timestamps = np.unique(df[:, 0])
        new_data = []
        for timestamp in unique_timestamps:
            subset = df[df[:, 0] == timestamp]
            new_candle = [
                timestamp,
                subset[0, 1],
                np.max(subset[:, 2]),
                np.min(subset[:, 3]),
                subset[-1, 4],
                np.sum(subset[:, 5])
            ]
            new_data.append(new_candle)

        return Data(np.array(new_data), Metadata(data.metadata.currency_1, data.metadata.currency_2, timeframe))
