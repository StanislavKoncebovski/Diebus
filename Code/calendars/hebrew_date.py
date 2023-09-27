from calendars.abstract_date import AbstractDate
from dataclasses import dataclass
import math
import tools


@dataclass
class HebrewDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Hebrew calendar.
    """
    # region Data Fields
    year: int
    month: int
    day: int
    # endregion

    NISAN = 1
    TISHRI = 7
    CRITICAL_MONTHS = [2, 4, 6, 10, 13]
    AVERAGE_YEAR_LENGTH = 35975351 / 98496

    def __init__(self, year: int = 0, month: int = 0, day: int = 0):
        """
        Initialization
        :param year: Hebrew year.
        :param month: Hebrew month
        :param day: Hebrew day.
        """
        self.year = year
        self.month = month
        self.day = day

    def to_moment(self) -> float:
        """
        Converts the Hebrew date to an RD time moment.
        :return: The RD time moment.
        RDM (?)
        """
        t = self.hebrew_new_year(self.year) + self.day - 1

        if self.month < HebrewDate.TISHRI:
            last_month_in_year = self.last_month_of_hebrew_year(self.year)
            for m in range(HebrewDate.TISHRI, last_month_in_year + 1):
                last_day_of_month = self.last_day_of_hebrew_month(self.year, m)
                t += last_day_of_month

            for m in range(HebrewDate.NISAN, self.month):
                last_day_of_month = self.last_day_of_hebrew_month(self.year, m)
                t += last_day_of_month

        else:
            for m in range(HebrewDate.TISHRI, self.month):
                last_day_of_month = self.last_day_of_hebrew_month(self.year, m)
                t += last_day_of_month

        return t

    def from_moment(self, t: float):
        """
        Converts an RD time moment to a Hebrew date.
        :param t: The RD time moment to convert.
        :return: None. The instance of HebrewDate will be generated instead.
        """
        approx = 1 + math.floor((t - tools.HEBREW_EPOCH) / HebrewDate.AVERAGE_YEAR_LENGTH)
        year = int(approx - 1)

        while self.hebrew_new_year(year) <= t:
            year += 1

        year -= 1

        if t < HebrewDate(year, 1, 1).to_moment():
            start = HebrewDate.TISHRI
        else:
            start = HebrewDate.NISAN

        month = start

        while not t <= HebrewDate(year, month, self.last_day_of_hebrew_month(year, month)).to_moment():
            month += 1

        day = int(1 + t - HebrewDate(year, month, 1).to_moment())

        self.year = year
        self.month = month
        self.day = day

    # region Protected Auxiliary
    def hebrew_new_year(self, year: int) -> int:
        """
        RDM (7.10)
        :param year:
        :return:
        """
        return tools.HEBREW_EPOCH + self.hebrew_calendar_elapsed_days(year) + self.hebrew_new_year_delay(year)

    def hebrew_calendar_elapsed_days(self, year) -> float:
        """
        RDM (7.8)
        :param year:
        :return:
        """
        months_elapsed = math.floor((235 * year - 234) / 19)
        parts_elapsed = 12084 + 13753 * months_elapsed
        day = 29 * months_elapsed + math.floor(parts_elapsed / 25920)

        if int(tools.fmod(3 * (day + 1), 7)) < 3:
            return day + 1
        else:
            return day

    def hebrew_new_year_delay(self, year):
        """
        RDM (7.9)
        :param year:
        :return:
        """
        ny0 = int(self.hebrew_calendar_elapsed_days(year - 1))
        ny1 = int(self.hebrew_calendar_elapsed_days(year))
        ny2 = int(self.hebrew_calendar_elapsed_days(year + 1))

        if ny2 - ny1 == 356:
            return 2
        elif ny1 - ny0 == 382:
            return 1
        else:
            return 0

    def last_month_of_hebrew_year(self, year: int) -> int:
        """
        RDM (7.4)
        :param year:
        :return:
        """
        if tools.is_hebrew_leap_year(year):
            return 13
        else:
            return 12

    def last_day_of_hebrew_month(self, year: int, month: int) -> int:
        """
        RDM (7.11)
        :param year:
        :param month:
        :return:
        """
        if month in HebrewDate.CRITICAL_MONTHS or \
                (month == 12 and not tools.is_hebrew_leap_year(year)) or \
                (month == 8 and not self.is_long_mareshvan(year)) or \
                (month == 9 and self.is_short_kislev(year)):
            return 29
        else:
            return 30

    def is_long_mareshvan(self, year) -> bool:
        """
        RDM (7.12)
        :param year:
        :return:
        """
        days_in_hebrew_year = self._days_in_hebrew_year(year)

        if days_in_hebrew_year == 355 or days_in_hebrew_year == 385:
            return True
        else:
            return False

    def is_short_kislev(self, year) -> bool:
        """
        RDM (7.13)
        :param year:
        :return:
        """
        days_in_hebrew_year = self._days_in_hebrew_year(year)
        if days_in_hebrew_year == 353 or days_in_hebrew_year == 383:
            return True
        else:
            return False

    def _days_in_hebrew_year(self, year):
        return self.hebrew_new_year(year + 1) - self.hebrew_new_year(year)
    # endregion


if __name__ == '__main__':
    year = 3593
    month = 9
    day = 25

    hebrew = HebrewDate(year, month, day)

    t = hebrew.to_moment()

    print(t)
