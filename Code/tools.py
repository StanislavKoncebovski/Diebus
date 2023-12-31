import math
from typing import Callable

import numpy as np

# region Mathematical constants
DEGREE = math.pi / 180
DEFAULT_BRACKETING_FACTOR = 0.6180339887498948482045868343656
DEFAULT_MAX_ITERATIONS = 100
DEFAULT_PRECISION = 1e-5
# endregion

# region EPOCHS for various calendars (RDM Table 1.2, p. 17).
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

# region Mathematical Operations
def quotient(x: float, y: float) -> float:
    """
    Calculates the whole part of a ratio.
    :param x: The dividend.
    :param y: The divisor.
    :return: The result.
    """
    return math.floor(x / y)


def int_quotient(x: float, y: float) -> int:
    """
    Calculates the whole part of a ratio as an integer number
    :param x: The dividend.
    :param y: The divisor.
    :return: The result.
    """
    return int(quotient(x, y))


def fmod(x: float, y: float) -> float:
    """
    RDU (1.17): The The	remainder, or modulus, of decimal numbers.
    :param x: The first operand.
    :param y: The second operand.
    :return: The result of the operation.
    Examples: fmod(9, 5) = 4; fmod(-9, 5) = 1; fmod(9, -5) = -1; fmod(-9, -5) = -4.
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


def sind(x: float) -> float:
    """
    Sine of an argument given in degrees. (Neither math nor numpy seem to have these simple functions).
    :param x: Tha argument in degrees.
    :return: sin(x).
    """
    return math.sin(x * DEGREE)


def cosd(x: float) -> float:
    """
    Cosine of an argument given in degrees.
    :param x: Tha argument in degrees.
    :return: cos(x).
    """
    return math.cos(x * DEGREE)


def tand(x: float) -> float:
    """
    Tangens of an argument given in degrees.
    :param x: Tha argument in degrees.
    :return: tan(x).
    """
    return math.tan(x * DEGREE)


# endregion

# region Root finding related
def bisection(f: Callable, left: float, right: float, precision: float = DEFAULT_PRECISION,
              max_iterations: int = DEFAULT_MAX_ITERATIONS) -> float:
    """
    Tries to find a root of an expression by bisection.
    R&D use bisection, since it always converges and the precision does not need to be very high
    (1s = 1/86400 or about 1e-5 is enough).
    :param f: The function f(x) the zero point of which has to be found:: x: f(x) = 0.
    :param left: The left boundary of the initial interval in which to search for the zero point.
                 The values of the function must be of opposite signs at the interval's boundaries.
    :param right: The right boundary of the initial interval in which to search for the zero point.
    :param precision: The precision to reach. Default = 1e-5.
    :param max_iterations: The number of iterations after which to abandon process. Default = 100.
    :return: The value of the zero point.
    :exception ValueError: Raised if the interval does not bracket a zero point.
    """
    f_left = f(left)
    r_right = f(right)

    if np.sign(f_left) == np.sign(r_right):
        raise ValueError("Wrong initial interval: the values of the function are of the same sign")

    middle = (left + right) / 2

    iterations = 0

    accuracy = math.fabs(f(middle))

    while accuracy > precision and iterations < max_iterations:
        f_middle = f(middle)

        if np.sign(f_middle) == np.sign(f_left):
            left = middle
        else:
            right = middle

        middle = (left + right) / 2

        accuracy = math.fabs(f(middle))
        iterations += 1

    return middle


def bracket(f: Callable, left: float, right: float, factor: float = DEFAULT_BRACKETING_FACTOR,
            max_iterations: int = DEFAULT_MAX_ITERATIONS) -> (float, float):
    """
    Tries to bracket an interval with respect to a function, i.e. if the initial interval is not a bracket itself,
    it successively increases its boundaries before it reaches a bracketing interval.
    :param f: The function f(x) that should be bracketed.
    :param left: The initial left boundary of the interval to start bracketing from.
    :param right: The initial right boundary of the interval to start bracketing from.
    :param factor: The factor to expand the intervals' boundaries. Default = 0.618...
    :param max_iterations: The number of iterations after which to abandon process. Default = 100.
    :return: A bracketing interval, if successfull.
    :exception StopIteration: Raised if no bracket was found after maxIterations.
    """
    left, right = np.minimum(left, right), np.maximum(left, right)

    f_left = f(left)
    r_right = f(right)

    if np.sign(f_left) != np.sign(r_right):
        return left, right

    iterations = 0

    while iterations <= max_iterations:
        width = right - left

        left -= factor * width
        f_left = f(left)
        if np.sign(f_left) != np.sign(r_right):
            return left, right

        right += factor * width
        r_right = f(right)
        if np.sign(f_left) != np.sign(r_right):
            return left, right

        iterations += 1

    raise StopIteration("Maximum iterations reached. No bracket found")


# endregion

def gregorian_year_from_rata_die(t: float) -> float:
    """
    Calculates Gregorian year from a rata die value.
    RDM (2.18).
    :param t: The value of rata die.
    :return: The Gregorian year.
    """
    d0 = t - 1
    n400 = math.floor(d0 / 146097)
    d1 = fmod(d0, 146097)
    n100 = math.floor(d1 / 36524)
    d2 = fmod(d1, 36524)
    n4 = math.floor(d2 / 1461)
    d3 = fmod(d2, 1461)
    n1 = math.floor(d3 / 365)

    year = 400.0 * n400 + 100.0 * n100 + 4.0 * n4 + n1

    if int(n100) != 4 and int(n1) != 4:
        year += 1

    return year


# region Leap years
def is_gregorian_leap_year(gregorian_year: int) -> bool:
    """
    Determines whether a year is a Gregorian leap year.
    RDM (2.16), p.51.
    See also: https://stackoverflow.com/questions/11621740/how-to-determine-whether-a-year-is-a-leap-year
    :param gregorian_year: The Gregorian year to check.
    :return: True if the Gregorian year is a leap one.
    """
    return gregorian_year % 4 == 0 and (gregorian_year % 100 != 0 or gregorian_year % 400 == 0)


def is_julian_leap_year(julian_year: int) -> bool:
    """
    Determines whether a year is a Julian leap year.
    RDM (3.1), p.63.
    :param julian_year: The Julian year to check.
    :return: True if the Julian year is a leap one.
    """
    jy4 = julian_year % 4
    return jy4 == 0 if julian_year > 0 else jy4 == 3


def is_hebrew_leap_year(hebrew_year: int) -> bool:
    """
    Determines whether a year is a Hebrew leap year.
    RDM (7.3)
    :param hebrew_year: The Hebrew year to check.
    :return: True if the Hebrew year is a leap one.
    """
    if int(fmod((7 * hebrew_year + 1), 19) < 7):
        return True
    else:
        return False


# endregion

# region Week-related Gregorian helper functions.
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


# endregion

# region Miscellaneous Helpers
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
        if is_gregorian_leap_year(year):
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


# endregion

# region String Representation Related
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
# endregion
