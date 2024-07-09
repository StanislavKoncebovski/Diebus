import math
from typing import Optional

import location
import times
import tools
from calendars.gregorian_date import GregorianDate
from location import Location

EARTH_RADIUS = 6.372e6
EVENING = False

def sunset(date: float, location: Location) -> float:
    '''
    UE (14.77)
    '''
    # The extra 16' (0.0111111111111111d)  is needed because we	want the time when the upper
    # limb of the sun first becomes visible.
    alpha = refraction(date + 0.75, location) + 0.0111111111111111
    return dusk(date, location, alpha)

def refraction(t: float, location: Location) -> float:
    '''
    The standard value of refraction, taking elevation into	account UE (14.75)
    0.0236111111111111 = 34', 2.199074074074074e-4 = 19''.
    '''
    h = max(0.0, location.elevation)
    dip = math.acos(EARTH_RADIUS / (EARTH_RADIUS + h))

    return 0.0236111111111111 + dip + 2.199074074074074e-4 * math.sqrt(h)

def dusk(date: float, location: Location, alpha: float) -> float:
    '''
    UE (14.74)
    '''
    result = moment_of_depression(date + 0.75, location, alpha, EVENING)

def moment_of_depression(approx: float, locale: Location, alpha: float, early: bool) -> Optional[float]:
    t = approx_moment_of_depression(approx, locale, alpha, early)

    if t is None:
        return None
    else:
        if abs(approx - t) < 3.472222222222222e-4:  # 30'
            return t
        else:
            return moment_of_depression(t, locale, alpha, early)

def approx_moment_of_depression(t: float, locale: Location, alpha: float, early: bool) -> Optional[float]:
    date = math.floor(t)
    try1 = sine_offset(t, locale, alpha)
    alt = date if alpha >= 0.0 and early else date + 1 if alpha >= 0 else date + 0.5
    value = sine_offset(t, locale, alpha) if abs(try1) > 1 else try1

    if abs(value) <= 1:
        arg = date + 0.5 + tools.fmod(0.5 + math.asin(value) / (2 * math.pi), 1)
        if early:
            arg -=1
        else:
            arg += 1

        arg -= 0.25

        return times.apparent_to_local(arg)

    else:
        return None

def sine_offset(t: float, locale: Location, alpha: float) -> float:
    t1 = times.local_to_universal(t, locale)
    delta = times.declination(t1, 0, times.solar_longitude(t1))

    return tools.tand(locale.latitude) * math.tan(delta) + math.sin(alpha) / (math.cos(delta) * math.cos(locale.latitude))

if __name__ == '__main__':
   gregorian = GregorianDate(1945, 11, 12)
   t = gregorian.to_moment()

   sunset = sunset(t, location.URBANA)

   print(sunset)