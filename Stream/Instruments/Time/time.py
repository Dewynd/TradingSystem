from datetime import datetime, timezone, timedelta


# Файл с основными инструментальными функциями для работы с временем


def utc_timestamp_now() -> float:
    """
    Возвращает временную метку (timestamp), соответствующую текущему времени в UTC.

    :return: Текущая временная метка (float).
    """
    return datetime.timestamp(datetime.utcnow())


def timestamp_now() -> float:
    """
    Возвращает временную метку (timestamp), соответствующую текущему времени в текущем часовом поясе.

    :return: Текущая временная метка (float).
    """
    return datetime.timestamp(datetime.now())


def utc_now() -> datetime:
    """
    Возвращает текущее время в UTC в виде объекта datetime.

    :return: Объект datetime с текущим временем в UTC.
    """
    return datetime.utcnow()


def time_now() -> datetime:
    """
    Возвращает текущее локальное время.

    :return: Объект datetime с текущим локальным временем.
    """
    return datetime.now()


def to_timestamp(time: datetime) -> float:
    """
    Конвертирует объект datetime во временную метку (timestamp).

    :param time: Объект datetime.
    :return: Временная метка (float).
    """
    return datetime.timestamp(time)


def convert_to_timestamp(year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> int:
    """
    Преобразует заданные дату и время во временную метку (timestamp).

    :param year: Год.
    :param month: Месяц (1-12).
    :param day: День (1-31).
    :param hour: Часы (0-23). По умолчанию 0.
    :param minute: Минуты (0-59). По умолчанию 0.
    :param second: Секунды (0-59). По умолчанию 0.
    :return: Временная метка (float).
    """
    dt = datetime(year, month, day, hour, minute, second)
    return int(dt.timestamp())


def to_time(timestamp) -> datetime:
    """
    Конвертирует временную метку (timestamp) в объект datetime.

    :param timestamp: Временная метка (float).
    :return: Объект datetime.
    """
    try:
        return datetime.fromtimestamp(timestamp)
    except:
        raise TypeError("Error in converting timestamp to time. It seems that you are using milliseconds instead of seconds.")



def time_of_1m_closing() -> datetime:
    """
    Возвращает время закрытия текущей 1-минутной свечи.

    :return: Время закрытия в формате datetime.
    """
    return datetime.replace(utc_now(), minute=(utc_now().minute + 1), second=0, microsecond=0)


def time_of_3m_closing() -> datetime:
    """
    Возвращает время закрытия текущей 3-минутной свечи.

    :return: Время закрытия в формате datetime.
    """
    return datetime.replace(utc_now(), minute=3 * (utc_now().minute // 3 + 1), second=0, microsecond=0)


def time_of_5m_closing() -> datetime:
    """
    Возвращает время закрытия текущей 5-минутной свечи.

    :return: Время закрытия в формате datetime.
    """
    return datetime.replace(utc_now(), minute=5 * (utc_now().minute // 5 + 1), second=0, microsecond=0)


def time_of_15m_closing() -> datetime:
    """
    Возвращает время закрытия текущей 15-минутной свечи.

    :return: Время закрытия в формате datetime.
    """
    return datetime.replace(utc_now(), minute=15 * (utc_now().minute // 15 + 1), second=0, microsecond=0)


def time_of_1h_closing() -> datetime:
    """
    Возвращает время закрытия текущей часовой свечи.

    :return: Время закрытия в формате datetime.
    """
    return datetime.replace(utc_now(), hour=(utc_now().hour + 1), minute=0, second=0, microsecond=0)


def time_of_4h_closing() -> datetime:
    """
    Возвращает время закрытия текущей 4-часовой свечи.

    :return: Время закрытия в формате datetime.
    """
    return datetime.replace(utc_now(), hour=4 * (utc_now().hour // 4 + 1), minute=0, second=0, microsecond=0)


def time_of_1d_closing() -> datetime:
    """
    Возвращает время закрытия текущей дневной свечи.

    :return: Время закрытия в формате datetime.
    """
    return datetime.replace(utc_now(), day=utc_now().day + 1, hour=0, minute=0, second=0, microsecond=0)


def time_before_1m_closing() -> timedelta:
    """
    Возвращает время до закрытия текущей 1-минутной свечи.

    :return: Время в формате timedelta.
    """
    return time_of_1m_closing() - utc_now()


def time_before_3m_closing() -> timedelta:
    """
    Возвращает время до закрытия текущей 3-минутной свечи.

    :return: Время в формате timedelta.
    """
    return time_of_3m_closing() - utc_now()


def time_before_5m_closing() -> timedelta:
    """
    Возвращает время до закрытия текущей 5-минутной свечи.

    :return: Время в формате timedelta.
    """
    return time_of_5m_closing() - utc_now()


def time_before_15m_closing() -> timedelta:
    """
    Возвращает время до закрытия текущей 15-минутной свечи.

    :return: Время в формате timedelta.
    """
    return time_of_15m_closing() - utc_now()


def time_before_1h_closing() -> timedelta:
    """
    Возвращает время до закрытия текущей часовой свечи.

    :return: Время в формате timedelta.
    """
    return time_of_1h_closing() - utc_now()


def time_before_4h_closing() -> timedelta:
    """
    Возвращает время до закрытия текущей 4-часовой свечи.

    :return: Время в формате timedelta.
    """
    return time_of_4h_closing() - utc_now()


def time_before_1d_closing() -> timedelta:
    """
    Возвращает время до закрытия текущей дневной свечи.

    :return: Время в формате timedelta.
    """
    return time_of_1d_closing() - utc_now()


def convert_timestamp(timestamp: float, seconds=False) -> str:
    """
    Конвертирует Unix-временную метку в строку, содержащую дату и время в UTC.

    :param timestamp: Временная метка (float).
    :return: Строка в формате 'YYYY-MM-DD HH:MM:SS UTC'.
    """
    if not seconds:
        timestamp = timestamp / 1000
    dt_object = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S %Z')
    return formatted_date


def timestamp_to_timedelta(timestamp):
    return timedelta(milliseconds=timestamp)


def performance_timer(func):
    """
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        time_start = time_now()
        func(*args, **kwargs)
        print(time_now()-time_start)

    return wrapper