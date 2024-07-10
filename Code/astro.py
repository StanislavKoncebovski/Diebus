import math
from typing import Optional

import location
import times
import tools
from calendars.gregorian_date import GregorianDate
from location import Location


EARTH_RADIUS = 6.372e6
JULIAN_EPOCH = 2451543.5

def day_number(t: float) -> float:
    """
    Paul Schlyter (PS): PS (1)
    """
    return t - JULIAN_EPOCH

def longitude_of_perihelion(d: float) -> float:
    """
    PS(2): Longitude of perihelion.
    :param d: Day number.
    :return: Longitude of perihelion, degrees.
    """
    return 282.9404 + 4.70935e-5 * d

def eccentricity(d: float) -> float:
    """
    PS (3)
    :param d:
    :return:
    """
    return 0.016709 - 1.151e-9 * d

def mean_solar_anomaly(d: float) -> float:
    """
    Mean anomaly of the Sun, PS(4)
    :param d:
    :return:
    """
    return 356.047 + 0.9856002585 * d

def obliquity(d: float) -> float:
    return 23.4393 - 3.563e-7 * d

def mean_solar_longitude(d: float) -> float:
    return longitude_of_perihelion(d) + mean_solar_anomaly(d)

def eccentric_solar_anomaly(d: float) -> float:
    M = mean_solar_anomaly(d)
    e = eccentricity(d)
    return M + (180.0 / math.pi) * e * math.sin(M * math.pi / 180) * (1 + e * math.cos(M * math.pi / 180))

def solar_cartesian_coordinates(d: float) -> (float, float):
    E = eccentric_solar_anomaly(d)
    e = eccentricity(d)
    x = math.cos(E * math.pi / 180) - e
    y = math.sin(E * math.pi / 180) * math.sqrt(1.0 - e**2)

    return x, y

def solar_polar_coordinates(d: float) -> (float, float):
    x, y = solar_cartesian_coordinates(d)
    r = math.sqrt(x**2 + y**2)
    v = math.atan2(y, x)

    return r, v

def solar_longitude(d: float) -> float:
    w = longitude_of_perihelion(d)
    r, v = solar_polar_coordinates(d)

    return w + v

def solar_ecliptic_coordinates(d: float) -> (float, float, float):
    r, v = solar_polar_coordinates(d)
    lon = solar_longitude(d)
    x = r * math.cos(lon)
    y = r * math.sin(lon)
    z = 0

    return x, y, z

def solar_cartesian_equatorial_coordinates(d: float) -> (float, float, float):
    """
    xequat = xeclip
    yequat = yeclip * cos(oblecl) - zeclip * sin(oblecl)
    zequat = yeclip * sin(oblecl) + zeclip * cos(oblecl)
    :param d:
    :return:
    """
    x, y, z = solar_ecliptic_coordinates(d)
    epsilon = obliquity(d)

    x_equat = x
    y_equat = y * math.cos(epsilon * math.pi / 180) - z * math.sin(epsilon * math.pi / 180)
    z_equat = y * math.sin(epsilon * math.pi / 180) + z * math.cos(epsilon * math.pi / 180)

    return x_equat, y_equat, z_equat

def solar_polar_equatorial_coordinates(d: float) -> (float, float):
    """
    r    = sqrt( x*x + y*y + z*z )
    RA   = atan2( y, x )
    Decl = asin( z / r ) = atan2( z, sqrt( x*x + y*y ) )
    :param d:
    :return: RA (degrees), declination (degrees)
    """
    x_equat, y_equat, z_equat = solar_cartesian_equatorial_coordinates(d)
    r = math.sqrt(x_equat**2 + y_equat**2 + z_equat**2)
    RA = math.atan2(y_equat, x_equat)
    decl = math.asin(z_equat / r)

    return RA, decl

def greenwich_sidereal_time(d: float) -> float:
    """
    :param d:
    :return: Sidereal time at Greenwich, hours
    """
    return mean_solar_longitude(d) / 15 + 12

def local_sidereal_time(d: float, longitude: float):
    return greenwich_sidereal_time(d) + longitude / 15

def alternative_polar_equatorial_coordinates(d: float, longitude: float) -> (float, float):
    """
    Equatorial coordinates where RA is replaced with the hour angle
    :param d:
    :param longitude:
    :return: HA, declination
    """
    RA, decl = solar_polar_equatorial_coordinates(d)
    sid = greenwich_sidereal_time(d) + longitude / 15
    RA, decl = solar_polar_equatorial_coordinates(d)

    return sid - RA, decl

def solar_horizontal_coordinates(d: float, latitude: float, longitude: float) -> (float, float):
    HA, decl = alternative_polar_equatorial_coordinates(d, longitude)
    x = math.cos(HA * math.pi / 180) * math.cos(decl * math.pi / 180)
    y = math.sin(HA * math.pi / 180) * math.cos(decl * math.pi / 180)
    z = math.sin(decl * math.pi / 180)

    x_hor = x * math.sin(latitude * math.pi / 180) - z * math.cos(latitude * math.pi / 180)
    y_hor = y
    z_hor = x * math.cos(latitude * math.pi / 180) + z * math.sin(latitude * math.pi / 180)

    azimuth = math.atan2(y_hor, x_hor) + 180
    altitude = math.asin(z_hor)

    return azimuth, altitude
