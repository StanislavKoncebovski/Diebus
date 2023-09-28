import unittest

from calendars.armenian_date import ArmenianDate


class TestArmenianDate(unittest.TestCase):
    """
    Tests for Armenian dates.
    """

    def test_armenian_date_to_moment(self):
        data = self.prepare_data()

        for rd in data:
            t = data[rd].to_moment()

            self.assertEqual(rd, t)
            print(rd, t)

    def test_moment_to_armenian_date(self):
        data = self.prepare_data()

        for rd in data:
            armenian = ArmenianDate()
            armenian.from_moment(rd)

            self.assertEqual(armenian.year, data[rd].year)
            self.assertEqual(armenian.month, data[rd].month)
            self.assertEqual(armenian.day, data[rd].day)

    def prepare_data(self):
        """
        Test data correspond to Sample Data in Appendix C of RDM (p. 396-400).
        :return: Dictionary with the sample RD values as the keys and corresponding instances of ArmenianDate as values.
        """
        file_name = "../data/armenian.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            year = int(cells[1])
            month = int(cells[2])
            day = int(cells[3])

            armenian = ArmenianDate(year, month, day)
            data[rd] = armenian

        return data
