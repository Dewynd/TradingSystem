import numpy as np
from Stream.Strategy.pairs import *


class Order:
    def __init__(self, order_type, order_side, margin, trade=None, title="Order", id=None):
        self._title = title
        self._order_type = order_type
        self._order_side = order_side
        self._margin = margin
        self._trade = trade
        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def order_type(self):
        return self._order_type

    @property
    def order_side(self):
        return self._order_side

    @property
    def margin(self):
        return self._margin

    @property
    def trade(self):
        return self._trade

    def is_order_worked(self, candlestick_data: np.ndarray):
        pass


class LimitOrder(Order):
    def __init__(self, order_type, order_side, margin, logic, trade=None, title="Order", id=None):
        self._logic = logic
        super().__init__(order_type, order_side, margin, trade, title, id=id)

    @property
    def id(self):
        return self._id

    def is_order_worked(self, candlestick_data: np.ndarray):
        high, low = candlestick_data[2], candlestick_data[3]
        trigger_price = float(self._logic[1:])

        if self._logic[0] == ">":
            return trigger_price if high >= trigger_price else False
        else:
            return trigger_price if low <= trigger_price else False


class StoplossOrder(Order):
    def __init__(self, order_type, order_side, margin, stoploss, trade=None, title="StoplossOrder", id=None):
        self._stoploss = stoploss
        self._limit_price = None
        super().__init__(order_type, order_side, margin, trade, title, id=id)

    def is_order_worked(self, candlestick_data: np.ndarray):
        high, low = candlestick_data[2], candlestick_data[3]
        if self._limit_price is None:
            self._limit_price = high if self._order_side == "long" else low

        if self._order_side == "long":
            return self._limit_price * (1-self._stoploss/100) if low <= self._limit_price * (1-self._stoploss/100) else False
        else:
            return self._limit_price * (1+self._stoploss/100) if high >= self._limit_price * (1+self._stoploss/100) else False


class PlacedOrder(Order):
    def __init__(self, order_type, order_side, order_id, margin, pair: Pair, trade=None, title="Order"):
        self._order_id = order_id
        self._pair = pair
        super().__init__(order_type, order_side, margin, trade, title)

    @property
    def order_id(self):
        return self._order_id

    @property
    def id(self):
        return self._order_id

    @property
    def pair(self):
        return self._pair