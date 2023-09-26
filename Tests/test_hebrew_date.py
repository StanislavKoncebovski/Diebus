import unittest

from calendars.hebrew_date import HebrewDate


class TestHebrewDate(unittest.TestCase):
    """
    Tests for Hebrew dates.
    TODO: test here! 2023-09-19 21:15
    """

    def test_hebrew_date_to_moment(self):
        data = self.prepare_data()

        for rd in data:
            t = data[rd].to_moment()

            self.assertEqual(rd, t)
            print(rd, t)

    def test_moment_to_hebrew_date(self):
        data = self.prepare_data()

        for rd in data:
            hebrew = HebrewDate()
            hebrew.from_moment(rd)

            self.assertEqual(hebrew.year, data[rd].year)
            self.assertEqual(hebrew.month, data[rd].month)
            self.assertEqual(hebrew.day, data[rd].day)

    def prepare_data(self):
        file_name = "../data/hebrew.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            year = int(cells[1])
            month = int(cells[2])
            day = int(cells[3])

            hebrew = HebrewDate(year, month, day)
            data[rd] = hebrew

        return data
