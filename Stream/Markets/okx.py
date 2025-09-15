import asyncio
import time

import requests
import pandas as pd
from Stream.Markets.market import Market, MarketInteractor, safe_call
from Stream.Data.Data import Candle
from Stream.Instruments.market import Timeframe
from Stream.Strategy.orders import PlacedOrder
from Stream.Strategy.pairs import *


class OKXMarket(Market):
    def __init__(self):
        super().__init__("OKX")

    @property
    def timeframes(self):
        return ["1s", "1m", "5m", "15m", "30m", "1h"]

    def __str__(self):
        return self._market_name


class OKXInteractor(MarketInteractor):
    def __init__(self, market: OKXMarket, market_interactor, account, trade):
        self._market_interactor = market_interactor
        self._account = account
        self._trade = trade
        super().__init__(market)

    async def set_leverage(self, pair:Pair, leverage):
        print(await safe_call(self._account.set_leverage, instId=f"{pair.symbol}-{pair.symbol2}-SWAP", lever=f"{leverage}", mgnMode="cross"))

    async def get_candlestick_data(self, pair: Pair, timeframe, limit=100, start_time=None):
        result = await safe_call(self._market_interactor.get_candlesticks, f'{pair.symbol}-{pair.symbol2}-SWAP', limit=limit, bar=timeframe)
        if result['code'] == '0':
            RawData = result['data']

            # Преобразуем данные в список, где каждая свеча это список значений [timestamp, open, high, low, close, volume]
            candlestick_data = [
                [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])]
                for row in RawData[::-1]
            ]

            return candlestick_data
        return None

    async def get_current_price(self, pair: Pair):
        result = await safe_call(self._market_interactor.get_candlesticks, f'{pair.symbol}-{pair.symbol2}-SWAP', limit=1)
        if result['code'] == '0':
            return float(result['data'][0][4])
        return False

    async def get_tick_size(self, pair: Pair):
        result = await safe_call(self._account.get_instruments, 'SWAP', instId=f'{pair.symbol}-{pair.symbol2}-SWAP')
        if result['code'] != '0':
            print(result)
            print("ERRRORR")
            return False
        return float(result['data'][0]['lotSz'])

    async def place_order(self, pair: Pair, order_side, order_type, position_side, margin, trading_mode="cross", price=None, stoploss=None):
        enter_price = await self.get_current_price(pair)
        tick_size = await self.get_tick_size(pair)
        size = margin / enter_price
        size = round(size / tick_size, 0)
        size = int(size) * tick_size
        size = round(size, 8)
        if not order_type in ("move_order_stop",):
            if order_type == "market":
                res = await safe_call(self._trade.place_order, instId=f'{pair.symbol}-{pair.symbol2}-SWAP', tdMode=trading_mode, side=order_side, posSide=position_side, ordType=order_type,
                        sz=f'{size}')
            else:
                res = await safe_call(self._trade.place_order, instId=f'{pair.symbol}-{pair.symbol2}-SWAP', tdMode=trading_mode, side=order_side,
                                        posSide=position_side, ordType=order_type,
                                        sz=f'{size}', px=f"{price}")
            print(res)
            if res["code"] == '0':
                return res["data"][0]["ordId"]
            else:
                raise Exception(f"Error during placing an order. Data: {res}")
        else:
            res = await safe_call(self._trade.place_algo_order,
                instId=f'{pair.symbol}-{pair.symbol2}-SWAP',
                tdMode='cross',
                side='sell',
                ordType='move_order_stop',  # Тип ордера для трейлинг-стопа
                sz=f'{size}',
                posSide='long',
                callbackRatio=f'{stoploss / 100}'
            )
            if res["code"] == '0':
                return res["data"][0]["algoId"]
            else:
                msg = f"Error during placing an order. Data: {res}"
                raise Exception(msg)

    async def remove_order(self, pair: Pair, order_id, type="default"):
        print("removing order")
        if type == "default" or 1 == 1:
            await safe_call(self._trade.cancel_order, instId=f'{pair.symbol}-{pair.symbol2}-SWAP',
                                     ordId=order_id)
            algo_orders = [{"instId": f'{pair.symbol}-{pair.symbol2}-SWAP', "algoId": f"{order_id}"}]
            await safe_call(self._trade.cancel_algo_order, algo_orders)
        print("removed order?")

    async def was_order_filled(self, placed_order: PlacedOrder):
        data = {'code': '1'}
        for i in range(5):
            try:
                data = self._trade.get_order(f'{placed_order.pair.symbol}-{placed_order.pair.symbol2}-SWAP', ordId=placed_order.order_id)
                break
            except:
                await asyncio.sleep(10)
                print("WAS ERROR ON API filled order")
        if data['code'] == '0':
            if data['data'][0]['state'] == 'filled':
                return True
        return False

    def get_candlestick_data_from_timestamp_to_timestamp(self, currency_1, currency_2, timeframe: Timeframe = "15m",
                                                         start_timestamp=100000000, end_timestamp=100000000):
        pass

    def cancel_all_orders(self, client, instId: str = None):
        # 1. Получаем список ордеров
        res = client.get_orders_pending()  # или без instId для всех
        if res.get("code") != "0":
            print("Ошибка получения ордеров:", res)
            return

        orders = res.get("data", [])
        print(f"Найдено {len(orders)} открытых ордеров")

        # 2. Отменяем
        for o in orders:
            order_id = o["ordId"]
            inst_id = o["instId"]
            r = client.cancel_order(instId=inst_id, ordId=order_id)
            print("Cancel", inst_id, order_id, "→", r)

    async def cancel_all_algo_orders(self):
        orders_list = await self.get_algo_order_list()
        orders = []
        for order in orders_list:
            orders.append({"instId": order["instId"], "algoId": order["algoId"]})
        batch_start_index = 0
        print(orders_list)
        while batch_start_index < len(orders):
            result = await safe_call(self._trade.cancel_algo_order, orders[batch_start_index:batch_start_index + 20])
            print(result)
            batch_start_index += 20

    async def get_algo_order_list(self):
        # Retrieve a list of untriggered one-way stop orders
        result = await safe_call(self._trade.order_algos_list, ordType="move_order_stop")
        return result["data"]
