from calendars.abstract_date import AbstractDate
from dataclasses import dataclass
import math
import tools


class GregorianDate:
    """
    Preliminary declaration.
    """
    pass


@dataclass
class GregorianDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Gregorian calendar.
    """
    # region Data Fields
    year: int
    month: int
    day: int
    # endregion

    DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    DAYS_OF_WEEK = ["Sunday",
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday"]

    MONTHS = ["January",
              "February",
              "March",
              "April",
              "May",
              "June",
              "July",
              "August",
              "September",
              "October",
              "November",
              "December"]

    def __init__(self, year: int = 0, month: int = 0, day: int = 0):
        """
        Initialization
        :param year: Gregorian year.
        :param month: Gregorian month (January = 1)
        :param day: Gregorian day.
        """
        self.year = year
        self.month = month
        self.day = day

    # region AbstractDate
    def to_moment(self) -> float:
        """
        Converts the Gregorian date to an RD time moment.
        :return: The RD time moment.
        """
        return tools.datetime_data_to_moment([self.year, self.month, self.day])

    def from_moment(self, t: float) -> None:
        """
        Converts an RD time moment to a Gregorian date.
        :param t: The RD time moment to convert.
        :return: None. The instance of GregorianDate will be generated instead.
        """
        year = tools.gregorian_year_from_rata_die(t)
        self.year = int(year)

        new_year = GregorianDate(self.year, 1, 1)
        days_prior = t - new_year.to_moment()
        correction = 0

        march1 = GregorianDate(self.year, 3, 1)
        if t >= march1.to_moment():
            if tools.is_gregorian_leap_year(self.year):
                correction = 1
            else:
                correction = 2

        d = (12.0 * (days_prior + correction) + 373) / 367

        self.month = int(math.floor(d))

        d = t - GregorianDate(self.year, self.month, 1).to_moment()
        self.day = int(d) + 1

    # endregion

    def is_valid(self) -> bool:
        """
        A Gregorian date is valid if its month is within [1, 12], and its day is within the month.
        :return:
        """
        if self.month < 1 or self.month > 12:
            return False

        days_in_month = GregorianDate.DAYS_IN_MONTH[self.month - 1]

        if self.month == 2 and tools.is_gregorian_leap_year(self.year):
            days_in_month += 1

        return 0 < self.day <= days_in_month

    @property
    def day_of_week(self) -> int:
        """
        Number of the week's day: 0 == Sunday; 1 == Monday,..., 6 == Saturday.
        :return:
        """
        return int(tools.day_of_week_from_moment(self.to_moment()))

    def day_of_year(self) -> int:
        """
        Number of the day in the year.
        :return:
        """
        s = 0
        for i in range(self.month - 1):
            s += GregorianDate.DAYS_IN_MONTH[i]

        if tools.is_gregorian_leap_year(self.year) and self.month > 2:
            s += 1

        return s + self.day

    def week_number(self) -> int:
        """
        TODO: implement!
        :return:
        """
        pass

    # region String representation
    def to_string(self, format_string: str = None) -> str:
        """
        Formatting options (format is case-insensitive):
        "iso": ISO format ('1996-02-25')
        "ymd": 'year-month-day' (1996 February 25)
        "dmy": 'day-month-year' (25 February 1996)
        "ymdw": 'year-month-day-day of week' (1996 February 25, Sunday)
        "wdmy": 'day of week-day-month-year' (Sunday, 25 February 1996).
        Only English names of months and days of week are supported.
        """
        match (format_string.lower()):
            case "iso":
                return f"{self.year}-{self.month}-{self.day}"
            case "ymd":
                return f"{self.year} {GregorianDate.MONTHS[self.month - 1]} {self.day}"
            case "dmy":
                return f"{self.day} {GregorianDate.MONTHS[self.month - 1]} {self.year}"
            case "ymdw":
                return f"{self.year} {GregorianDate.MONTHS[self.month - 1]} {self.day}, {self.day_of_week}"
            case "wdmy":
                return f"{self.day_of_week}, {self.year} {GregorianDate.MONTHS[self.month - 1]} {self.day}"
            case _:
                return super().to_string()
    # endregion
