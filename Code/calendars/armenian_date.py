from calendars.abstract_date import AbstractDate
from calendars.egyptian_date import EgyptianDate
from dataclasses import dataclass
import tools


@dataclass
class ArmenianDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Armenian calendar (RDM 1.9, p. 25).
    """

    # region Data Fields
    year: int
    month: int
    day: int
    # endregion

    EPOCH = tools.ARMENIAN_EPOCH

    def __init__(self, year: int = 0, month: int = 0, day: int = 0):
        """
        Initialization
        :param year: Armenian year.
        :param month: Armenian month.
        :param day: Armenian day.
        """
        self.year = year
        self.month = month
        self.day = day

    def to_moment(self) -> float:
        """
        Converts the Armenian date to an RD time moment.
        :return: The RD time moment.
        RDM (1.30)
        """
        return ArmenianDate.EPOCH + EgyptianDate(self.year, self.month, self.day).to_moment() - EgyptianDate.EPOCH

    def from_moment(self, t: float):
        """
        Converts an RD time moment to an Armenian date.
        :param t: The RD time moment to convert.
        :return: None. The instance of ArmenianDate is generated instead.
        RDM (1.31)
        """
        armenian = EgyptianDate()
        armenian.from_moment(t + EgyptianDate.EPOCH - ArmenianDate.EPOCH)

        self.year = armenian.year
        self.month = armenian.month
        self.day = armenian.day
