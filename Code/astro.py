from Code.times import julian_centuries
from Code.tools import sind, cosd, fmod

SUN_LONGITUDE_DATA = [
 [403406, 0.9287892, 270.54861],
 [195207, 35999.1376958, 340.19128],
 [119433, 35999.4089666, 63.91854],
 [112392, 35998.7287385, 331.2622],
 [3891, 71998.20261, 317.843],
 [2819, 71998.4403, 86.631],
 [1721, 36000.35726, 240.052],
 [660, 71997.4812, 310.26],
 [350, 32964.4678, 247.23],
 [334, -19.441, 260.87],
 [314, 445267.1117, 297.82],
 [268, 45036.884, 343.14],
 [242, 3.1008, 166.79],
 [234, 22518.4434, 81.53],
 [158, -19.9739, 3.5],
 [132, 65928.9345, 132.75],
 [129, 9038.0293, 182.95],
 [114, 3034.7684, 162.03],
 [99, 33718.148, 29.8],
 [93, 3034.448, 266.4],
 [86, -2280.773, 249.2],
 [78, 29929.992, 157.6],
 [72, 31556.493, 257.8],
 [68, 149.588, 185.1],
 [64, 9037.75, 69.9],
 [46, 107997.405, 8.0],
 [38, -4444.176, 197.1],
 [37, 151.771, 250.4],
 [32, 67555.316, 65.3],
 [29, 31556.08, 162.7],
 [28, -4561.54, 341.5],
 [27, 107996.706, 291.6],
 [27, 1221.655, 98.5],
 [25, 62894.167, 146.7],
 [24, 31437.369, 110.0],
 [21, 14578.298, 5.2],
 [21, -31931.757, 342.6],
 [20, 34777.243, 230.9],
 [18, 1221.999, 256.1],
 [17, 62894.511, 45.3],
 [14, -4442.039, 242.9],
 [13, 107997.909, 115.2],
 [13, 119.066, 151.8],
 [13, 16859.071, 285.3],
 [12, -4.578, 53.3],
 [10, 26895.292, 126.6],
 [10, -39.127, 205.7],
 [10, 12297.536, 85.9],
 [10, 90073.778, 146.1]]

class Astro:
    """
    Contains data and routines to compute astronomical events.
    """
    @classmethod
    def solar_longitude(cls, t: float) -> float:
        """
        Calculates the value of the sun longitude in geocentric ecliptic coordinate system for a given moment of time.
        :param t: The value of time, RD.
        :return: The value of the sun longitude, in degrees.
        """
        c = julian_centuries(t)

        sum = 0
        for item in SUN_LONGITUDE_DATA:
            sum += item[0] * sind(item[1] * c + item[2])

        sun_longitude = (Astro.aberration(t) + Astro.nutation(t) +
                         282.7771834 + 36000.79653744 * c + 0.000005729577951308232 * sum)

        return fmod(sun_longitude, 360)

    @classmethod
    def aberration(cls, t: float) -> float:
        """
        Aberration, the effect of the sun’s moving about 20.47 seconds of arc during the 8 minutes
        during which its light is en route to Earth.
        RDM (12.27).
        :param t: The time moment, RD.
        :return: The value of aberration, in degrees.
        """
        c = julian_centuries(t)
        return 0.0000974 * cosd(177.63 + 35999.01848 * c) - 0.005575

    @classmethod
    def nutation(cls, t: float) -> float:
        """
        Nutation RDU (14.31), RDM (12.26): caused by the gravitational pull of the moon and sun on the unevenly
        shaped Earth. Nutation causes slight changes in the celestial latitudes and longitudes of stars and planets.
        :param t: The time moment, RD.
        :return: The value of nutation, degrees.
        """
        c = julian_centuries(t)
        A = 124.90 + c * (-1934.134 + 0.002063 * c)
        B = 201.11 + c * (72001.5377 + 0.00057 * c)

        return -0.004778 * sind(A) - 0.0003667 * sind(B)


