class BaseModifycator:
    def __init__(self, modify_function=None, title="Modifycator"):
        self._title = title
        self._values = []
        self._system_values = []
        self._modify_function = modify_function

    @property
    def title(self):
        return self._title

    @property
    def values(self):
        return self._values

    def value(self, item):
        return self._values[item]

    def system_value(self, item):
        return self._system_values[item]

    @property
    def system_values(self):
        return self._system_values

    def __getitem__(self, item):
        return self._values[item]


class Modifycator(BaseModifycator):
    def __init__(self, modify_function=None, title="Modifycator"):
        super().__init__(modify_function, title)

    def run(self, data):
        self._values = []
        for i in range(len(data)):
            self._values.append(self._modify_function(i))

    def update_values(self, data):
        for i in range(len(data)):
            self._values.append(self._modify_function(i))


class Indicator(BaseModifycator):
    def __init__(self, modify_function=None, title="Modifycator"):
        self._strategy = None
        super().__init__(modify_function, title)

    def add_to_strategy(self, strategy):
        self._strategy = strategy
        self.run()

    def run(self):
        if self._strategy.data is None:
            return False
        for i in range(len(self._strategy.data)):
            value, system_value = self._modify_function(i)
            self._values.append(value)
            self._system_values.append(system_value)

    def update_values(self, data):
        for i in range(len(data)):
            value, system_value = self._modify_function(i)
            self._values.append(value)
            self._system_values.append(system_value)

    def update_value(self, i):
        self._values[i], self._system_values[i] = self._modify_function(i)

    def complement_values(self):
        self._strategy.logger.log(f"Complementing indicator's values")
        if self._strategy.data is None:
            self._strategy.logger.log(f"Complementing values cancelled because self._strategy.data is None")
            return False
        if len(self._values) == len(self._strategy.data):
            self._strategy.logger.log(f"Values already complemented")
            return True
        elif len(self._values) > len(self._strategy.data):
            self._strategy.logger.log("Length of modifier data > data so recalculating modifier data")
            self.update_values(self._strategy.data)
        for i in range(len(self._values), len(self._strategy.data)):
            value, system_value = self._modify_function(i)
            self._values.append(value)
            self._system_values.append(system_value)
            self._strategy.logger.log(f"Values complementing to data")


class ClassicRSI(Indicator):
    def __init__(self, range=14, title="RSI"):
        self._range = range
        super().__init__(self.rsi, title=title)

    def rsi(self, i):
        if i < self._range - 1:
            return 0
        else:
            sum_up = 0
            sum_down = 0
            for j in range(i-self._range+1, i+1):
                if self._strategy.data.candle(j).is_bullish():
                    sum_up += self._strategy.data.candle(j).body.size()
                else:
                    sum_down += abs(self._strategy.data.candle(j).body.size())
            rs = sum_up/(sum_down if sum_down != 0 else 10**-12)
            RSI = 100 - 100/(1+rs)
            return RSI, None


class RSI(Indicator):
    def __init__(self, range=14, title="RSI"):
        self._range = range
        super().__init__(self.rsi, title=title)

    @property
    def range(self):
        return self._range

    def rsi(self, i):
        if i < self._range - 1:
            return None, None
        elif i == self._range -1:
            sum_up = 0
            sum_down = 0
            for j in range(i-self._range+1, i+1):
                if self._strategy.data.candle(j).is_bullish():
                    sum_up += self._strategy.delta_from(j)
                else:
                    sum_down += abs(self._strategy.delta_from(j))
            avg_gain = sum_up / self._range
            avg_loss = sum_down / self._range
            if avg_loss == 0:
                RSI = 100
            else:
                RS = avg_gain/avg_loss
                RSI = 100 - 100/(1+RS)
            return RSI, [avg_gain, avg_loss]  # Сохраняем avg_gain и avg_loss в system_values для дальнейшего использования в вычислениях
        else:
            change = self._strategy.data.candle(i).body.size()
            avg_gain, avg_loss = self._system_values[i-1]

            gain = max(change, 0)
            loss = max(-change, 0)

            avg_gain = (avg_gain * (self._range - 1) + gain) / self._range
            avg_loss = (avg_loss * (self._range - 1) + loss) / self._range

            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - 100 / (1 + rs)
            return rsi, [avg_gain, avg_loss]


