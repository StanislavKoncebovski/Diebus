from calendars.abstract_date import AbstractDate
from dataclasses import dataclass
import math
import tools

# region Month and Weekdays names
# Sources: RDM p. 75,
# https://en.wikipedia.org/wiki/Coptic_calendar

MONTHS_COPTIC = ["Ⲑⲟⲟⲩⲧ",
                 "Ⲡⲁⲱⲡⲉ",
                 "Ϩⲁⲑⲱⲣ",
                 "Ⲕⲟⲓⲁϩⲕ",
                 "Ⲧⲱⲃⲉ",
                 "Ⲙϣⲓⲣ",
                 "Ⲡⲁⲣⲙϩⲟⲧⲡ",
                 "Ⲡⲁⲣⲙⲟⲩⲧⲉ",
                 "Ⲡⲁϣⲟⲛⲥ",
                 "Ⲡⲁⲱⲛⲉ",
                 "Ⲉⲡⲏⲡ",
                 "Ⲙⲉⲥⲱⲣⲏ",
                 "Ⲉⲡⲁⲅⲟⲙⲉⲛⲁⲓ"]

MONTHS_TRANSLIT = ["Thout",
                    "Paopi",
                    "Hathor",
                    "Koiak",
                    "Tobi",
                    "Meshir",
                    "Paremhat",
                    "Parmouti",
                    "Pashons",
                    "Paoni",
                    "Epip",
                    "Mesori",
                    "Pi Kogi Enavot"]

# Sources: RDM p. 75.
# Wolfgang Kosack. Lehrbuch des Koptischen. Akademische Druck- u. Verlagsanstalt, 1974. ISBN  978-3-201-00889-1.
DAYS_OF_WEEK_COPTIC = ["Ⲧⲕⲩⲣⲓⲁⲕⲏ",
                      "Ⲡⲉⲥⲛⲁⲩ",
                      "Ⲡϣⲟⲙⲏ̄ⲧ",
                      "Ⲡⲉϥⲧⲟⲟⲩ",
                      "Ⲡϯⲟⲩ",
                      "Ⲡⲥⲟⲟⲩ",
                      "Ⲡⲥⲁⲃⲃⲁⲧⲟⲛ"]

DAYS_OF_WEEK_TRANSLIT = ["Tkyriakê", "Pesnau", "Pshoment", "Peftoou", "Ptiou", "Psoou", "Psabbaton"]
# endregion

@dataclass
class CopticDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Coptic calendar.
    """
    # region Data Fields
    year: int
    month: int
    day: int
    # endregion

    EPOCH = tools.COPTIC_EPOCH

    def __init__(self, year: int = 0, month: int = 0, day: int = 0):
        """
        Initialization
        :param year: Coptic year.
        :param month: Coptic month
        :param day: Coptic day.
        """
        self.year = year
        self.month = month
        self.day = day

    def to_moment(self) -> float:
        """
        Converts the Coptic date to an RD time moment.
        :return: The RD time moment.
        """
        result = CopticDate.EPOCH - 1 + 365 * (self.year - 1) + math.floor(self.year / 4) + 30 * (self.month - 1) + self.day
        return result

    def from_moment(self, t: float):
        """
        Converts an RD time moment to a Coptic date.
        :param t: The RD time moment to convert.
        :return: None. The instance of CopticDate will be generated instead.
        """
        self.year = math.floor((4 * (t - CopticDate.EPOCH) + 1463) / 1461)
        self.month = int(math.floor((t - CopticDate(self.year, 1, 1).to_moment()) / 30)) + 1
        self.day = int(t + 1 - CopticDate(self.year, self.month, 1).to_moment())
