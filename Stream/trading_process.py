import asyncio
import datetime

from Stream.Instruments.Time.time import timestamp_now
from Stream.Instruments.market import Timeframe
from Stream.Strategy.pairs import *
from Stream.Strategy.strategy import OnlineStrategy


class TradingProcess:
    def __init__(self, strategy: OnlineStrategy, pair: Pair, timeframe: Timeframe, timer=0.5):
        self._strategy = strategy
        self._pair = pair
        self._timeframe = timeframe
        self._timestamp = timestamp_now()
        self._timer = timer
        self._strategy.set_trading_object(self)
        self._candle_open_timestamp = self._timeframe.get_timestamp_of_next_opening()

    @property
    def pair(self):
        return self._pair

    @property
    def timeframe(self):
        return self._timeframe

    @property
    def strategy(self):
        return self._strategy

    @property
    def timestamp(self):
        return self._timestamp

    async def step(self, candlestick_data):
        self._timestamp = timestamp_now()
        self._strategy.logger.log("Шаг стратегии")
        if candlestick_data[-100][0] > self._strategy.data[-100][0]:  # Проверка если была закрыта свеча
            self._strategy.logger.log(f"Не совпадают -100 и -100 {candlestick_data[-100][0]} и {self._strategy.data[-100][0]}")
            search_indent = 1  # Первоначальный сдвиг поиска
            try:
                while True:  # Двигаемся до тех пор, пока timestamp новых данных не будет равен timestamp сохраненных данных
                    self._strategy.logger.log(f"Проверка совпадения: {search_indent}  {candlestick_data[-100][0]} и {self._strategy.data[-100 + search_indent][0]}")
                    if candlestick_data[-100][0] == self._strategy.data[-100 + search_indent][0]:
                        await self._strategy.step(candlestick_data[-100:], True,
                                                  renewed_amount=100 - search_indent)
                        # print("Обновлены данные")
                        self._candle_open_timestamp = self._timeframe.get_timestamp_of_next_opening()
                        break
                    search_indent += 1
            except Exception as e:
                print(e)
                self._strategy.logger.log(f"Problem: {e}")
                await self._strategy.step(candlestick_data[-100:], renewed_amount=99)
        elif candlestick_data[-100][0] == self._strategy.data[-100][0]:  # Свеча не была закрыта
            await self._strategy.step(candlestick_data[-100:], renewed_amount=100)
        else:
            print(f"Ебаный api опять прислал ошибочные данные")

    async def run(self):
        data = await self._strategy.interactor.get_candlestick_data(self._pair, str(self._timeframe))
        self._strategy.set_data(data)
        while True:
            # print(f"Получена новая цена: {price}")
            candlestick_data = (
                await self._strategy.interactor.get_candlestick_data(self._pair, str(self._timeframe)))
            await self.step(candlestick_data)
            await asyncio.sleep(self._timer)


class MultiTradingProcess:
    def __init__(self, timer=0.5, update_function=None):
        self._timer = timer
        self._trading_objects = []
        self._update_function = update_function

    def add_trading_process(self, trading_process):
        self._trading_objects.append(trading_process)

    def add_trading_processes(self, trading_processes):
        for trading_process in trading_processes:
            self._trading_objects.append(trading_process)

    async def run(self):
        #await self._trading_objects[0].strategy.interactor.cancel_all_algo_orders()
        data = await self._trading_objects[0].strategy.interactor.get_candlestick_data(self._trading_objects[0].pair, str(
            self._trading_objects[0].timeframe))
        for trading_object in self._trading_objects:
            trading_object.strategy.set_data(data)
        while True:
            print(datetime.datetime.utcnow())
            candlestick_data = (
                await self._trading_objects[0].strategy.interactor.get_candlestick_data(self._trading_objects[0].pair, str(
                    self._trading_objects[0].timeframe)))
            for trading_object in self._trading_objects:
                await trading_object.step(candlestick_data)
            if self._update_function is not None:
                await self._update_function()
            await asyncio.sleep(self._timer)