class Stochastic(Indicator):
    def __init__(self, length, k_smoothing, d_smoothing, title="Stochastic"):
        self._length = length
        self._k_smoothing = k_smoothing
        self._d_smoothing = d_smoothing
        super().__init__(self.stochastic, title=title)

    def stochastic(self, i):
        if i-self._length+1<0:
            return [None, None], [None]

        # Находим наибольшее и наименьшее значения за период
        lowest_of_period = float("inf")
        highest_of_period = -float("inf")
        for j in range(i-self._length+1, i+1):
            highest_of_period = max(highest_of_period, self._strategy.data.candle(j).high)
            lowest_of_period = min(lowest_of_period, self._strategy.data.candle(j).low)

        # Высчитываем процент нахождения цены относительно диапазона т.е. % на котором находится цена в диапазоне
        # от наименьшей цены диапазона до наибольшей, где наибольшая=100% и наименьшая=0%
        percentage_k = ((self._strategy.data.candle(i).close) - lowest_of_period) / (highest_of_period - lowest_of_period) * 100
        if i-self._length-self._k_smoothing+2 < 0:
            return [None, None], [percentage_k]

        # Высчитываем сглаженное значение %k. Складываем последние ``self._k_smoothing`` percentage_k значения
        summ_of_percentage_k = percentage_k
        for j in range(i-self._k_smoothing+1, i):
            summ_of_percentage_k += self._system_values[j][0]
        sma_percentage_k = summ_of_percentage_k / self._k_smoothing

        if i-self._length-self._k_smoothing-self._d_smoothing+3 < 0:
            return [sma_percentage_k, None], [percentage_k]

        summ_of_percentage_d = sma_percentage_k
        for j in range(i-self._d_smoothing+1, i):
            summ_of_percentage_d += self._values[j][0]
        sma_percentage_d = summ_of_percentage_d / self._d_smoothing
        return [sma_percentage_k, sma_percentage_d], [percentage_k]


class MACD(Indicator):
    def __init__(self, fast=12, slow=26, signal=9, title="MACD"):
        self._fast = fast
        self._slow = slow
        self._signal = signal
        super().__init__(self.macd, title=title)

    def ema(self, prev_ema, price, period):
        """Вычисляем EMA по формуле"""
        alpha = 2 / (period + 1)
        return (price - prev_ema) * alpha + prev_ema

    def macd(self, i):
        # Нужно минимум slow периодов для начала
        if i < self._slow - 1:
            return [None, None, None], [None, None, None]

        close_price = self._strategy.data.candle(i).close

        # На старте считаем SMA для EMA fast/slow
        if i == self._slow - 1:
            sum_fast = 0
            for j in range(i - self._fast + 1, i + 1):
                sum_fast += self._strategy.data.candle(j).close
            ema_fast = sum_fast / self._fast

            sum_slow = 0
            for j in range(i - self._slow + 1, i + 1):
                sum_slow += self._strategy.data.candle(j).close
            ema_slow = sum_slow / self._slow

            macd_line = ema_fast - ema_slow
            signal_line = macd_line  # стартовое значение = сам macd_line
            histogram = macd_line - signal_line
            return [macd_line, signal_line, histogram], [ema_fast, ema_slow, signal_line]

        # Берём предыдущие EMA
        prev_ema_fast, prev_ema_slow, prev_signal = self._system_values[i - 1]

        # Обновляем EMA fast и EMA slow
        ema_fast = self.ema(prev_ema_fast, close_price, self._fast)
        ema_slow = self.ema(prev_ema_slow, close_price, self._slow)

        macd_line = ema_fast - ema_slow
        signal_line = self.ema(prev_signal, macd_line, self._signal)
        histogram = macd_line - signal_line

        return [macd_line, signal_line, histogram], [ema_fast, ema_slow, signal_line]


class Mega(Indicator):
    def __init__(self, amount_of_candles_to_analise_mega, title="Mega"):
        self._amount_of_candles_to_analise_mega = amount_of_candles_to_analise_mega
        super().__init__(self.mega, title=title)

    @property
    def amount_of_candles_to_analise_mega(self):
        return self._amount_of_candles_to_analise_mega

    def mega(self, i):
        # Нужно минимум slow периодов для начала
        rsi_modifier = self._strategy.modifycator("RSI")
        if not (i >= (self._amount_of_candles_to_analise_mega + rsi_modifier.range) and isinstance(
                rsi_modifier.value(i - self._amount_of_candles_to_analise_mega), (int, float))):
            return None, None
        summ_of_gains = 0
        summ_of_losses = 0
        summ_of_rsi_gains = 0
        summ_of_rsi_losses = 0
        print("Свечи:")
        for j in range(i - self._amount_of_candles_to_analise_mega, i):
            self._strategy.logger.log(
                f"{self._strategy.data.candle(j)}, {self._strategy.delta_percentage_from(j)}, {rsi_modifier[j]}")


            candle = self._strategy.data.candle(j)
            if candle.is_bullish():
                summ_of_gains += self._strategy.delta_percentage_from(j)
                summ_of_rsi_gains += (rsi_modifier[j] - rsi_modifier[j - 1])
            else:
                summ_of_losses += self._strategy.delta_percentage_from(j)
                summ_of_rsi_losses += (rsi_modifier[j] - rsi_modifier[j - 1])
        self._strategy.logger.log(f"{summ_of_gains} {summ_of_rsi_gains}   {summ_of_losses} {summ_of_rsi_losses}")
        green_coef = summ_of_gains / summ_of_rsi_gains
        red_coef = summ_of_losses / summ_of_rsi_losses
        self._strategy.logger.log(f"Зеленый коэф: {green_coef}; Красный коэф: {red_coef}")
        coef = green_coef / red_coef
        return coef, None


