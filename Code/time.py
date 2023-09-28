import tools
from calendars.gregorian_date import GregorianDate
from location import Location
from numpy.polynomial.polynomial import Polynomial

# region Ephemeris constants
EPHEMERIS_CORRECTION_1987 = [63.86, 0.3345, -0.060374, 0.0017275, 0.000651814, 0.00002373599]
EPHEMERIS_CORRECTION_1900 = [-0.00002, 0.000297, 0.025184, -0.181133, 0.553040, -0.861938, 0.677066, -0.212591]
EPHEMERIS_CORRECTION_1800 = [-0.000009, 0.003844, 0.083563, 0.865736, 4.867575, 15.845535, 31.332267, 38.291999, 28.316289, 11.636204, 2.043794]
EPHEMERIS_CORRECTION_1700 = [8.118780842, -0.005092142, 0.003336121, -0.0000266484]
EPHEMERIS_CORRECTION_1600 = [120, -0.9808, -0.01532, 0.000140272128]
EPHEMERIS_CORRECTION_1000 = [1574.2, -556.01, 71.23472, 0.319781, -0.8503463, -0.005050998, 0.0083572073]
EPHEMERIS_CORRECTION_0 = [10583.6, -1014.41, 33.78311, -5.952053, -0.1798452, 0.022174192, 0.00090316521]
# endregion

# region Time conversions
def local_to_universal(t_local: float, location: Location) -> float:
    """
    Converts local time to universal time.
    Universal Time (U.T.C.) is the local mean solar time, reckoned from midnight,
    at the observatory in Greenwich, England, the 0◦ meridian. (RD).
    Local time is the mean solar time at the locality.
    RDM (12.6)
    :param t_local: The local time.
    :param location: The location.
    :return: The Universal time.
    """
    return t_local - location.longitude / 360


def universal_to_local(t_universal: float, location: Location) -> float:
    """
    Converts universal time to local time.
    RDM (12.7)
    :param t_universal: The universal time.
    :param location: The location.
    :return: The local time.
    :return: The local time.
    """
    return t_universal + location.longitude / 360


def universal_to_standard(t_universal: float, location: Location) -> float:
    """
    Converts universal time to standard local time.
    RDM (12.8)
    :param t_universal: The universal time.
    :param location: The location.
    :return: The standard time.
    """
    return t_universal + location.zone / 24


def standard_to_universal(t_standard: float, location: Location) -> float:
    """
    Converts universal time to standard time.
    RDM (12.9)
    :param t_standard: The universal time.
    :param location: The location.
    :return: The standard time in the locality.
    """
    return t_standard - location.zone / 24


def local_to_standard(t_local: float, location: Location) -> float:
    """
    Converts local time to standard time.
    RDM (12.10).
    :param t_local: The local time.
    :param location: The location.
    :return: The standard time.
    """
    return universal_to_standard(local_to_universal(t_local, location), location)


def standard_to_local(t_standard: float, location: Location) -> float:
    """
    Converts standard time to local time.
    RDM (12.11).
    :param t_standard: The standard time.
    :param location: The location.
    :return: The universal time.
    """
    return universal_to_local(standard_to_universal(t_standard, location), location)
# endregion

def ephemeris_correction(t: float) -> float:
    """

    :param t:
    :return:
    """
    year = tools.gregorian_year_from_rata_die(t)
    c = (GregorianDate(int(year), 7, 1).to_moment() - GregorianDate(1900, 1, 1).to_moment()) / 36525
    y2000 = year - 2000
    y1700 = year - 1700
    y1600 = year - 1600
    y1000 = (year - 1000) / 100
    y0 = year / 100
    y1820 = (year - 1820) / 100

    if 2051 <= year <= 2150:
        z = (year - 1820) / 100
        return (-20 + 32 * z * z + 0.5628 * (2150 - year)) / 86400

    elif 2006 <= year <= 2050:
        return (62.92 + 0.32217 * y2000 + 0.005589 * y2000 * y2000) / 86400

    elif 1987 <= year <= 2005:
        return Polynomial(EPHEMERIS_CORRECTION_1987)(y2000) / 86400

    elif 1900 <= year <= 1986:
        return Polynomial(EPHEMERIS_CORRECTION_1900)(c)

    elif 1800 <= year <= 1899:
        return Polynomial(EPHEMERIS_CORRECTION_1800)(c)

    elif 1700 <= year <= 1799:
        return Polynomial(EPHEMERIS_CORRECTION_1700)(y1700) / 86400

    elif 1600 <= year <= 1699:
        return Polynomial(EPHEMERIS_CORRECTION_1600)(y1600) / 86400

    elif 500 <= year <= 1599:
        return Polynomial(EPHEMERIS_CORRECTION_1000)(y1000) / 86400

    elif -500 <= year < 500:
        return Polynomial(EPHEMERIS_CORRECTION_0)(y0) / 86400

    else:
        return (-20 + 32 * y1820 * y1820) / 86400
