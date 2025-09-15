import numpy as np

class Body:
    def __init__(self, open_price, close_price):
        self.__open = float(open_price)
        self.__close = float(close_price)

    def min(self):
        return min(self.__open, self.__close)

    def max(self):
        return max(self.__open, self.__close)

    def size(self):
        return self.__close - self.__open

    def percentage_size(self):
        return (self.__close - self.__open) / self.__open * 100

class Candle:
    def __init__(self, row):
        self.__timestamp, self.__open, self.__high, self.__low, self.__close, self.__volume = row

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def open(self):
        return self.__open

    @property
    def high(self):
        return self.__high

    @property
    def low(self):
        return self.__low

    @property
    def close(self):
        return self.__close

    @property
    def volume(self):
        return self.__volume

    @property
    def body(self):
        return Body(self.__open, self.__close)

    def is_bullish(self):
        return self.__close >= self.__open

    def is_bearish(self):
        return self.__close < self.__open

    def __str__(self):
        return f"{self.timestamp} {self.open} {self.high} {self.low} {self.close} {self.volume}"