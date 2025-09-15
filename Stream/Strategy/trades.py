from Stream.Strategy.orders import Order

class Trade:
    def __init__(self, position_type, margin, open_price, open_time, title="Trade", id=None):
        self._title = title
        self._position_type = position_type
        self._margin = margin
        self._open_price = open_price
        self._open_time = open_time
        self._id = id
        self._orders = []

    @property
    def title(self):
        return self._title

    @property
    def id(self):
        return self._id

    @property
    def orders(self):
        return self._orders

    @property
    def margin(self):
        return self._margin

    @property
    def position_type(self):
        return self._position_type

    def process_order(self, order: Order):
        if self._position_type == "long":
            if order.order_side == "buy":
                self._margin += order.margin
            else:
                self._margin = max(0, self._margin-order.margin)
        else:
            if order.order_side == "sell":
                self._margin += order.margin
            else:
                self._margin = max(0, self._margin-order.margin)

    def is_position_closed(self):
        if self._margin <= 0:
            return True
        else:
            return False

    def add_order(self, order):
        self._orders.append(order)

    def remove_order(self, order):
        self._orders.remove(order)


class TrackableTrade(Trade):
    def __init__(self, position_type, margin, open_price, open_time, title="Trade", id=None, track_function=None):
        self._track_function = track_function
        self._data = {}
        super().__init__(position_type, margin, open_price, open_time, title="Trade", id=None)

    async def step(self, *args, **kwargs):
        await self._track_function(*args, **kwargs)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data