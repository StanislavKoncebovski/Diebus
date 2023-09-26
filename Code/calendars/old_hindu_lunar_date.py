from calendars.abstract_date import AbstractDate
from calendars.old_hindu_solar_date import OldHinduSolarDate
from dataclasses import dataclass
import math
import tools


@dataclass
class OldHinduLunarDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Old Hindu Lunar calendar.
    """
    # region Data Fields
    year: int
    month: int
    is_leap_month: bool
    day: int
    # endregion

    ARYA_LUNAR_MONTH = 1577917500 / 53433336
    ARYA_LUNAR_DAY = ARYA_LUNAR_MONTH / 30

    def __init__(self, year: int = 0, month: int = 0, is_leap_lunar_month: bool = False, day: int = 0):
        """
        Initialization
        :param year: Old Hindu Solar year.
        :param month: Old Hindu Solar month
        :param day: Old Hindu Solar day.
        """
        self.year = year
        self.month = month
        self.is_leap_month = is_leap_lunar_month
        self.day = day

    def to_moment(self) -> float:
        """
        Converts the Old Hindu Lunar date to an RD time moment.
        :return: The RD time moment.
        RDM (??)
        """
        mina = (12 * self.year - 1) * OldHinduSolarDate.ARYA_SOLAR_MONTH
        lunar_new_year = OldHinduLunarDate.ARYA_LUNAR_MONTH * (tools.quotient(mina, OldHinduLunarDate.ARYA_LUNAR_MONTH) + 1)

        result = OldHinduSolarDate.EPOCH + lunar_new_year

        if not self.is_leap_month and math.ceil((lunar_new_year - mina) /
                                                (OldHinduSolarDate.ARYA_SOLAR_MONTH - OldHinduLunarDate.ARYA_LUNAR_MONTH)) <= self.month:
            result += OldHinduLunarDate.ARYA_LUNAR_MONTH * self.month
        else:
            result += OldHinduLunarDate.ARYA_LUNAR_MONTH * (self.month - 1)

        result += (self.day - 1) * OldHinduLunarDate.ARYA_LUNAR_DAY

        result += 0.75

        result = math.floor(result)

        return result

    def from_moment(self, t: float):
        """
        Converts an RD time moment to an Old Hindu Lunar date.
        :param t: The RD time moment to convert.
        :return: None. The instance of OldHinduLunarDate will be generated instead.
        RDM (??)
        """
        sun = t - OldHinduSolarDate.EPOCH + 0.25
        new_moon = sun - tools.fmod(sun, OldHinduLunarDate.ARYA_LUNAR_MONTH)
        self.is_leap_month = OldHinduSolarDate.ARYA_SOLAR_MONTH - \
                             OldHinduLunarDate.ARYA_LUNAR_MONTH >= tools.fmod(new_moon,
                                                                              OldHinduSolarDate.ARYA_SOLAR_MONTH) \
                             and tools.fmod(new_moon, OldHinduSolarDate.ARYA_SOLAR_MONTH) > 0

        self.month = 1 + int(tools.fmod(math.ceil(new_moon / OldHinduSolarDate.ARYA_SOLAR_MONTH), 12))
        self.day = 1 + int(tools.fmod(tools.quotient(sun, OldHinduLunarDate.ARYA_LUNAR_DAY), 30))
        self.year = int(math.ceil((new_moon + OldHinduSolarDate.ARYA_SOLAR_MONTH) /
                                  OldHinduSolarDate.ARYA_SOLAR_YEAR) - 1)
