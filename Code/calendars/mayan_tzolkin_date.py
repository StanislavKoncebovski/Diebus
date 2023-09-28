from calendars.abstract_date import AbstractDate
from dataclasses import dataclass
import tools


def ordinal(number: int, name: int):
    """
    Mayan Tzolkin Ordinal.
    RDM (10.10)
    :param number: The value of Mayan Tzolkin date number.
    :param name: The value of Mayan Tzolkin date name.
    :return: The Mayan Tzolkin ordinal.
    """
    return tools.fmod(number - 1 + 39 * (number - name), 260)


@dataclass
class MayanTzolkinDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Mayan Tzolkin calendar.
    """

    # region Data Fields
    number: int
    name: int
    # endregion

    EPOCH = tools.MAYAN_LONG_COUNT_EPOCH - ordinal(4, 20)

    def __init__(self, number: int = 0, name: int = 0):
        """
        Initialization.
        :param number:
        :param name:
        """
        self.number = number
        self.name = name

    def to_moment(self) -> float:
        """
        Just as with the Haab calendar, it is impossible to convert a tzolkin date to an R.D. date.  (RDM 10.2, p.148.)
        :return:
        """
        pass

    def from_moment(self, t: float) -> None:
        """
        Converts an RD time moment to a Mayan Tzolkin date.
        :param t: The RD time moment to convert.
        :return: None. The instance of MayanTzolkinDate is generated instead.
        RDM (10.9)
        """
        count = t - MayanTzolkinDate.EPOCH + 1
        self.number = int(tools.amod(count, 13))
        self.name = int(tools.amod(count, 20))
