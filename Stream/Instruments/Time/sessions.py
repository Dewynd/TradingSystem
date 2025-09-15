import datetime
from time import utc_now


#  Сессии
#  Нью-Йоркская сессия
def time_opening_ny_exchange():
    if (utc_now() - datetime.timedelta(hours=4)).weekday() >= 5:
        return datetime.datetime.replace(utc_now(), day=utc_now().day + 7 - utc_now().weekday(), hour=13, minute=30,
                                         second=0, microsecond=0)
    return datetime.datetime.replace(utc_now(), day=utc_now().day + 1, hour=13, minute=30, second=0, microsecond=0)


def time_closing_ny_exchange():
    if (utc_now() - datetime.timedelta(hours=4)).weekday() >= 5:
        return datetime.datetime.replace(utc_now(), day=utc_now().day + 7 - utc_now().weekday(), hour=21, minute=0,
                                         second=0, microsecond=0)
    return datetime.datetime.replace(utc_now(), day=utc_now().day + 1, hour=21, minute=0, second=0, microsecond=0)


def time_before_opening_ny_exchange():
    return time_opening_ny_exchange() - utc_now()


def time_before_closing_ny_exchange():
    return time_closing_ny_exchange() - utc_now()


#  Гонконгская сессия
def time_opening_hk_exchange():
    if (utc_now() + datetime.timedelta(hours=8)).weekday() >= 5:
        return datetime.datetime.replace(utc_now(), day=utc_now().day + 7 - utc_now().weekday(), hour=1, minute=30,
                                         second=0, microsecond=0)
    return datetime.datetime.replace(utc_now(), day=utc_now().day + 1, hour=1, minute=30, second=0, microsecond=0)


def time_closing_hk_exchange():
    if (utc_now() + datetime.timedelta(hours=8)).weekday() >= 5:
        return datetime.datetime.replace(utc_now(), day=utc_now().day + 7 - utc_now().weekday(), hour=9, minute=0,
                                         second=0, microsecond=0)
    return datetime.datetime.replace(utc_now(), day=utc_now().day + 1, hour=9, minute=0, second=0, microsecond=0)


def time_before_opening_hk_exchange():
    return time_opening_hk_exchange() - utc_now()


def time_before_closing_hk_exchange():
    return time_closing_hk_exchange() - utc_now()


#  Лондонская сессия
def time_opening_ln_exchange():
    if utc_now().weekday() >= 5:
        return datetime.datetime.replace(utc_now(), day=utc_now().day + 7 - utc_now().weekday(), hour=9, minute=30,
                                         second=0, microsecond=0)
    return datetime.datetime.replace(utc_now(), day=utc_now().day + 1, hour=9, minute=30, second=0, microsecond=0)


def time_closing_ln_exchange():
    if utc_now().weekday() >= 5:
        return datetime.datetime.replace(utc_now(), day=utc_now().day + 7 - utc_now().weekday(), hour=17, minute=0,
                                         second=0, microsecond=0)
    return datetime.datetime.replace(utc_now(), day=utc_now().day + 1, hour=17, minute=0, second=0, microsecond=0)


def time_before_opening_ln_exchange():
    return time_opening_ln_exchange() - utc_now()


def time_before_closing_ln_exchange():
    return time_closing_ln_exchange() - utc_now()


#  Гонконгская сессия
def time_opening_ft_exchange():
    if (utc_now() + datetime.timedelta(hours=1)).weekday() >= 5:
        return datetime.datetime.replace(utc_now(), day=utc_now().day + 7 - utc_now().weekday(), hour=8, minute=30,
                                         second=0, microsecond=0)
    return datetime.datetime.replace(utc_now(), day=utc_now().day + 1, hour=8, minute=30, second=0, microsecond=0)


def time_closing_ft_exchange():
    if (utc_now() + datetime.timedelta(hours=1)).weekday() >= 5:
        return datetime.datetime.replace(utc_now(), day=utc_now().day + 7 - utc_now().weekday(), hour=16, minute=0,
                                         second=0, microsecond=0)
    return datetime.datetime.replace(utc_now(), day=utc_now().day + 1, hour=16, minute=0, second=0, microsecond=0)


def time_before_opening_ft_exchange():
    return time_opening_ft_exchange() - utc_now()


def time_before_closing_ft_exchange():
    return time_closing_ft_exchange() - utc_now()