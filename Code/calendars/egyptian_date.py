from calendars.abstract_date import AbstractDate
from dataclasses import dataclass
import math
import tools


@dataclass
class EgyptianDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Egyptian calendar.
    """

    # region Data Fields
    year: int
    month: int
    day: int
    # endregion

    EPOCH = tools.EGYPTIAN_EPOCH

    def __init__(self, year: int = 0, month: int = 0, day: int = 0):
        """
        Initialization
        :param year: Egyptian year.
        :param month: Egyptian month
        :param day: Egyptian day.
        """
        self.year = year
        self.month = month
        self.day = day

    def to_moment(self) -> float:
        """
        Converts the Egyptian date to an RD time moment.
        :return: The RD time moment.
        RDM (1.40)
        """
        return EgyptianDate.EPOCH + 365 * (self.year - 1) + 30 * (self.month - 1) + self.day - 1

    def from_moment(self, t: float):
        """
        Converts an RD time moment to a Egyptian date.
        :param t: The RD time moment to convert.
        :return: None. The instance of EgyptianDate will be generated instead.
        RDM (1.41)
        """
        days = t - EgyptianDate.EPOCH
        self.year = math.floor(days / 365) + 1
        self.month = math.floor((days % 365) / 30) + 1
        self.day = days - 365 * (self.year - 1) - 30 * (self.month - 1) + 1
