import unittest

from calendars.coptic_date import CopticDate


class TestCopticDate(unittest.TestCase):
    """
    Tests for Coptic dates.
    """
    def test_coptic_date_to_moment(self):
        data = self.prepare_data()

        for rd in data:
            t = data[rd].to_moment()

            self.assertEqual(rd, t)
            print(rd, t)


    def test_moment_to_coptic_date(self):
        data = self.prepare_data()

        for rd in data:
            greg = CopticDate()
            greg.from_moment(rd)

            self.assertEqual(greg.year, data[rd].year)
            self.assertEqual(greg.month, data[rd].month)
            self.assertEqual(greg.day, data[rd].day)

    def prepare_data(self):
        file_name = "../data/coptic.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            year = int(cells[1])
            month = int(cells[2])
            day = int(cells[3])

            coptic = CopticDate(year, month, day)
            data[rd] = coptic

        return data
