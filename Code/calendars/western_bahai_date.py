from calendars.abstract_date import AbstractDate
from calendars.gregorian_date import GregorianDate
from dataclasses import dataclass
import math
import tools

class WesternBahaiDate:
    pass

# region Module functions
def from_bahai_year(bahai_year: int) -> (int, int, int):
    """
    Calculates major, cycle, and year from a "total" Bahai year.
    :param bahai_year: The value of "total" Bahai year.
    :return: Tuple (major, cycle, year_within_cycle)
    """
    major = (bahai_year - 1) // 361 + 1
    cycle_index = bahai_year - (major - 1) * 361  # index of the cycle within the major cycle.
    cycle = (cycle_index - 1) // 19 + 1
    year = cycle_index - (cycle - 1) * 19

    return major, cycle, year


def to_bahai_year(major, cycle, year_within_cycle) -> int:
    """
    Calculates the 'total' Bahai year from major, cycle, and year number within cycle
    :param major: The major value.
    :param cycle: The index value.
    :param year_within_cycle: Number of the year within the cycle.
    :return: The 'total' Bahai year.
    """
    return (major - 1) * 361 + (cycle - 1) * 19 + year_within_cycle

def ayyam_i_ha(gregorian_year: int) -> (int, int):
    """
    Calculates the beginning and the end of Ayyam-i-Ha for a given Gregorian year as the numbers of days in the year
    (1-based).
    :param gregorian_year: The Gregorian year.
    :return: Tuple containing the beginning and the end of Ayyam-i-Ha in the year.
    """
    start = GregorianDate(gregorian_year, 2, 26).day_of_year()
    end = GregorianDate(gregorian_year, 3, 1).day_of_year()

    return start, end

# endregion

# region Names
MONTHS_ARABIC =  ["ايام الهاء", "بهاء", "جلال", "جمال", "عظمة", "نور", "رحمة", "كلمات", "كمال", "اسماء", "عزة",
                  "مشية", "علم", "قدرة", "قول", "مسائل", "شرف", "سلطان", "ملك",  "علاء"]

MONTHS_TRANSLIT = ["Ayyam-i-Ha", "Baha'", "Jalal", "Jamal", "`Azamat", "Nur", "Rahmat", "Kalimat",
                 "Kamal", "Asma'", "`Izzat", "Mashiyyat", "`Ilm", "Qudrat", "Qawl", "Masa'il",
                 "Sharaf", "Sultan", "Mulk", "`Ala'"]

DAYS_OF_WEEK_TRANSLIT = ["Jamal", "Kamal", "Fidal", "`Idal", "Istijlal", "Istiqlal", "Jalal"]
DAYS_OF_WEEK_ARABIC = ["جلال", "جمال", "كمال", "فضال", "عدال", "استجلال", "استقلال"]

YEARS_TRANSLIT = ["Alif", "Bá'", "Ab",  "Dál",  "Báb",	"Váv",	"Abad",	"Jád",	"Bahá",	"Hubb",	"Bahháj",
                  "Javáb", "Ahad", "Vahháb", "Vidád", "Badí'", "Bahí", "Abhá", "Váhid"]

YEARS_ARABIC = ["أ", "ب", "أب", "د", "باب", "و", "أبد", "جاد", "بهاء", "حب", "بهاج", "جواب", "احد", "وﻫﺎب",
                    "وداد", "بدیع", "بهي", "ابهى", "واحد"]
# endregion

