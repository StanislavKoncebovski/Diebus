import math

import numpy as np

import tools
from calendars.gregorian_date import GregorianDate
from location import Location
from numpy.polynomial.polynomial import Polynomial
from tools import sind, cosd

J2000 = 730120.5    # Noon on 2000-01-01 (Gregorian): RDU (14.18)
SPRING = 0          # Longitude of sun at vernal equinox
SUMMER = 90         # Longitude of sun at summer solstice
AUTUMN = 180        # Longitude of sun at autumnal equinox
WINTER = 270        # Longitude of sun at winter solstice

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
SIDEREAL = [280.46061837, 1308572.97170280125, 0.000387933, -2.5833118057349522087315939033841e-8]

MEAN_TROPICAL_YEAR = 365.242189

# region Constants to calculate solar longitude
SOLAR_LONGITUDE_X = [
    403406, 195207, 119433, 112392, 3891,
    2819, 1721, 660, 350, 334,
    314, 268, 242, 234, 158,
    132, 129, 114, 99, 93,
    86, 78, 72, 68, 64,
    46, 38, 37, 32, 29,
    28, 27, 27, 25, 24,
    21, 21, 20, 18, 17,
    14, 13, 13, 13, 12,
    10, 10, 10, 10
]

SOLAR_LONGITUDE_Y = [
    0.9287892, 35999.1376958, 35999.4089666, 35998.7287385, 71998.20261,
    71998.4403, 36000.35726, 71997.4812, 32964.4678, -19.4410,
    445267.1117, 45036.8840, 3.1008, 22518.4434, -19.9739,
    65928.9345, 9038.0293, 3034.7684, 33718.148, 3034.448,
    -2280.773, 29929.992, 31556.493, 149.588, 9037.750,
    107997.405, -4444.176, 151.771, 67555.316, 31556.080,
    -4561.540, 107996.706, 1221.655, 62894.167, 31437.369,
    14578.298, -31931.757, 34777.243, 1221.999, 62894.511,
    -4442.039, 107997.909, 119.066, 16859.071, -4.578,
    26895.292, -39.127, 12297.536, 90073.778
]

SOLAR_LONGITUDE_Z = [
    270.54861, 340.19128, 63.91854, 331.26220, 317.843,
    86.631, 240.052, 310.26, 247.23, 260.87,
    297.82, 343.14, 166.79, 81.53, 3.50,
    132.75, 182.95, 162.03, 29.8, 266.4,
    249.2, 157.6, 257.8, 185.1, 69.9,
    8.0, 197.1, 250.4, 65.3, 162.7,
    341.5, 291.6, 98.5, 146.7, 110.0,
    5.2, 342.6, 230.9, 256.1, 45.3,
    242.9, 115.2, 151.8, 285.3, 53.3,
    126.6, 205.7, 85.9, 146.1
]


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

def declination(t: float, beta:float, lambda1: float):
    epsilon = obliquity(t)
    return math.asin(math.sin(beta) * math.cos(epsilon) + math.cos(beta) * math.sin(epsilon) * math.sin(lambda1))


def equation_of_time(t: float) -> float:
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


def local_to_apparent(t_local: float) -> float:
    """
    Conversion of apparent time to local time.
    RDM (12.18).
    Apparent time is the time measured by a sundial (e.g. the moment of midday),
    whereas local time is based on mean time (measured with a device, such as a mechanical clock or atom clock).
    :param t_local: The local time, days.
    :return: The apparent time, days.
    """
    return t_local + equation_of_time(t_local)


def apparent_to_local(t_apparent: float) -> float:
    """
    Conversion of apparent  time to local time.
    RDM (12.19).
    RD: Slightly inaccurate: the argument in EquationOfTime() should be not t, but the local time instead.
    :param t_apparent: The apparent time, days.
    :return: The local time, days
    """
    return t_apparent - equation_of_time(t_apparent)


def midnight(t_apparent: float, location: Location) -> float:
    """
    Calculates the true, or apparent middle of the night for a location.
    SK: R&D give this and the next formula without an explanation what a midnight is, and I still do not understand how
    you can know the time of a midnight only knowing an arbitrary moment of time.
    RDM (2.20)
    :param t_apparent:  Apparent time.
    :param location: Location to find the midnight for.
    :return: Local time of midnight.
    """
    return local_to_standard(apparent_to_local(t_apparent), location)


