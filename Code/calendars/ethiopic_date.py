from calendars.abstract_date import AbstractDate
from calendars.coptic_date import CopticDate
from dataclasses import dataclass
import tools


@dataclass
class EthiopicDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Coptic calendar.
    """

    # region Data Fields
    year: int
    month: int
    day: int
    # endregion

    EPOCH = tools.ETHIOPIC_EPOCH

    def __init__(self, year: int = 0, month: int = 0, day: int = 0):
        """
        Initialization.
        :param year: Ethiopic year.
        :param month: Ethiopic month
        :param day: Ethiopic day.
        """
        self.year = year
        self.month = month
        self.day = day

    def to_moment(self) -> float:
         """
        Converts the Ethiopic date to an RD time moment.
        RDM (4.6).
        :return: The RD time moment.
         """
         return EthiopicDate.EPOCH + CopticDate(self.year, self.month, self.day).to_moment() - CopticDate.EPOCH

    def from_moment(self, t: float):
        """
        Converts an RD time moment to an Ethiopic date.
        RDM (4.7).
        :param t: The RD time moment to convert.
        :return: None. The instance of EthiopicDate is generated instead.
        :param t:
        :return:
        """
        ethiopic = CopticDate()
        ethiopic.from_moment(t + CopticDate.EPOCH - EthiopicDate.EPOCH)

        self.year = ethiopic.year
        self.month = ethiopic.month
        self.day = ethiopic.day
