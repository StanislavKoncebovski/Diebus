from calendars.abstract_date import AbstractDate
from calendars.julian_date import JulianDate
from dataclasses import dataclass
import tools

KALENDS = 1
NONES = 2
IDES = 3

COUNT_NAMES = ["",
		"pridie ",
		"ante diem iii ",
		"ante diem iv ",
		"ante diem v ",
		"ante diem vi ",
		"ante diem vii ",
		"ante diem viii ",
		"ante diem ix ",
		"ante diem x ",
		"ante diem xi ",
		"ante diem xii ",
		"ante diem xiii ",
		"ante diem xiv ",
		"ante diem xv ",
		"ante diem xvi ",
		"ante diem xvii ",
		"ante diem xviii ",
		"ante diem xix "]

EVENT_NAMES = ["Kalens", "Nones", "Ides"]

@dataclass
class RomanDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Roman calendar.
    RDM: "In ancient Rome it was customary to refer to days of the month by counting down
    to certain key events in the month: the kalends, the nones, and the ides.This custom... coming from a
    time in which the month was still synchronized with the lunar cycle: the kalends
    were the new moon, the nones the first quarter moon, and the ides the full moon.
    """

    # region Data Fields
    year: int
    month: int
    event: int          # The next event (KALENDS / NONES / IDES)
    count: int          # The inclusive count of days until the event
    is_leap_day: bool   # The leap day indicator
    # endregion

    def __init__(self, year: int = 0, month: int = 0, event: int = 0, count: int = 0, is_leap_day: bool = False):
        """
        Initialization
        :param year: The Julian year
        :param month: The Julian month
        :param event: The next event (KALENDS / NONES / IDES)
        :param count: The inclusive count of days until the event
        :param is_leap_day: The leap day indicator
        """
        self.year = year
        self.month = month
        self.event = event
        self.count = count
        self.is_leap_day = is_leap_day

    def to_moment(self) -> float:
        """
        Converts the Roman date to an RD time moment.
        :return: The RD time moment.
        RDM (3.10)
        """
        approx = 0

        if self.event == KALENDS:
            approx = JulianDate(self.year, self.month, 1).to_moment()
        elif self.event == NONES:
            approx = JulianDate(self.year, self.month, self._nones_of_month(self.month)).to_moment()
        elif self.event == IDES:
            approx = JulianDate(self.year, self.month, self._ides_of_month(self.month)).to_moment()

        result = approx - self.count

        if tools.is_leap_julian_year(self.year) and self.month == 3 and self.event == KALENDS and (16 >= self.count >= 6):
            result += 0
        else:
            result += 1

        if self.is_leap_day:
            result += 1

        return result

    def from_moment(self, t: float):
        """
        Converts an RD time moment to a Roman date.
        :param t: The RD time moment to convert.
        :return: None. The instance of RomanDate will be generated instead.
        RDM (3.11)
        """
        j = JulianDate()
        j.from_moment(t)

        m = j.month
        d = j.day
        y = j.year

        month_prime = int(tools.amod(Decimal(m + 1), 12))

        if month_prime == 1:
            year_prime = y + 1
        else:
            year_prime = y

        kalends1 = RomanDate(year_prime, month_prime, KALENDS, 1, False).to_moment()

        if d == 1:
            self.year = y
            self.month = m
            self.event = KALENDS
            self.count = 1
            self.is_leap_day = False

        elif d <= self._nones_of_month(m):
            self.year = y
            self.month = m
            self.event = NONES
            self.count = self._nones_of_month(m) - d + 1
            self.is_leap_day = False

        elif d <= self._ides_of_month(m):
            self.year = y
            self.month = m
            self.event = IDES
            self.count = self._ides_of_month(m) - d + 1
            self.is_leap_day = False

        elif m != 2 or not tools.is_leap_julian_year(y):
            self.year = year_prime
            self.month = month_prime
            self.event = KALENDS
            self.count = int(kalends1 - t + 1)
            self.is_leap_day = False

        elif d < 25:
            self.year = y
            self.month = 3
            self.event = KALENDS
            self.count = 30 - d
            self.is_leap_day = False

        else:
            self.year = y
            self.month = 3
            self.event = KALENDS
            self.count = 31 - d
            self.is_leap_day = (d == 25)

    #region Protected Auxiliary
    def _ides_of_month(self, month: int):
        if month == 3 or month == 5 or month == 7 or month == 10:
            return 15
        else:
            return 13


    def _nones_of_month(self, month: int):
        return self._ides_of_month(month) - 8
    # endregion
