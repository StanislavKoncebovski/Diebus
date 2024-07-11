from dataclasses import dataclass

from astropy.units import Quantity

from calendars.abstract_date import AbstractDate
from calendars.gregorian_date import GregorianDate
from location import Location, TEHRAN
from astroplan import Observer
from astropy.time import Time

from tools import to_julian_days, from_julian_days


# Ultimate Edition (UE) (16.5)
# TEHRAN = Location("Tehran", 35.6966111, 51.423056, 0, 3.5)

@dataclass
class BahaiDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for astronomical Bahai calendar.
    """
    # region Data Fields
    major: int
    cycle: int
    year: int
    month: int
    day: int
    # endregion

    # region Initialization
    def __init__(self, major: int = 0, cycle: int = 0, year: int = 0, month: int = 0, day: int = 0):
        """
        Creates an instance of WesternBahaiDate from constituent values.
        :param major:   The number of the 361-year major cycle (Kull-i-Shay) [RDM 15.2, p. 231]
        :param cycle:   The number of the 19-year cycle (Vahid) [RDM 15.2, p. 230]
        :param year:    The number of the year within the Vahid cycle (1 = Alif, ..., 19 = Vahid).
        :param month:   The number of the month in the year (1 = Bahá, ..., 19 = Alá)
        :param day:     The number of the day in the month.
        """
        self.major = major
        self.cycle = cycle
        self.year = year
        self.month = month
        self.day = day
    # endregion

    def to_moment(self) -> float:
        """
        Converts the astronomical Bahai date to the RD time moment.
        RDM (14.3).
        :return: The RD time moment.
        """
        ...

    def from_moment(self, t: float) -> None:
        """
        Converts an RD time moment to an instance of BahaiDate.
        RDM (14.4).
        :param t: The RD time moment to convert.
        :return: None. The instance of WesternBahaiDate will be generated instead.
        """
        ...

    def bahai_sunset(self, t: float) -> float:
        """
        Calculates the RD moment of sunset in Tehran for the day indicated by the value of the RD datetime.
        :param t: The moment of time to calculate the next sunset for.
        :return: The RD value of the sunset in Tehran for the defined datetime (UTC).
        """

        # define the observer position
        observer = Observer(name=TEHRAN.name, latitude=TEHRAN.latitude,
                            longitude=TEHRAN.longitude, elevation=Quantity(0, 'm'))

        # create an instance of astroplan.Time
        jd = to_julian_days(t)
        time = Time(str(jd), format='jd')
        sunset = observer.sun_set_time(time, which="next")

        utc = sunset.to_value('jd')


if __name__ == '__main__':
    gregorian = GregorianDate(2024, 7, 11)
    t = gregorian.to_moment()
    print(t)


    bd = BahaiDate()
    sunset = bd.bahai_sunset(t)
    print(sunset)

    # observer = Observer(name="Potsdam", latitude=52.406001,
    #                     longitude=13.059181, elevation=Quantity(0, 'm'))
    #
    # jd = to_julian_days(t)
    #
    # time = Time(str(jd), format='jd')
    # sunset = observer.sun_set_time(time, which="next")
    #
    # t_sunset = from_julian_days(sunset.tt)
    # print(t_sunset)