class RelativeVolatilityIndex(Indicator):
    def __init__(self, length=10, title="RVI"):
        self._length = length
        super().__init__(self.rvi, title=title)

    @property
    def length(self):
        return self._length

    def rvi(self, i):
        if i < self._length:
            return None, None

        # изменения цен
        delta = self._strategy.data.candle(i).close - self._strategy.data.candle(i-1).close
        sigma = abs(delta)

        if delta > 0:
            sigma_up = sigma
            sigma_down = 0
        elif delta < 0:
            sigma_up = 0
            sigma_down = sigma
        else:
            sigma_up = 0
            sigma_down = 0

        # начальная инициализация (первые n баров)
        if i == self._length:
            avg_up = 0
            avg_down = 0
            for j in range(i - self._length + 1, i + 1):
                d = self._strategy.data.candle(j).close - self._strategy.data.candle(j-1).close
                s = abs(d)
                if d > 0:
                    avg_up += s
                elif d < 0:
                    avg_down += s
            avg_up /= self._length
            avg_down /= self._length
        else:
            prev_avg_up, prev_avg_down = self._system_values[i-1]
            avg_up = (prev_avg_up * (self._length - 1) + sigma_up) / self._length
            avg_down = (prev_avg_down * (self._length - 1) + sigma_down) / self._length

        rvi_value = 100 * avg_up / (avg_up + avg_down) if (avg_up + avg_down) != 0 else 50

        return rvi_value, [avg_up, avg_down]


class NewRelativeVolatilityIndex(Indicator):
    def __init__(self, length=10, title="RVI"):
        self._length = length
        super().__init__(self.rvi, title=title)

    @property
    def length(self):
        return self._length

    def stddev(self, values):
        """Стандартное отклонение"""
        mean = sum(values) / len(values)
        return (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5

    def rvi(self, i):
        if i < self._length:
            return None, None

        # считаем стандартное отклонение за период
        closes = [self._strategy.data.candle(j).close for j in range(i - self._length + 1, i + 1)]
        deltas = [closes[k] - closes[k - 1] for k in range(1, len(closes))]
        sigma = self.stddev(deltas)

        delta = closes[-1] - closes[-2]
        if delta > 0:
            sigma_up, sigma_down = sigma, 0
        elif delta < 0:
            sigma_up, sigma_down = 0, sigma
        else:
            sigma_up, sigma_down = 0, 0

        # инициализация
        if i == self._length:
            avg_up = 0
            avg_down = 0
            for j in range(i - self._length + 1, i + 1):
                d = self._strategy.data.candle(j).close - self._strategy.data.candle(j-1).close
                s = abs(d)
                if d > 0:
                    avg_up += s
                elif d < 0:
                    avg_down += s
            avg_up /= self._length
            avg_down /= self._length
        else:
            prev_avg_up, prev_avg_down = self._system_values[i-1]
            avg_up = (prev_avg_up * (self._length - 1) + sigma_up) / self._length
            avg_down = (prev_avg_down * (self._length - 1) + sigma_down) / self._length

        rvi_value = 100 * avg_up / (avg_up + avg_down) if (avg_up + avg_down) != 0 else 50
        return rvi_value, [avg_up, avg_down]

from Stream.Instruments.Time.time import convert_timestamp

class URelativeVolatilityIndex(Indicator):
    def __init__(self, length=10, title="RVI"):
        self._length = length
        super().__init__(self.rvi, title=title)

    @property
    def length(self):
        return self._length

    def stddev(self, values):
        """Стандартное отклонение"""
        mean = sum(values) / len(values)
        return (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5

    def rvi(self, i):
        if i < self._length:
            return None, None

        # берём массив цен закрытия за окно
        closes = [self._strategy.data.candle(j).close for j in range(i - self._length + 1, i + 1)]

        # стандартное отклонение за период (ключевой момент для OKX)
        sigma = self.stddev(closes)

        # изменение цены
        delta = closes[-1] - closes[-2]
        print(closes)

        if delta > 0:
            sigma_up, sigma_down = sigma, 0
        elif delta < 0:
            sigma_up, sigma_down = 0, sigma
        else:
            sigma_up, sigma_down = 0, 0

        # инициализация при первом доступном индексе
        if i == self._length:
            avg_up = sigma_up
            avg_down = sigma_down
        else:
            prev_avg_up, prev_avg_down = self._system_values[i - 1]
            avg_up = (prev_avg_up * (self._length - 1) + sigma_up) / self._length
            avg_down = (prev_avg_down * (self._length - 1) + sigma_down) / self._length

        # итоговое значение RVI
        rvi_value = 100 * avg_up / (avg_up + avg_down) if (avg_up + avg_down) != 0 else 50
        return [convert_timestamp(self._strategy.data.candle(i).timestamp), rvi_value], [avg_up, avg_down]
