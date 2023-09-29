import math

import tools
from calendars.gregorian_date import GregorianDate
from location import Location
from numpy.polynomial.polynomial import Polynomial
from tools import sind, cosd

J2000 = 730120.5  # Noon on 2000-01-01 (Gregorian): RDU (14.18)

# region Ephemeris constants
EPHEMERIS_CORRECTION_1987 = [63.86, 0.3345, -0.060374, 0.0017275, 0.000651814, 0.00002373599]
EPHEMERIS_CORRECTION_1900 = [-0.00002, 0.000297, 0.025184, -0.181133, 0.553040, -0.861938, 0.677066, -0.212591]
EPHEMERIS_CORRECTION_1800 = [-0.000009, 0.003844, 0.083563, 0.865736, 4.867575, 15.845535, 31.332267, 38.291999,
                             28.316289, 11.636204, 2.043794]
EPHEMERIS_CORRECTION_1700 = [8.118780842, -0.005092142, 0.003336121, -0.0000266484]
EPHEMERIS_CORRECTION_1600 = [120, -0.9808, -0.01532, 0.000140272128]
EPHEMERIS_CORRECTION_1000 = [1574.2, -556.01, 71.23472, 0.319781, -0.8503463, -0.005050998, 0.0083572073]
EPHEMERIS_CORRECTION_0 = [10583.6, -1014.41, 33.78311, -5.952053, -0.1798452, 0.022174192, 0.00090316521]

# endregion

OBLIQUITY = [23.43929111111111, -0.013004167, -1.638e-07, 5.03611e-07]

# Coefficients for solar longitude, anomaly, and eccentricity used to calculate equation of time, RDU (14.20)
ET_LONGITUDE = [280.46645, 36000.76983, 0.0003032]
ET_ANOMALY = [357.52910, 35999.05030, -0.0001559, -0.00000048]
ET_ECCENTRICITY = [0.016708617, -0.000042037, -0.0000001236]


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
    "Astronomical calculations are done using Dynamical Time... Solar time units ... are not constant hrough time ...
    because of the retarding effects of tides and the atmosphere, which cause a relatively teady lengthening of the day.
    Because the accumulated discrepancy is not entirely predictable and is not accurately known ...
    the following ad hoc function is used for the EPHEMERIS CORRECTION."
    RDU (14.15).
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


def universal_to_dynamic(t_dynamic: float) -> float:
    """
    RDM (12.13).
    :param t_dynamic: The dynamic time.
    :return: The dynamic time.
    """
    return t_dynamic + ephemeris_correction(t_dynamic)


def dynamic_to_universal(t_universal: float) -> float:
    """
    RDM (12.14).
    :param t_universal: The universal time (solar UTC).
    :return: The universal time.
    """
    return t - ephemeris_correction(t_universal)


def julian_centuries(t: float) -> float:
    """
    RDU (14.18).
    """
    return (universal_to_dynamic(t) - J2000) / 36525


def obliquity(t: float) -> float:
    """
    RDM (12.23).
    """
    c = julian_centuries(t)
    return Polynomial(OBLIQUITY)(c)


def equation_of_time(t: float, eccentricity=None) -> float:
    c = julian_centuries(t)

    solar_longitude = Polynomial(ET_LONGITUDE)(c)  # degrees
    anomaly = Polynomial(ET_ANOMALY)(c)  # degrees
    eccentricity = Polynomial(ET_ECCENTRICITY)(c)
    epsilon = obliquity(t)  # degrees
    y = tools.tand(0.5 * epsilon) ** 2

    et = y * sind(2 * solar_longitude) - 2.0 * eccentricity * sind(anomaly) + \
         4 * eccentricity * y * sind(anomaly) * cosd(2 * solar_longitude) - 0.5 * y ** 2 * sind(4 * solar_longitude) - \
         1.25 * eccentricity ** 2 * sind(2 * anomaly)

    et /= (2 * math.pi)

    return et

if __name__ == '__main__':

    year = 2023
    ts = []
    ets = []

    for day in range(1, 366):
        gregorian = GregorianDate.from_day_number(day, year)
        t = gregorian.to_moment()
        et = equation_of_time(t)
        minutes = et * 24 * 60

        ts.append(t)
        ets.append(minutes)

        # print(t, et, minutes)

    import matplotlib.pyplot as plt
    from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

    fig, ax = plt.subplots(1, 1)

    # ax.xaxis.set_major_locator(MultipleLocator(30.0))
    # ax.xaxis.set_major_formatter('{x:.0f}')
    # ax.xaxis.set_minor_locator(MultipleLocator(10))
    #
    # ax.yaxis.set_major_locator(MultipleLocator(2.0))
    # ax.yaxis.set_major_formatter('{x:.0f}')
    # ax.yaxis.set_minor_locator(MultipleLocator(0.5))

    ax.plot(ts, ets, linewidth=2.0, label="observed", antialiased=True)
    plt.show()
