from calendars.abstract_date import AbstractDate
from dataclasses import dataclass
import math
import tools

@dataclass
class ArithmeticPersianDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Arithmetic Persian calendar.
    """

    # region Data Fields
    year: int
    month: int
    day: int
    # endregion

    EPOCH = tools.PERSIAN_EPOCH

    def __init__(self, year: int = 0, month: int = 0, day: int = 0):
        """
        Initialization
        :param year: Armenian year.
        :param month: Armenian month
        :param day: Armenian day.
        """
        self.year = year
        self.month = month
        self.day = day

    def to_moment(self) -> float:
        """
        Converts the Arithmetic Persian date to an RD time moment.
        :return: The RD time moment.
        RDM (13.8)
        """
        y = self.year - 473
        if self.year > 0:
            y -= 1

        year = tools.fmod(y, 2820) + 474

        result = ArithmeticPersianDate.EPOCH - 1 + 1029983 * math.floor(y / 2820) + 365 * (year - 1)
        result += math.floor((682 * year - 110) / 2816)

        if self.month <= 7:
            result += 31 * (self.month - 1)
        else:
            result += 30 * (self.month - 1) + 6

        result += self.day

        return result

    def from_moment(self, t: float):
        """
        Converts an RD time moment to a Arithmetic Persian date.
        :param t: The RD time moment to convert.
        :return: None. The instance of ArithmeticPersianDate will be generated instead.
        RDM (13.9, 10)
        """
        self.year = self._year_from_fixed(t)
        day_of_year = 1 + t - ArithmeticPersianDate(self.year, 1, 1).to_moment()
        if day_of_year < 186:
            self.month = int(math.ceil(day_of_year / 31))
        else:
            self.month = int(math.ceil((day_of_year - 6) / 30))

        self.day = int(t - ArithmeticPersianDate(self.year, self.month, 1).to_moment() + 1)

    def _year_from_fixed(self, t: float) -> int:
        """
        Converts an RD time moment to an Arithmetic Persian date.
        :param t: The RD time moment to convert.
        :return: None. The instance of ArithmeticPersianDate will be generated instead.
        RDM (1.41)
        """
        l0 = t - ArithmeticPersianDate(475, 1, 1).to_moment()
        n2820 = math.floor(l0 / 1029983)
        d1 = tools.fmod(l0, 1029983)
        if d1 == 1029982:
            y2820 = 2820
        else:
            y2820 = math.floor((2816 * d1 + 1031337) / 1028522)

        year = 474 + 2820 * n2820 + y2820

        if year > 0:
            return year
        else:
            return year - 1
