import math
from dataclasses import dataclass

import location
import times
import tools
from calendars.abstract_date import AbstractDate


@dataclass
class PersianDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Astronomical Persian calendar (RDM 13.2, p. 213).
    """
    # region Data Fields
    year: int
    month: int
    day: int
    # endregion

    EPOCH = tools.PERSIAN_EPOCH

    def __init__(self, year: int = 0, month: int = 0, day: int = 0):
        """
        Initialization.
        :param year: Astronomical Persian year.
        :param month: Astronomical Persian month
        :param day: Astronomical Persian day.
        """
        self.year = year
        self.month = month
        self.day = day

    def to_moment(self) -> float:
        """
        Converts an Astronomical Persian date to an RD time moment.
        :return: The RD time moment.
        RDM (13.5)
        """
        year_factor = self.year - 1 if 0 < self.year else self.year
        new_year = self._new_year_on_or_before(
            PersianDate.EPOCH + 180 + math.floor(times.MEAN_TROPICAL_YEAR * year_factor))
        month_factor_1 = 31 if self.month <= 7 else 30
        return new_year - 1 + month_factor_1 * (self.month - 1) + 6 + self.day

    def from_moment(self, t: float):
        """
        Converts an RD time moment to a Astronomical Persian date.
        :param t: The RD time moment to convert.
        :return: None. The instance of PersianDate is generated instead.
        RDM (13.6)
        """
        pass

    # region Protected Auxiliary
    def _new_year_on_or_before(self, rd: float) -> int:
        """
        Fixed date of Astronomical Persian New Year on or before fixed date.
        :param rd: The fixed date (Rata Die).
        :return: The Rata Die value for the Persian new Year on or before the date.
        """
        approx = times.estimate_prior_solar_longitude(self._midday_in_tehran(rd), times.SPRING)

        i = int(math.floor(approx)) - 1

        while not times.solar_longitude(self._midday_in_tehran(i)) <= times.SPRING + 2:
            i += 1

        return i

    def _midday_in_tehran(self, rd: float) -> float:
        """
        Universal time of midday on fixed date in Tehran.
        :param rd: The Rate Die value of a date.
        :return: The Rate Die value of midday for that date in Tehran.
        """
        return times.standard_to_universal(times.midday(rd, location.TEHRAN), location.TEHRAN)
    # endregion


if __name__ == '__main__':
    year = 1374
    month = 12
    day = 6

    persian = PersianDate(year, month, day)

    t = persian.to_moment()

    print(t)
