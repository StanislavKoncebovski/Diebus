import math

# region EPOCS for various calendars
ARMENIAN_EPOCH = 201443
BALINESE_EPOCH = -1721279
CHINESE_EPOCH = -963099
COPTIC_EPOCH = 103605
EGYPTIAN_EPOCH = -272787
ETHIOPIC_EPOCH = 2796
FRENCH_REVOLUTIONARY_EPOCH = 654415
GREGORIAN_EPOCH = 1
HEBREW_EPOCH = -1373427
HINDU_EPOCH = -1132959
ISLAMIC_EPOCH = 227015
ISO_EPOCH = 1
JULIAN_DAY_EPOCH = -1721424.5
JULIAN_EPOCH = -1
MAYAN_LONG_COUNT_EPOCH = -1137142
MAYAN_HAAB_EPOCH = -1137490
MODIFIED_JULIAN_DAY_EPOCH = 678576
PERSIAN_EPOCH = 226896
TIBETAN_EPOCH = -46410
WESTERN_BAHAI_EPOCH = 673222
ZOROASTRIAN_EPOCH = 230638


# endregion

def ordinal_suffix(value: int) -> str:
    """
    Gets the ordinal suffix (English) for an integer number ("st" for those ending with 1 etc.)
    """
    value_string = str(value)

    match (value_string[-1]):
        case "1":
            suffix = "st" if value != 11 else "th"
        case "2":
            suffix = "nd" if value != 12 else "th"
        case "3":
            suffix = "rd" if value != 13 else "th"
        case _:
            suffix = "th"

    return suffix


def quotient(x: float, y: float) -> float:
    """
    Calculates the whole part of a ratio.
    :param x: The dividend.
    :param y: The divisor.
    :return: The result
    """
    return math.floor(x / y)


def int_quotient(x: float, y: float) -> int:
    """
    Calculates the whole part of a ratio as an integer number
    :param x: The dividend.
    :param y: The divisor.
    :return: The result
    """
    return int(quotient(x, y))


def fmod(x: float, y: float) -> float:
    """
    RDU (1.17): The The	remainder, or modulus, of decimal numbers.
    :rtype: object
    :param x: The first operand.
    :param y: The second operand.
    :return: The result of the operation.
    fmod(9, 5) = 4; fmod(-9, 5) = 1; fmod(9, -5) = -1; fmod(-9, -5) = -4.
    """
    return x - y * math.floor(x / y)


def amod(x: float, y: float) -> float:
    """
    RDU (1.29): Adjusted Remainder, a "function like mod with its values adjusted in such a	way
    that the modulus of	a multiple of the divisor is the divisor itself rather than 0".
    :param x: The first operand.
    :param y: The second operand.
    :return: The result of the operation.
    """
    return y + fmod(x, -y)


def max(i: int, j: int) -> int:
    """
    Maximum of two integers.
    :param i: Integer # 1.
    :param j: Integer # 2.
    :return: Result: max(i, j)
    """
    return i if i >= j else j


def fmax(x: float, y: float) -> float:
    """
    Maximum of two floats.
    :param x: Float # 1.
    :param y: Float # 2.
    :return: Result: max(x, y)
    """
    return x if x >= y else y


def is_leap_gregorian_year(gregorian_year: int) -> bool:
    """
    Determine whether a year is a leap year.
    Source: https://stackoverflow.com/questions/11621740/how-to-determine-whether-a-year-is-a-leap-year
    """
    return gregorian_year % 4 == 0 and (gregorian_year % 100 != 0 or gregorian_year % 400 == 0)


def is_leap_julian_year(julian_year: int) -> bool:
    """
    RDM (3.1), p.63.
    """
    jy4 = julian_year % 4
    return jy4 == 0 if julian_year > 0 else jy4 == 3


def is_leap_hebrew_year(year: int) -> bool:
    """
    RDM (7.3)
    :param year:
    :return:
    """
    if int(fmod((7 * year + 1), 19) < 7):
        return True
    else:
        return False


def datetime_data_to_moment(ymdhmsm: list[int]) -> float:
    """
    Converts a list of values containing the year, month, day, and optionally,
                                             hour, minute, second, and microsecond
    to an RD moment.
    :param ymdhmsm: List containing the values of the year, month, day, and, optionally,
                                                      hour, minute, second, and microsecond.
    :return: The RD value.
    """
    if len(ymdhmsm) < 3:
        raise IndexError

    year = ymdhmsm[0]
    month = ymdhmsm[1]
    day = ymdhmsm[2]

    rd = 365.0 * (year - 1) + math.floor((year - 1) / 4) - math.floor((year - 1) / 100) + math.floor((year - 1) / 400)
    rd += math.floor((367 * month - 362) / 12)

    if month > 2:
        if is_leap_gregorian_year(year):
            rd -= 1
        else:
            rd -= 2

    rd += day

    if len(ymdhmsm) >= 6:
        hour = ymdhmsm[3]
        minute = ymdhmsm[4]
        second = ymdhmsm[5]

        rd += hour / 24 + minute / (24 * 60) + second / (24 * 60 * 60)

    if len(ymdhmsm) >= 7:
        microsecond = ymdhmsm[6]
        rd += microsecond / (24 * 60 * 60 * 1000000)

    return rd


def day_of_week_from_moment(t: float) -> float:
    """
    RDM (1.39): Day of week from RD moment.
    :param t: The RD moment value.
    :return: The week's day number (0 == Sunday; 1 == Monday,..., 6 == Saturday).
    """
    return fmod(t, 7)


def k_day_on_or_before(t: float, k: int) -> float:
    """
    RDM (1.41): The k-th day of the week that falls in the 7-day period ending on the moment's date.
    :param t: The RD moment value.
    :param k: The number of the week's day.
    :return: The number of the day fulfilling the definition above.
    """
    return t - day_of_week_from_moment(t - k)


def k_day_before(t: float, k: int) -> float:
    """
    RDM (1.48): The k-th day of the week that falls in the 7-day period ending exclusively on the moment's date.
    :param t: The RD moment value.
    :param k: The number of the week's day.
    :return: The number of the day fulfilling the definition above.
    """
    return k_day_on_or_before(t - 1, k)


def k_day_after(t: float, k: int) -> float:
    """
    RDM (1.49): The k-th day of the week that falls in the 7-day period beginning exclusively with the moment's date.
    :param t: The RD moment value.
    :param k: The number of the week's day.
    :return: The number of the day fulfilling the definition above.
    """
    return k_day_on_or_before(t + 7, k)


def n_th_k_day(n: int, k: int, t: float):
    """
    RDM (2.28): The n-th repetition of the weekday number k after/before(+/-) a given Gregorian date.
    :param n: The number of the repetition.
    :param k: The number of the week's day.
    :param t: The moment of the Gregorian date.
    :return: The number of the date fulfilling the definition above.
    """
    if n > 0:
        return 7 * n + k_day_before(t, k)
    else:
        return 7 * n + k_day_after(t, k)


def julian_day_to_rate_die(jd: float) -> float:
    return jd + JULIAN_DAY_EPOCH


def julian_day_to_rata_die(jd: float) -> float:
    return int(math.floor(julian_day_to_rate_die(jd)))
