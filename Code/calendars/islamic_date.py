from calendars.abstract_date import AbstractDate
from dataclasses import dataclass
import math
import tools

MONTHS_TRANSLIT = ["Muharram", "Safar", "Rabı‘ I", "Rabı‘ II", "Jumada I", "Jumada II", "Rajab", "Sha‘ban", "Ramadan",
                   "Shawwal", "Dhu al-Qa‘da", "Dhu al-Hijja"]


@dataclass
class IslamicDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Islamic calendar.
    """

    # region Data Fields
    year: int
    month: int
    day: int
    # endregion

    def __init__(self, year: int = 0, month: int = 0, day: int = 0):
        """
        Initialization.
        :param year: Islamic year.
        :param month: Islamic month
        :param day: Islamic day.
        """
        self.year = year
        self.month = month
        self.day = day

    def to_moment(self) -> float:
        """
        Converts the Islamic date to an RD time moment.
        :return: The RD time moment.
        RDM (6.3)
        """
        result = self.day + 29 * (self.month - 1) + math.floor((6 * self.month - 1) / 11) + (self.year - 1) * 354
        result += math.floor((3 + 11 * self.year) / 30) + tools.ISLAMIC_EPOCH - 1

        return result

    def from_moment(self, t: float):
        """
        Converts an RD time moment to an Islamic date.
        :param t: The RD time moment to convert.
        :return: None. The instance of IslamicDate is generated instead.
        RDM (6.4)
        """
        year = math.floor((30 * (t - tools.ISLAMIC_EPOCH) + 10646) / 10631)
        prior_days = t - IslamicDate(year, 1, 1).to_moment()
        month = math.floor((11 * prior_days + 330) / 325)
        day = t - IslamicDate(year, month, 1).to_moment() + 1

        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
