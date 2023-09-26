import unittest

from calendars.julian_date import JulianDate


class TestJulianDate(unittest.TestCase):
    """
    Tests for Julian dates.
    """

    def test_julian_date_to_moment(self):
        data = self.prepare_data()

        for rd in data:
            t = data[rd].to_moment()

            self.assertEqual(rd, t)
            print(rd, t)


    def test_moment_to_julian_date(self):
        data = self.prepare_data()

        for rd in data:
            greg = JulianDate()
            greg.from_moment(rd)

            self.assertEqual(greg.year, data[rd].year)
            self.assertEqual(greg.month, data[rd].month)
            self.assertEqual(greg.day, data[rd].day)

    def prepare_data(self):
        file_name = "../data/julian.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            year = int(cells[1])
            month = int(cells[2])
            day = int(cells[3])

            jul = JulianDate(year, month, day)
            data[rd] = jul

        return data
