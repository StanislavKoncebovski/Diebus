from dataclasses import dataclass

from calendars.abstract_date import AbstractDate
from location import Location
from times import standard_to_universal

# Ultimate Edition (UE) (16.5)
TEHRAN = Location("Tehran", 35.6966111, 51.423056, 0, 3.5)

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

    def _bahai_sunset(self, date: float):
        '''
        UE (16.6)
        '''
        return standard_to_universal(sunset(date, TEHRAN), TEHRAN)