from calendars.abstract_date import AbstractDate
from dataclasses import dataclass
import tools


@dataclass
class MayanHaabDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Mayan Haab calendar.
    """

    # region Data Fields
    month: int
    day: int
    # endregion

    EPOCH = tools.MAYAN_HAAB_EPOCH

    def __init__(self, month: int = 0, day: int = 0):
        self.month = month
        self.day = day

    def to_moment(self) -> float:
        """
        It is not possible to convert a haab date to an R.D. date because without a “year”
        there is no unique corresponding R.D. date. (RDM 10.2, p.146.)
        :return:
        """
        pass

    def from_moment(self, t: float) -> None:
        """
        Converts an RD time moment to a Mayan Haab date.
        :param t: The RD time moment to convert.
        :return: None. The instance of MayanHaabDate will be generated instead.
        RDM (10.6)
        """
        count = tools.fmod(t - MayanHaabDate.EPOCH, 365)
        self.day = int(tools.fmod(count, 20))
        self.month = 1 + int(tools.quotient(count, 20))
