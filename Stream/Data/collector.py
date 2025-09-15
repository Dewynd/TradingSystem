import asyncio
import random

import numpy as np
import requests
from Stream.Data.Candle import Candle
from Stream.Data.Data import Metadata, Data
from Stream.Instruments.Time.time import timestamp_now, convert_timestamp
def get_candles(pair, interval="15m", limit=200, start_time=None):
    if start_time:
        start_time *= 1000
        request = f"https://api.binance.com/api/v3/klines?symbol={pair}&interval={interval}&startTime={start_time}&limit={limit}"
    else:
        request = f"https://api.binance.com/api/v3/klines?symbol={pair}&interval={interval}&limit={limit}"
    response = requests.get(request)
    if response.status_code == 200:
        data_ = response.json()
        data = []
        for row in data_:
            data.append([float(x) for x in row[:6]])
        return data
    else:
        return None


from abc import ABC, abstractmethod
import aiohttp
from Stream.Instruments.market import Timeframe

class Collector(ABC):
    def __init__(self):
        self._session = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    @abstractmethod
    async def get_candlestick_data(self, pair, timeframe: Timeframe, limit=200, start_time=None):
        pass

class OkxCollector(Collector):
    base_address = "https://www.okx.com"

    def get_url(self, pair, timeframe: Timeframe = Timeframe("1m"), limit=100, start_time=None):
        start_time_part = f"&after={start_time}" if start_time is not None else ""
        if limit == None:
            limit = 100
        url = f'{self.base_address}/api/v5/market/history-mark-price-candles?instId={pair}&bar={str(timeframe)}&limit={limit}{start_time_part}'
        return url

    async def get_candlestick_data(self, pair, timeframe: Timeframe = Timeframe("1m"), limit=100, start_time=None):
        url = self.get_url(pair, timeframe, limit, start_time)
        async with self._session.get(url) as response:
            html = await response.json()
            return html

    async def get_candlestick_data_by_url(self, url, proxy=None):
        if proxy is None:
            async with self._session.get(url) as response:
                html = await response.json()
                return html
        else:
            async with self._session.get(url, proxy=proxy) as response:
                html = await response.json()
                return html

class DataCollector:
    async def get_candlestick_data(market, pair, timeframe: Timeframe = Timeframe("1m"), limit=100, start_time=None):
        async with OkxCollector() as okx:
            raw_data = []
            start_time *= 1000

            while (limit is not None and limit > 0) or (limit is None and start_time < timestamp_now()*1000):
                print(convert_timestamp(start_time))
                raw_data_part = (await okx.get_candlestick_data(pair, timeframe, min(limit if limit is not None else 100, 100), start_time))["data"][::-1]
                raw_data.extend(raw_data_part)
                if limit is not None:
                    limit -= 100
                start_time += timeframe.milliseconds * 100
            candle_data = np.array(raw_data, dtype=float)
            metadata = Metadata(pair.split("-")[0], pair.split("-")[1], timeframe)
            data = Data(candle_data, metadata)
            return data

    async def candlestick_parser(urls, responces, session, proxy):
        while len(urls) > 0:
            print(f"{len(responces)}/{len(urls)}")
            id = random.choice(list(urls.keys()))
            url = urls[id]

            resp = (await session.get_candlestick_data_by_url(url, proxy))["data"][::-1]
            print(resp)
            if id in urls.keys():
                del urls[id]
            responces[id] = resp

    @classmethod
    async def get_candlestick_data_f(cls, market, pair, timeframe: Timeframe = Timeframe("1m"), limit=100, start_time=None, proxies=None):
        urls = {}
        responces = {}
        async with OkxCollector() as okx:
            raw_data = []
            start_time *= 1000
            i = 0
            while (limit is not None and limit > 0) or (limit is None and start_time < timestamp_now()*1000):
                url = okx.get_url(pair, timeframe, limit, start_time)
                urls[i] = url
                if limit is not None:
                    limit -= 100
                start_time += timeframe.milliseconds * 100
                i += 1
            tasks = []
            for proxy in proxies:
                task = asyncio.create_task(cls.candlestick_parser(urls, responces, okx, proxy))
                tasks.append(task)
            await asyncio.gather(*tasks)
            print(len(urls))
            print(responces)
            for i in range(len(responces)):
                raw_data.extend(responces[i])
            candle_data = np.array(raw_data, dtype=float)
            metadata = Metadata(pair.split("-")[0], pair.split("-")[1], timeframe)
            data = Data(candle_data, metadata)
            return data