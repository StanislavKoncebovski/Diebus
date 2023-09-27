import unittest

from calendars.old_hindu_solar_date import OldHinduSolarDate


class TestOldHinduSolarDate(unittest.TestCase):
    """
    Tests for Old Hindu Solar dates.
    """
    def test_old_hindu_solar_date_to_moment(self):
        data = self.prepare_data()

        for rd in data:
            t = data[rd].to_moment()

            self.assertEqual(rd, t)
            print(rd, t)

    def test_moment_to_old_hindu_solar_date(self):
        data = self.prepare_data()

        for rd in data:
            hindu = OldHinduSolarDate()
            hindu.from_moment(rd)

            self.assertEqual(hindu.year, data[rd].year)
            self.assertEqual(hindu.month, data[rd].month)
            self.assertEqual(hindu.day, data[rd].day)

    def prepare_data(self):
        file_name = "../data/old_hindu_solar.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            year = int(cells[1])
            month = int(cells[2])
            day = int(cells[3])

            hindu = OldHinduSolarDate(year, month, day)
            data[rd] = hindu

        return data