@dataclass
class WesternBahaiDate(AbstractDate):
    """
    Implements conversion to and from RD time moment for Western (historical) Bahai calendar.
    """

    # region Data Fields
    major: int
    cycle: int
    year: int
    month: int
    day: int
    # endregion

    # BAHAI_EPOCH = 673222.0
    MARCH = 3

    # region Initialization
    def __init__(self, major: int = 0, cycle: int = 0, year: int = 0, month: int = 0, day: int = 0):
        """
        Creates an instance of WesternBahaiDate from constituent values.
        :param major:   The number of the 361-year major cycle (Kull-i-Shay) [RDM 15.2, p. 231]
        :param cycle:   The number of the 19-year cycle (Vahid) [RDM 15.2, p. 230]
        :param year:    The number of the year within the Vahid cycle (1 = Alif, ..., 19 = Vahid).
        :param month:   The number of the month in the year (1 = Bahá, ..., 19 = Alá)
        :param day:     The number of the day in the month.
        """
        self.major = major
        self.cycle = cycle
        self.year = year
        self.month = month
        self.day = day

    # endregion

    # region AbstractDate
    def to_moment(self) -> float:
        """
        Converts the Western Bahai date to the RD time moment.
        :return: The RD time moment.
        """
        gregorian_date_of_bahai_epoch = GregorianDate()
        gregorian_date_of_bahai_epoch.from_moment(tools.WESTERN_BAHAI_EPOCH)
        gregorian_year_of_bahai_epoch = gregorian_date_of_bahai_epoch.year

        # RDM (15.3): g-year
        gregorian_year = gregorian_year_of_bahai_epoch + 361 * (self.major - 1) + 19 * (self.cycle - 1) + self.year - 1
        t = GregorianDate(gregorian_year, WesternBahaiDate.MARCH, 20).to_moment()

        if self.month == 0:  # Ayyám-i-Há
            t += 342
        elif self.month == 19:
            if tools.is_gregorian_leap_year(gregorian_year + 1):
                t += 347
            else:
                t += 346
        else:
            t += 19 * (self.month - 1)

        t += self.day

        return t

    def from_moment(self, t: float) -> None:
        """
        Converts an RD time moment to an instance of WesternBahaiDate.
        :param t: The RD time moment to convert.
        :return: None. The instance of WesternBahaiDate will be generated instead.
        """
        gregorian_date = GregorianDate()
        gregorian_date.from_moment(t)
        gregorian_year = gregorian_date.year

        start_gregorian_date = GregorianDate()
        start_gregorian_date.from_moment(tools.WESTERN_BAHAI_EPOCH)
        start_year = start_gregorian_date.year

        years = gregorian_year - start_year
        if t <= GregorianDate(gregorian_year, WesternBahaiDate.MARCH, 20).to_moment():
            years -= 1

        self.major = int(math.floor(years / 361) + 1)
        self.cycle = int(math.floor(years % 361 / 19) + 1)
        self.year = years % 19 + 1

        # TODO: work here. to_moment is possibly wrong; for 1996-02-12 it gives days = 310 whereas it must be more.
        days = t - WesternBahaiDate(self.major, self.cycle, self.year, 1, 1).to_moment()

        start_ayyam_i_ha = WesternBahaiDate(self.major, self.cycle, self.year, 0, 1).to_moment()
        end_ayyam_i_ha = start_ayyam_i_ha + 4
        if tools.is_gregorian_leap_year(gregorian_year):
            end_ayyam_i_ha += 1

        if t >= WesternBahaiDate(self.major, self.cycle, self.year, 19, 1).to_moment():
            self.month = 19
        elif start_ayyam_i_ha < t <= end_ayyam_i_ha:
            self.month = 0
        else:
            self.month = days // 19 + 1

        self.day = int(t + 1 - WesternBahaiDate(self.major, self.cycle, self.year, self.month, 1).to_moment())

    # endregion

    @property
    def bahai_year(self):
        """
        'Total' Bahai year, as is convenient in practice.
        :return:
        """
        return to_bahai_year(self.major, self.cycle, self.year)

    # region String representation
    def to_string(self, format: str = None) -> str:
        """
        Formatting options (format is case-sensitive):
        "ymd": (Bahá'í) 'year-month-day' (152-18-19 BE)

        With English names of months and cycles.
            "yMd": (Bahá'í) 'year-month name-day' (152 BE, Mulk 19)
            "dMy": 'day-month name-year' (19 Mulk 152 BE)
            "dmymj": 'day-month-year-major-cycle' (19 Mulk of year 19, 8-th Váhid of the 1st Kull-u-Shai)
        Support of Arabic names is postponed until a future version,
        which should generate valid Arabic phrases instead of simple replacing the English names with the Arabic ones.
        """
        month_names = MONTHS_TRANSLIT

        match(format):
            case "ymd":
                return f"{self.bahai_year}-{self.month}-{self.day} BE"
            case "dmy":
                return f"{self.day} {self.month} {self.bahai_year} BE"

            case "ymd":
                return f"{self.bahai_year} {month_names[self.month - 1]} {self.day} BE"
            case "yMd":
                return f"{self.bahai_year}, {self.day} {month_names[self.month - 1]}  BE"
            case "dMy":
                return f"{self.day} {month_names[self.month - 1]} {self.bahai_year} BE"

            case "dmymj":
                return self._to_dmymj()

            # case "dmymjA":
            #     return self._to_dmymj()
            case _ :
                return super().to_string()
    # endregion

    # region Protected Auxiliary
    def _to_dmymj(self) -> str:
        """
        Formats a Bahai date in the dmyml format.
        '19 Mulk of year 19, 8-th Váhid of the 1st Kull-u-Shai'
        """

        month_names = MONTHS_TRANSLIT

        result = f"{self.day} {month_names[self.month - 1]} of year {self.year}, {self.cycle}"

        cycle_suffix = tools.ordinal_suffix(self.cycle)
        major_suffix = tools.ordinal_suffix(self.major)

        result += f"{cycle_suffix} Váhid of the {self.major}{major_suffix} Kull-u-Shai"

        return result
    # endregion

