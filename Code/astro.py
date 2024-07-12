import math
from datetime import datetime
from typing import Optional

from astroplan import Observer
from astropy.time import Time
from astropy.units import Quantity

from location import Location
from tools import to_julian_days, EARTH_RADIUS, RADIAN, from_julian_days


class Astro:
    """
    Contains routines needed for the calculation of astronomical events, such as sunrise and sunset.
    """
    @classmethod
    def sunset(cls, rd: float, location: Location) -> Optional[float]:
        """
        Calculates the sunset in a location on a defined date.
        Uses the Observer.sun_set_time() method of the Observer class of the astroplan library.
        :param rd: The RD value of the date to calculate the sunset for.
        :param location: The location to calculate the sunset for.
        :return: The RD value of the sunset moment, if it exists, otherwise None.
        """
        offset_timedelta = datetime.timedelta(hours=location.zone)
        tzinfo = datetime.timezone(offset_timedelta)

        # Convert Location to astroplan.Observer
        observer = Observer(name=location.name, latitude=location.latitude, longitude=location.longitude,
                            elevation=Quantity(location.elevation, 'm'), timezone=tzinfo)

        # Convert RD to Julian days
        jd = to_julian_days(rd)

        # Create an instance of Time
        time = Time(jd, format='jd')

        alpha = Astro.horizon(location)

        # Sunset value as an instance of Time
        sunset = observer.sun_set_time(time, which="next", horizon=Quantity(-alpha, 'deg'))

        # Sunset value in Julian days (universal time)
        sunset_jd = sunset.to_value('jd')

        # Sunset value in RD units
        sunset_rd = from_julian_days(sunset_jd)

        # Convert to standard time of the location
        sunset_rd += location.zone / 24  # universal to standard

        return rd

    @classmethod
    def horizon(cls, location: Location) -> float:
        """
        Calculates the visible horizon for the location taking into account the half visible diameter of the Sun,
        refraction, and elevation. (RDU 13.72)
        :param location: The location to calculate the horizon for.
        :return: The value of the visible horizon.
        """
        h = max(0.0, location.elevation)
        dip = math.acos(EARTH_RADIUS / (EARTH_RADIUS + location.elevation))
        return 0.8333333333333333 + dip * RADIAN + 0.0052777777777778 * math.sqrt(location.elevation)
