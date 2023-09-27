from calendars.abstract_date import AbstractDate
from calendars.gregorian_date import GregorianDate
from dataclasses import dataclass
import math
import tools


@dataclass
class JulianDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Julian calendar.
    """
    # region Data Fields
    year: int
    month: int
    day: int
    # endregion

    EPOCH = int(GregorianDate(0, 12, 30).to_moment())

    def __init__(self, year: int = 0, month: int = 0, day: int = 0):
        """
        Initialization
        :param year: Julian year.
        :param month: Julian month
        :param day: Julian day.
        """
        self.year = year
        self.month = month
        self.day = day

    def to_moment(self) -> float:
        """
        Converts the Julian date to an RD time moment.
        :return: The RD time moment.
        """
        y = self.year + 1 if self.year < 0 else self.year
        result = JulianDate.EPOCH - 1 + 365 * (y - 1) + math.floor((y - 1) / 4)
        result += math.floor((367 * self.month - 362) / 12)
        if self.month > 2:
            result += -1 if tools.is_julian_leap_year(self.year) else -2
        result += self.day

        return result

    def from_moment(self, t: float):
        """
        Converts an RD time moment to a Julian date.
        :param t: The RD time moment to convert.
        :return: None. The instance of JulianDate will be generated instead.
        RDM (3.4), p. 65.
        """
        approx = math.floor((4 * (t - JulianDate.EPOCH) + 1464) / 1461)
        approx = int(approx)
        self.year = approx if approx > 0 else approx - 1
        julian_start = JulianDate(self.year, 1, 1)
        prior_days = t - julian_start.to_moment()

        correction = 2
        if t < JulianDate(self.year, 3, 1).to_moment():
            correction = 0

        if t >= JulianDate(self.year, 3, 1).to_moment() and tools.is_julian_leap_year(self.year):
            correction = 1

        self.month = int(math.floor((12 * (prior_days + correction) + 373) / 367))

        self.day = int(t - JulianDate(self.year, self.month, 1).to_moment() + 1)

    # region String representation
    def to_string(self, format: str = None) -> str:
        """
        Formatting options (format is case-insensitive):
        "iso": ISO format ('1996-02-25 JE')
        "ymd": 'year-month-day' (1996 February 25 JE)
        "dmy": 'day-month-year' (25 February 1996 JE)
        Only English names of months and days of week are supported.
        """
        match(format.lower()):
            case "iso":
                return f"{self.year}-{self.month}-{self.day}"
            case "ymd":
                return f"{self.year} {GregorianDate.MONTHS[self.month - 1]} {self.day}"
            case "dmy":
                return f"{self.day} {GregorianDate.MONTHS[self.month - 1]} {self.year}"
            case _ :
                return super().to_string()
    # endregion

