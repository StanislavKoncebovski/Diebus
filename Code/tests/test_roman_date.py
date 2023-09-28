import unittest

from calendars.roman_date import RomanDate

class TestRomanDate(unittest.TestCase):
    """
    Tests for Roman dates.
    """

    def test_roman_date_to_moment(self):
        data = self.prepare_data()

        for rd in data:
            t = data[rd].to_moment()

            self.assertEqual(rd, t)
            print(rd, t)

    def test_moment_to_roman_date(self):
        data = self.prepare_data()

        for rd in data:
            roman = RomanDate()
            roman.from_moment(rd)

            print(roman, data[rd])
            self.assertEqual(roman.year, data[rd].year)
            self.assertEqual(roman.month, data[rd].month)
            self.assertEqual(roman.event, data[rd].event)
            self.assertEqual(roman.count, data[rd].count)
            self.assertEqual(roman.is_leap_day, data[rd].is_leap_day)

    def prepare_data(self):
        """
        Test data correspond to Sample Data in Appendix C of RDM (p. 396-400).
        :return: Dictionary with the sample RD values as the keys and corresponding instances of RomanDate as values.
        """
        file_name = "../data/roman.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            year = int(cells[1])
            month = int(cells[2])
            event = int(cells[3])
            count = int(cells[4])
            is_leap_day = cells[5] != 'f'

            roman = RomanDate(year, month, event, count, is_leap_day)
            data[rd] = roman

        return data
