from math import asin, pi

from calendars.gregorian_date import GregorianDate
from times import julian_centuries, aberration, nutation, obliquity
from tools import sind, fmod

SUN_LONGITUDE_COEFFICIENTS = [
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

SUN_LONGITUDE_MULTIPLICATION = [

    0.9287892, 35999.1376958, 35999.4089666, 35998.7287385, 71998.20261,
    71998.4403, 36000.35726, 71997.4812, 32964.4678, -19.4410,
    445267.1117, 45036.8840, 3.1008, 22518.4434, -19.9739,
    65928.9345, 9038.0293, 3034.7684, 33718.148, 3034.448,
    - 2280.773, 29929.992, 31556.493, 149.588, 9037.750,
    107997.405, -4444.176, 151.771, 67555.316, 31556.080,
    -4561.540, 107996.706, 1221.655, 62894.167, 31437.369,
    14578.298, -31931.757, 34777.243, 1221.999, 62894.511,
    -4442.039, 107997.909, 119.066, 16859.071, -4.578,
    26895.292, -39.127, 12297.536, 90073.778
]

SUN_LONGITUDE_ADDENDA = [
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


def sun_longitude(t: float) -> float:
    """
    Solar longitude for a moment of time.
    :param t: Moment of time, RD.
    :return: Solar longitude, degrees.
    """
    c = julian_centuries(t)

    sum = 0
    n = 49

    for i in range(n):
        sum += SUN_LONGITUDE_COEFFICIENTS[i] * sind(SUN_LONGITUDE_MULTIPLICATION[i] * c + SUN_LONGITUDE_ADDENDA[i])

    sun_longitude = aberration(t) + nutation(t) + 282.7771834 + 36000.79653744 * c + 0.000005729577951308232 * sum

    return fmod(sun_longitude, 360)

def declination(t: float) -> float:
    return asin(sind(obliquity(t)) * sind(sun_longitude(t))) * 180 / pi

def moment_from_depression()

if __name__ == '__main__':
    gregorian = GregorianDate(1990, 4, 19)
    print(gregorian)
    rd = gregorian.to_moment()

    sun_lon = sun_longitude(rd)

    print(sun_lon)

    decl = declination(rd)

    print(decl)