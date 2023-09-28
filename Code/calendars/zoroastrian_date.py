from calendars.abstract_date import AbstractDate
from calendars.egyptian_date import EgyptianDate
from dataclasses import dataclass
import tools


@dataclass
class ZoroastrianDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Zoroastrian calendar.
    NB: There were no test data in RDM's calendrica.
    """
    # region Data Fields
    year: int
    month: int
    day: int
    # endregion

    EPOCH = tools.ZOROASTRIAN_EPOCH

    def __init__(self, year: int = 0, month: int = 0, day: int = 0):
        """
        Initialization
        :param year: Zoroastrian year.
        :param month: Zoroastrian month
        :param day: Zoroastrian day.
        """
        self.year = year
        self.month = month
        self.day = day

    def to_moment(self) -> float:
        """
        Converts the Zoroastrian date to an RD time moment.
        :return: The RD time moment.
        RDM (1.40)
        """
        return ZoroastrianDate.EPOCH + EgyptianDate(self.year, self.month, self.day).to_moment() - EgyptianDate.EPOCH

    def from_moment(self, t: float):
        """
        Converts an RD time moment to a Zoroastrian date.
        :param t: The RD time moment to convert.
        :return: None. The instance of Zoroastrian is generated instead.
        RDM (1.41)
        """
        egyptian = EgyptianDate()
        egyptian.from_moment(t + EgyptianDate.EPOCH - ZoroastrianDate.EPOCH)

        self.year = egyptian.year
        self.month = egyptian.month
        self.day = egyptian.day
