from astro import Astro
from calendars.gregorian_date import GregorianDate
from location import Location
from tools import to_hms

gregorian = GregorianDate(1996, 2, 25)

rd = gregorian.to_moment()

location = Location("Jerusalem", latitude=31.778889, longitude=35.225556, elevation=754, zone=2)
sunset = Astro.sunset(rd, location)

print(sunset)

fits = sunset - rd

hms = to_hms(fits)

print (hms)

# 17:38:08 vs 17:37:39