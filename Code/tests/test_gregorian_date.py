import unittest

from calendars.gregorian_date import GregorianDate


class TestGregorianDate(unittest.TestCase):
    """
    Tests for Gregorian dates.
    """

    def test_gregorian_date_to_moment(self):
        data = self.prepare_data()

        for rd in data:
            t = data[rd].to_moment()

            self.assertEqual(rd, t)
            print(rd, t)

    def test_moment_to_gregorian_date(self):
        data = self.prepare_data()

        for rd in data:
            greg = GregorianDate()
            greg.from_moment(rd)

            self.assertEqual(greg.year, data[rd].year)
            self.assertEqual(greg.month, data[rd].month)
            self.assertEqual(greg.day, data[rd].day)

    def prepare_data(self):
        """
        Test data correspond to Sample Data in Appendix C of RDM (p. 396-400).
        :return: Dictionary with the sample RD values as the keys and corresponding instances of GregorianDate as values.
        """
        file_name = "../data/gregorian.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            # 708842,1941,9,29
            cells = line.split(',')
            rd = int(cells[0])
            year = int(cells[1])
            month = int(cells[2])
            day = int(cells[3])

            gregorian = GregorianDate(year, month, day)
            data[rd] = gregorian

        return data
