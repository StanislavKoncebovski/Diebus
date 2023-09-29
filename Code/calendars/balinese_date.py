from calendars.abstract_date import AbstractDate
from dataclasses import dataclass
import numpy as np
import tools

PANCAWARA_I = [5, 9, 7, 4, 8]
SAPTAWARA_J = [5, 4, 3, 7, 8, 6, 9]


@dataclass
class BalineseDate(AbstractDate):
    """
    Implements conversion from RD time moment for Balinese Pawukon calendar (RDM Chapter 1, p. 153).
    Conversion from a Balinese date to RD is impossible ("...there is no way to convert a Pawukon date into a
    fixed date" - RDM, p. 159) and is unsupported in ths calendar.
    """

    # region Data Fields (Balinese Pawukon date components).
    luang: bool
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

    # region Initialization
    def __init__(self, luang: bool = False,
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
        """
        Initialization. Creates an instance of BalineseDate from date components.
        :param luang:
        :param dwiwara:
        :param triwara:
        :param caturwara:
        :param pancawara:
        :param sadwara:
        :param saptawara:
        :param asatawara:
        :param sangawara:
        :param dasawara:
        """
        self.luang = luang
        self.dwiwara = dwiwara
        self.triwara = triwara
        self.caturwara = caturwara
        self.pancawara = pancawara
        self.sadwara = sadwara
        self.saptawara = saptawara
        self.asatawara = asatawara
        self.sangawara = sangawara
        self.dasawara = dasawara

    # endregion
    def from_moment(self, t: float):
        """
        Converts an RD time moment to a Balinese date.
        :param t: The RD time moment to convert.
        :return: None. The instance of BalineseDate is generated instead.
        RDM (11.1)
        """
        self.luang = self._is_day_luang_from_fixed(t)
        self.dwiwara = self._dwiwara_from_fixed(t)
        self.triwara = self._triwara_from_fixed(t)
        self.caturwara = self._caturwara_from_fixed(t)
        self.pancawara = self._pancawara_from_fixed(t)
        self.sadwara = self._sadwara_from_fixed(t)
        self.saptawara = self._saptawara_from_fixed(t)
        self.asatawara = self._asatawara_from_fixed(t)
        self.sangawara = self._sangawara_from_fixed(t)
        self.dasawara = self._dasawara_from_fixed(t)

    # region Protected Auxiliary
    def _is_day_luang_from_fixed(self, t: float) -> bool:
        """
        RDM (11.11)
        :param t:
        :return:
        """
        return int(tools.fmod(self._dasawara_from_fixed(t), 2)) == 0

    def _dwiwara_from_fixed(self, t):
        """
        RDM (11.10)
        :param t:
        :return:
        """
        return int(tools.fmod(self._dasawara_from_fixed(t) + 1, 2)) + 1

    def _triwara_from_fixed(self, t):
        """
        RDM (11.4)
        :param t:
        :return:
        """
        return int(tools.fmod(self._day_from_fixed(t), 3)) + 1

    def _caturwara_from_fixed(self, t):
        """
        RDM (11.14)
        :param t:
        :return:
        """
        return int(tools.amod(self._asatawara_from_fixed(t), 4))

    def _pancawara_from_fixed(self, t) -> int:
        """
        RDM (11.7)
        :param t:
        :return:
        """
        return int(tools.fmod(self._day_from_fixed(t) + 1, 5)) + 1

    def _sadwara_from_fixed(self, t):
        """
        RDM (11.5)
        :param t:
        :return:
        """
        return int(tools.fmod(self._day_from_fixed(t), 6)) + 1

    def _saptawara_from_fixed(self, t) -> int:
        """
        RDM (11.6)
        :param t:
        :return:
        """
        return int(tools.fmod(self._day_from_fixed(t), 7)) + 1

    def _asatawara_from_fixed(self, t) -> int:
        """
        RDM (11.13)
        :param t:
        :return:
        """
        day = self._day_from_fixed(t)
        return int(tools.fmod(np.maximum(6, 4 + tools.fmod(day - 70, 210)), 8)) + 1

    def _sangawara_from_fixed(self, t) -> int:
        """
        RDM (11.12)
        :param t:
        :return:
        """
        return int(tools.fmod(np.maximum(0, self._day_from_fixed(t) - 3), 9)) + 1

    def _dasawara_from_fixed(self, t) -> int:
        """
        RDM (11.9)
        :param t:
        :return:
        """
        i: int = self._pancawara_from_fixed(t)
        j: int = self._saptawara_from_fixed(t)

        return int(tools.fmod(PANCAWARA_I[i - 1] + SAPTAWARA_J[j - 1] + 1, 10))

    def _day_from_fixed(self, t: float):
        """
        RDM (11.3)
        :param t:
        :return:
        """
        return int(tools.fmod(t - BalineseDate.EPOCH, 210))
    # endregion
