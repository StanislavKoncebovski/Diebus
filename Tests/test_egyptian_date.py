import unittest

from calendars.egyptian_date import EgyptianDate


class TestEgyptianDate(unittest.TestCase):
    """
    Tests for Egyptian dates.
    """

    def test_egyptian_date_to_moment(self):
        data = self.prepare_data()

        for rd in data:
            t = data[rd].to_moment()

            self.assertEqual(rd, t)
            print(rd, t)

    def test_moment_to_egyptian_date(self):
        data = self.prepare_data()

        for rd in data:
            egyptian = EgyptianDate()
            egyptian.from_moment(rd)

            self.assertEqual(egyptian.year, data[rd].year)
            self.assertEqual(egyptian.month, data[rd].month)
            self.assertEqual(egyptian.day, data[rd].day)

    def prepare_data(self):
        file_name = "../data/egyptian.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            year = int(cells[1])
            month = int(cells[2])
            day = int(cells[3])

            eqyptian = EgyptianDate(year, month, day)
            data[rd] = eqyptian

        return data
