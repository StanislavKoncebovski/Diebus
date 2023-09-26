from calendars.abstract_date import AbstractDate
from dataclasses import dataclass
import tools

PANCAWARA_I = [5, 9, 7, 4, 8]
SAPTAWARA_J = [5, 4, 3, 7, 8, 6, 9]

@dataclass
class BalineseDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Balinese Pawukon calendar.
    """

    # region Data Fields
    luang: int
    dwiwara: int
    triwara: int
    caturwara: int
    pancawara: int
    sadwara: int
    saptawara: int
    asatawara: int
    sangawara: int
    dasawara: int
    # endregion

    EPOCH = tools.BALINESE_EPOCH

    def __init__(self,  luang: int = 0,
                        dwiwara: int = 0,
                        triwara: int = 0,
                        caturwara: int = 0,
                        pancawara: int = 0,
                        sadwara: int = 0,
                        saptawara: int = 0,
                        asatawara: int = 0,
                        sangawara: int = 0,
                        dasawara: int = 0,
                 ):
        self.luang		= luang
        self.dwiwara	= dwiwara
        self.triwara	= triwara
        self.caturwara	= caturwara
        self.pancawara	= pancawara
        self.sadwara	= sadwara
        self.saptawara	= saptawara
        self.asatawara	= asatawara
        self.sangawara	= sangawara
        self.dasawara	= dasawara


    def from_moment(self, t: float):
        """
        Converts an RD time moment to a Balinese date.
        :param t: The RD time moment to convert.
        :return: None. The instance of BalineseDate will be generated instead.
        RDM (?.?)
        """
        self.luang		= self._is_day_luang_from_fixed(t)
        self.dwiwara	= self.dwiwara_from_fixed(t)
        self.triwara	= self.triwara_from_fixed(t)
        self.caturwara	= self.caturwara_from_fixed(t)
        self.pancawara	= self.pancawara_from_fixed(t)
        self.sadwara	= self.sadwara_from_fixed(t)
        self.saptawara	= self.saptawara_from_fixed(t)
        self.asatawara	= self.asatawara_from_fixed(t)
        self.sangawara	= self.sangawara_from_fixed(t)
        self.dasawara	= self.dasawara_from_fixed(t)

    def _is_day_luang_from_fixed(self, t: float) -> bool:
        return int(tools.fmod(self.dasawara_from_fixed(t), 2)) == 0

    def dwiwara_from_fixed(self, t):
        return int(tools.fmod(self.dasawara_from_fixed(t) + 1, 2)) + 1

    def triwara_from_fixed(self, t):
        return int(tools.fmod(self.day_from_fixed(t), 3)) + 1

    def caturwara_from_fixed(self, t):
        return int(tools.amod(self.asatawara_from_fixed(t), 4))

    def pancawara_from_fixed(self, t) -> int:
        return int(tools.fmod(self.day_from_fixed(t) + 1, 5)) + 1

    def sadwara_from_fixed(self, t):
        return int(tools.fmod(self.day_from_fixed(t), 6)) + 1

    def saptawara_from_fixed(self, t) -> int:
        return int(tools.fmod(self.day_from_fixed(t), 7)) + 1

    def asatawara_from_fixed(self, t) -> int:
        day = self.day_from_fixed(t)
        return int(tools.fmod(tools.fmax(6, 4 + tools.fmod(day - 70, 210)), 8)) + 1

    def sangawara_from_fixed(self, t) -> int:
        return int(tools.fmod(tools.fmax(0, self.day_from_fixed(t) - 3), 9)) +1

    def dasawara_from_fixed(self, t) -> int:
        i: int = self.pancawara_from_fixed(t)
        j: int = self.saptawara_from_fixed(t)

        return int(tools.fmod(PANCAWARA_I[i - 1] + SAPTAWARA_J[j - 1] + 1, 10))

    def day_from_fixed(self, t: float):
        return int(tools.fmod(t - BalineseDate.EPOCH, 210))

if __name__ == '__main__':
    balinese_epoch = tools.julian_day_to_rate_die(146)
    print(balinese_epoch)
