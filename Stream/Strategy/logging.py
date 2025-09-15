from Stream.Strategy.history import *
from Stream.Instruments.Time.time import convert_timestamp

class Logger:
    def __init__(self, filepath, orders=True, trades=True, console=False):
        self.__logs = []
        self._log_orders = orders
        self._log_trades = trades
        self._filepath = filepath
        self._console = console
        self._strategy = None

        with open(self._filepath, "w", encoding='utf-8') as f:
            f.write("")

    def set_strategy(self, strategy):
        self._strategy = strategy

    def save(self, filepath):
        with open(filepath, "w", encoding='utf-8') as f:
            for log in self.__logs:
                f.write(f"{log}\n")

    def log(self, message, is_timestamp=True, use_seconds=True):
        if is_timestamp:
            message = f"[{convert_timestamp(self._strategy.timestamp, use_seconds)}] {message}"
        self.__logs.append(message)
        with open(self._filepath, "a", encoding='utf-8') as f:
            f.write(f"{message}\n")
        if self._console:
            print(f"{message}\n")

    def log_events(self, events, use_seconds=True):
        for event in events:
            if isinstance(event, OrderCreated) and self._log_orders:
                self.log(f'[{convert_timestamp(event.timestamp, use_seconds)}] Ордер {event.id} "{event.title}" типа {event.order_side} на {"покупку" if event.order_type == "buy" else "продажу"} создан на маржу {event.margin} по цене {event.order_price}', is_timestamp=False)
            elif isinstance(event, OrderExecuted) and self._log_orders:
                self.log(
                    f'[{convert_timestamp(event.timestamp, use_seconds)}] Ордер {event.id} "{event.title}" исполнен на маржу {event.margin} по цене {event.order_price}', is_timestamp=False)
            elif isinstance(event, TradeOpened) and self._log_trades:
                self.log(f'[{convert_timestamp(event.timestamp, use_seconds)}] Сделка {event.id} типа {event.trade_type} открыта по цене {event.price} на маржу {event.margin}', is_timestamp=False)
            elif isinstance(event, TradeClosed) and self._log_trades:
                self.log(
                    f'[{convert_timestamp(event.timestamp, use_seconds)}] Сделка {event.id} закрыта по цене {event.price} на маржу {event.margin}', is_timestamp=False)

    def clear_logs(self):
        self.__logs.clear()


class SmartLogger:
    def __init__(self, loggers:list, filepath):
        """
        loggers: list логгеров. От 0 логгера до последнего. В 0 логгер идут все события. Дальше в зависимости от настройки.
        """
        self._loggers = []
        for logger in loggers:
            self._loggers.append(Logger(filepath+'_'+logger+".txt"))

    def set_strategy(self, strategy):
        for logger in self._loggers:
            logger.set_strategy(strategy)

    def save(self, filepath):
        for logger in self._loggers:
            logger.save(filepath+'_'+logger+".txt")

    def log(self, message, is_timestamp=True, use_seconds=True, event_level=0):
        for logger_index in range(len(self._loggers)):
            if event_level >= logger_index:
                self._loggers[logger_index].log(message, is_timestamp, use_seconds)

    def log_events(self, events, use_seconds=True, events_level=0):
        for logger_index in range(len(self._loggers)):
            if events_level >= logger_index:
                self._loggers[logger_index].log_events(events, use_seconds)

    def clear_logs(self):
        for logger in self._loggers:
            logger.clear_logs()