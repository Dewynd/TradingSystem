class TradingAction:
    def __init__(self, timestamp):
        self._timestamp = timestamp

    @property
    def timestamp(self):
        return self._timestamp


class OrderAction(TradingAction):
    def __init__(self, timestamp, margin, order_title, id):
        self._order_title = order_title
        self._margin = margin
        self._id = id
        super().__init__(timestamp)

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._order_title

    @property
    def margin(self):
        return self._margin


class OrderCreated(OrderAction):
    def __init__(self, timestamp, order_type, order_side, order_price, margin, order_title, id, trade_id):
        self._order_price = order_price
        self._order_type = order_type
        self._order_side = order_side
        self._trade_id = trade_id
        super().__init__(timestamp, margin, order_title, id)

    @property
    def order_type(self):
        return self._order_type

    @property
    def order_side(self):
        return self._order_side

    @property
    def order_price(self):
        return self._order_price

    @property
    def trade_id(self):
        return self._trade_id


class OrderExecuted(OrderAction):
    def __init__(self, timestamp, order_price, margin, order_title, id):
        self._order_price = order_price
        super().__init__(timestamp, margin, order_title, id)

    @property
    def order_price(self):
        return self._order_price


class TradeAction(TradingAction):
    def __init__(self, timestamp, margin, price, id):
        self._margin = margin
        self._id = id
        self._price = price
        super().__init__(timestamp)

    @property
    def id(self):
        return self._id

    @property
    def price(self):
        return self._price

    @property
    def margin(self):
        return self._margin


class TradeOpened(TradeAction):
    def __init__(self, trade_type, timestamp, margin, price, id):
        self._trade_type = trade_type
        super().__init__(timestamp, margin, price, id)

    @property
    def trade_type(self):
        return self._trade_type


class TradeClosed(TradeAction):
    def __init__(self, timestamp, margin, price, id, title=""):
        self.title=title
        super().__init__(timestamp, margin, price, id)


class TradeMarginAdded(TradeAction):
    def __init__(self, timestamp, margin, price, id):
        super().__init__(timestamp, margin, price, id)


class TradeMarginReduced(TradeAction):
    def __init__(self, timestamp, margin, price, id):
        super().__init__(timestamp, margin, price, id)