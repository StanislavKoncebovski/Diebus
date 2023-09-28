from calendars.abstract_date import AbstractDate
from dataclasses import dataclass
import math
import tools


@dataclass
class OldHinduSolarDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Old Hindu Solar calendar.
    """
    # region Data Fields
    year: int
    month: int
    day: int
    # endregion

    # Fixed date of start of the Hindu calendar (Kali Yuga).
    EPOCH = tools.HINDU_EPOCH
    ARYA_SOLAR_YEAR = 1577917500 / 4320000
    ARYA_SOLAR_MONTH = ARYA_SOLAR_YEAR / 12
    ARYA_JOVIAN_PERIOD = 1577917500 / 364224

    def __init__(self, year: int = 0, month: int = 0, day: int = 0):
        """
        Initialization.
        :param year: Old Hindu Solar year.
        :param month: Old Hindu Solar month
        :param day: Old Hindu Solar day.
        """
        self.year = year
        self.month = month
        self.day = day

    def to_moment(self) -> float:
        """
        Converts the Old Hindu Solar date to an RD time moment.
        :return: The RD time moment.
        RDM (9.7).
        """
        result = OldHinduSolarDate.EPOCH + self.year * OldHinduSolarDate.ARYA_SOLAR_YEAR + \
                 (self.month - 1) * OldHinduSolarDate.ARYA_SOLAR_MONTH + self.day - 0.25

        return math.floor(result)

    def from_moment(self, t: float):
        """
        Converts an RD time moment to an Old Hindu Solar date.
        :param t: The RD time moment to convert.
        :return: None. The instance of OldHinduSolarDate will be generated instead.
        RDM (9.8).
        """
        sun = (t - OldHinduSolarDate.EPOCH) + 0.25
        year = math.floor(sun / OldHinduSolarDate.ARYA_SOLAR_YEAR)

        month = 1 + int(tools.fmod(tools.quotient(sun,  OldHinduSolarDate.ARYA_SOLAR_MONTH), 12))
        day = 1 + int(math.floor(tools.fmod(sun, OldHinduSolarDate.ARYA_SOLAR_MONTH)))

        self.year = year
        self.month = month
        self.day = day

