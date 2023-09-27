import unittest

from calendars.old_hindu_lunar_date import OldHinduLunarDate


class TestOldHinduLunarDate(unittest.TestCase):
    """
    Tests for Old Hindu Lunar dates.
    """
    def test_old_hindu_lunar_date_to_moment(self):
        data = self.prepare_data()

        for rd in data:
            t = data[rd].to_moment()

            self.assertEqual(rd, t)
            print(rd, t)

    def test_moment_to_old_hindu_lunar_date(self):
        data = self.prepare_data()

        for rd in data:
            hindu = OldHinduLunarDate()
            hindu.from_moment(rd)

            self.assertEqual(hindu.year, data[rd].year)
            self.assertEqual(hindu.month, data[rd].month)
            self.assertEqual(hindu.is_leap_month, data[rd].is_leap_month)
            self.assertEqual(hindu.day, data[rd].day)

    def prepare_data(self):
        file_name = "../data/old_hindu_lunar.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            year = int(cells[1])
            month = int(cells[2])
            is_leap_month = cells[3] != 'f'
            day = int(cells[4])

            hindu = OldHinduLunarDate(year, month, is_leap_month, day)
            data[rd] = hindu

        return data
