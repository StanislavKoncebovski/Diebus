from calendars.abstract_date import AbstractDate
from dataclasses import dataclass
import tools

@dataclass
class MayanLongCountDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Mayan Long Count calendar.
    """

    # region Data Fields
    baktun: int
    katun: int
    tun: int
    uinal: int
    kin: int
    # endregion

    EPOCH = tools.MAYAN_LONG_COUNT_EPOCH

    # region Initialization
    def __init__(self, baktun: int=0, katun: int=0, tun: int=0, uinal: int=0, kin: int=0):
        """
        Initialization from data.
        :param baktun:
        :param katun:
        :param tun:
        :param uinal:
        :param kin:
        """
        self.baktun = baktun
        self.katun = katun
        self.tun = tun
        self.uinal = uinal
        self.kin = kin
    # endregion

    def to_moment(self) -> float:
        """
        Converts a Mayan Long Count date to an RD time moment.
        RDM (10.2).
        :return: The RD time moment.
        """
        return MayanLongCountDate.EPOCH + self.baktun * 144000 + self.katun * 7200 + \
               self.tun * 360 + self.uinal * 20 + self.kin

    def from_moment(self, t: float) -> None:
        """
        Converts an RD time moment to a Mayan Long Count date.
        RDM (3.4).
        :param t: The RD time moment to convert.
        :return: None. The instance of MayanLongCountDate is generated instead.
        RDM (10.3).
        :param t:
        :return:
        """
        long_count = t - MayanLongCountDate.EPOCH
        self.baktun = int(tools.quotient(long_count, 144000))
        day_of_baktun = tools.fmod(long_count, 144000)
        self.katun = int(tools.quotient(day_of_baktun, 7200))
        day_of_katun = tools.fmod(day_of_baktun, 7200)
        self.tun = int(tools.quotient(day_of_katun, 360))
        day_of_tun = tools.fmod(day_of_katun, 360)
        self.uinal = int(tools.quotient(day_of_tun, 20))
        self.kin = int(tools.fmod(day_of_tun, 20))