def midday(t_apparent: float, location: Location) -> float:
    """
    Calculates the true, or apparent middle of the day (aka apparent noon) for a location.
    RDM (2.21)
    :param t_apparent: Apparent time.
    :param location: Location to find the midday for.
    :return: Local time of midday.
    """
    return local_to_standard(apparent_to_local(t_apparent + 0.5), location)


def solar_to_sidereal(t: float) -> float:
    """
    Conversion of mean solar time to mean sidereal time.
    RDM (12.22).
    :param t: Mean solar time.
    :return: Mean sidereal time, in degrees.
    """
    c = julian_centuries(t)

    result = Polynomial(SIDEREAL)(c)

    return tools.fmod(result, 360)


def aberration(t: float) -> float:
    """
    Aberration, the effect of the sun’s moving about 20.47 seconds of arc during the 8 minutes
    during which its light is en route to Earth.
    RDM (12.27).
    :param t: The time moment.
    :return: The value of aberration, in degrees.
    """
    c = julian_centuries(t)
    return 0.0000974 * math.cos(tools.DEGREE * (177.63 + 35999.01848 * c)) - 0.005575


def nutation(t: float) -> float:
    """
    Nutation RDU (14.31), RDM (12.26): caused by the gravitational pull of the moon and sun on the unevenly
    shaped Earth. Nutation causes slight changes in the celestial latitudes and longitudes of stars and planets.
    :param t: The time moment.
    :return: The value of nutation, degrees.
    """
    c = julian_centuries(t)
    A = 124.90 + c * (-1934.134 + 0.002063 * c)
    B = 201.11 + c * (72001.5377 + 0.00057 * c)

    return -0.004778 * math.sin(A * tools.DEGREE) - 0.0003667 * math.sin(B * tools.DEGREE)


def solar_longitude(t: float) -> float:
    """
    Calculates the longitude o the sun at a given astronomical time.
    RDM (12.25).
    :param t: Astronomical time given as an R.D.
    :return: The value of solar longitude, in degrees.
    """
    c = julian_centuries(t)

    s = 0.0

    for i in range(len(SOLAR_LONGITUDE_X)):
        s += SOLAR_LONGITUDE_X[i] * math.sin(tools.DEGREE * (SOLAR_LONGITUDE_Y[i] * c + SOLAR_LONGITUDE_Z[i]))

    longitude = 282.7771834 + 36000.76953744 * c + 0.000005729577951308232 * s + aberration(t) + nutation(t)

    return tools.fmod(longitude, 360)


def estimate_prior_solar_longitude(t: float, solar_longitude_value: float) -> float:
    """
    Approximate moment of time at or before a given value of time when solar longitude just exceeded lambda degrees.
    :param t: The given value of time before which we need the value of the taime with the given solar longitude.
    :param solar_longitude_value: The value of solar longitude.
    :return: The moment of time when the solar longitude is being reached.
    """
    rate = MEAN_TROPICAL_YEAR / 360
    tau = t - rate * tools.fmod(solar_longitude(t) - solar_longitude_value, 360)
    delta = tools.fmod(solar_longitude(tau) - solar_longitude_value + 180, 360) - 180

    return np.minimum(t, tau - rate * delta)


if __name__ == '__main__':

    year = 2023
    ts = []
    ets = []
    t0 = GregorianDate.from_day_number(1, year).to_moment()

    for day in range(1, 366):
        gregorian = GregorianDate.from_day_number(day, year)
        t = gregorian.to_moment() - t0
        et = equation_of_time(t)
        minutes = et * 24 * 60

        ts.append(t)
        ets.append(minutes)

        # print(t, et, minutes)

    import matplotlib.pyplot as plt
    from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

    fig, ax = plt.subplots(1, 1)

    ax.xaxis.set_major_locator(MultipleLocator(30.0))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.xaxis.set_minor_locator(MultipleLocator(10))

    ax.yaxis.set_major_locator(MultipleLocator(5.0))
    ax.yaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_minor_locator(MultipleLocator(0.5))

    plt.grid(visible=True, which='major', color='b', alpha=0.25, linestyle='-', linewidth=0.75)
    plt.grid(visible=True, which='minor', color='r', alpha=0.15, linestyle='-', linewidth=0.5)

    ax.plot(ts, ets, linewidth=2.0, label="observed", antialiased=True)
    plt.show()
