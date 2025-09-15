from abc import ABC, abstractmethod
from Stream.Instruments.market import Timeframe
from Stream.Strategy.pairs import *
import asyncio


class Market(ABC):
    def __init__(self, market_name):
        self._market_name = market_name
    @property
    @abstractmethod
    def timeframes(self):
        pass

    def has_timeframe(self, timeframe):
        return str(timeframe) in self.timeframes

    @property
    def market_name(self):
        return self._market_name



class MarketInteractor(ABC):
    def __init__(self, market: Market):
        self._market = market

    @abstractmethod
    async def get_candlestick_data(self, pair: Pair, timeframe, limit=100, start_time=None):
        pass

    @abstractmethod
    async def get_current_price(self, symbol):
        pass

    @abstractmethod
    def get_candlestick_data_from_timestamp_to_timestamp(self, pair: Pair, timeframe:Timeframe="15m", start_timestamp=100000000, end_timestamp=100000000):
        pass

    @abstractmethod
    def place_order(self, pair: Pair, order_side, order_type, position_side, margin, price=None):
        pass

    @abstractmethod
    async def was_order_filled(self, order_id):
        pass


async def safe_call(func, *args, retries=60, base_sleep=10, **kwargs):
    for i in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            time_sleep = i * 3 + base_sleep
            print(f"Exception: {e}. Sleeping for {time_sleep} seconds")
            await asyncio.sleep(time_sleep)

    raise Exception(f"Error in safe_call wrapper. Retries: {retries}")