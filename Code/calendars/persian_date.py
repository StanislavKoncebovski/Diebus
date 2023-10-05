from dataclasses import dataclass
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
        pass


    def from_moment(self, t: float):
        """
        Converts an RD time moment to a Astronomical Persian date.
        :param t: The RD time moment to convert.
        :return: None. The instance of PersianDate is generated instead.
        RDM (13.6)
        """
        pass
