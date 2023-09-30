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

    def test_gregorian_date_from_day_number(self):
        data = self.prepare_data()

        for rd in data:
            gregorian = data[rd]
            day_number = gregorian.day_of_year()
            gregorian_calculated = GregorianDate.from_day_number(day_number, gregorian.year)

            self.assertEqual(gregorian.year, gregorian_calculated.year)
            self.assertEqual(gregorian.month, gregorian_calculated.month)
            self.assertEqual(gregorian.day, gregorian_calculated.day)

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
            cells = line.split(',')
            rd = int(cells[0])
            year = int(cells[1])
            month = int(cells[2])
            day = int(cells[3])

            gregorian = GregorianDate(year, month, day)
            data[rd] = gregorian

        return data
