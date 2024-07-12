import datetime
import math

from astropy.utils.exceptions import AstropyWarning
from astropy.utils.iers import conf, IERS_A

from astroplan import Observer
from astropy.units import Quantity

from calendars.gregorian_date import GregorianDate
from location import Location
from tools import to_julian_days, from_julian_days, to_hms, EARTH_RADIUS, RADIAN

import warnings
from erfa import ErfaWarning
from astropy.utils.iers import conf
from astropy.time import Time

# ================= PREAMBLE: WARNING SUPPRESSION =========
# Suppress the specific ErfaWarning
warnings.filterwarnings("ignore", category=ErfaWarning)

# Suppress the specific IERS-related warning
warnings.filterwarnings("ignore", category=AstropyWarning)

conf.auto_download = True

# Ensure the latest IERS data is loaded
iers_a = IERS_A.open()

# =============== END OF PREAMBLE =========================
gregorian = GregorianDate(1870, 10, 7)

rd = gregorian.to_moment()

print(f"rd = {rd}")

jd = to_julian_days(rd)

print(f"jd = {jd}")

location = Location("Jerusalem", 31.8, 35.2, 800, 2)
offset_timedelta = datetime.timedelta(hours=location.zone)
tzinfo = datetime.timezone(offset_timedelta)

observer = Observer(name=location.name, latitude=location.latitude,  longitude=location.longitude,
                    elevation=Quantity(location.elevation, 'm'), timezone=tzinfo)

print(observer)

time = Time(jd, format='jd')

print(time)

dip = math.acos(EARTH_RADIUS / (EARTH_RADIUS + location.elevation))
alpha = 0.8333333333333333 + dip * RADIAN + 0.0052777777777778 * math.sqrt(location.elevation)

print(f"alpha={alpha}")

sunset = observer.sun_set_time(time, which="next", horizon=Quantity(-alpha, 'deg'))

sunset_jd = sunset.to_value('jd')
print(sunset_jd)

rd_sunset = from_julian_days(sunset_jd)

print(rd_sunset)

rd_sunset += location.zone / 24 # universal to standard




sunset_gregorian = GregorianDate()
sunset_gregorian.from_moment(rd_sunset)

print(sunset_gregorian)

day_time = rd_sunset - rd

print(day_time)

hms = to_hms(day_time)

print(hms)

# 15:38:22 vs 17:37:39



