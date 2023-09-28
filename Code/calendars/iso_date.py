from calendars.abstract_date import AbstractDate
from calendars.gregorian_date import GregorianDate
from dataclasses import dataclass
import math
import tools


class IsoDate:
    """
    Preliminary declaration.
    """
    pass

@dataclass
class IsoDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for ISO date (ISO_8601).
    Sources: https://en.wikipedia.org/wiki/ISO_8601, RDM, RDU.
    """
    # region Data Fields
    year: int
    week: int
    day: int
    # endregion

    def __init__(self, year: int = 0, week: int = 0, day: int = 0):
        """
        Initialization.
        :param year: (Gregorian) year.
        :param week: Week number.
        :param day: Day of week.
        """
        self.year = year
        self.week = week
        self.day = day

    # region AbstractDate
    def to_moment(self) -> float:
        """
        Converts the ISO date to an RD time moment.
        RDM (5.1).
        :return: The RD time moment.
        """
        return tools.n_th_k_day(self.week, 0, GregorianDate(self.year - 1, 12, 28).to_moment()) + self.day

    def from_moment(self, t: float) -> None:
        """
        Converts an RD time moment to an ISO date.
        RDM (5.2).
        :param t: The RD time moment to convert.
        :return: None. The instance of IsoDate will be generated instead.
        """
        # TODO: hier bug!
        gd = GregorianDate()
        gd.from_moment(t -3)
        self.year = gd.year

        if t >= IsoDate(self.year + 1, 1, 1).to_moment():
            self.year += 1

        excess = (t - IsoDate(self.year, 1, 1).to_moment()) / 7

        self.week = int(math.floor(excess)) + 1

        self.day = int(tools.amod(t, 7))
    # endregion

    # region String representation
    def __str__(self):
        """
        Source: https://en.wikipedia.org/wiki/ISO_8601
        Week with weekday	2022-W01-3
        :return:
        """
        return f"{self.year}-W{self.week:02}-{self.day}"
    # endregion

if __name__ == '__main__':
    t = 728714

    id = IsoDate()
    id.from_moment(t)

    print(id)
# expected: year = 1996, week =	8, day = 7
