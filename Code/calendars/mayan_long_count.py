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

    def __init__(self, baktun: int=0, katun: int=0, tun: int=0, uinal: int=0, kin: int=0):
        self.baktun = baktun
        self.katun = katun
        self.tun = tun
        self.uinal = uinal
        self.kin = kin

    def to_moment(self) -> float:
        return MayanLongCountDate.EPOCH + self.baktun * 144000 + self.katun * 7200 + \
               self.tun * 360 + self.uinal * 20 + self.kin

    def from_moment(self, t: float) -> None:
        long_count = t - MayanLongCountDate.EPOCH
        self.baktun = int(tools.quotient(long_count, 144000))
        day_of_baktun = tools.fmod(long_count, 144000)
        self.katun = int(tools.quotient(day_of_baktun, 7200))
        day_of_katun = tools.fmod(day_of_baktun, 7200)
        self.tun = int(tools.quotient(day_of_katun, 360))
        day_of_tun = tools.fmod(day_of_katun, 360)
        self.uinal = int(tools.quotient(day_of_tun, 20))
        self.kin = int(tools.fmod(day_of_tun, 20))



