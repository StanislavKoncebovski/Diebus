import unittest

from calendars.arithmetic_persian import ArithmeticPersianDate


class TestArithmeticPersianDate(unittest.TestCase):
    """
    Tests for Arithmetic Persian dates.
    """
    def test_arithmetic_persian_date_to_moment(self):
        data = self.prepare_data()

        for rd in data:
            t = data[rd].to_moment()

            self.assertEqual(rd, t)
            print(rd, t)

    def test_moment_to_arithmetic_persian_date(self):
        data = self.prepare_data()

        for rd in data:
            persian = ArithmeticPersianDate()
            persian.from_moment(rd)

            # print(persian, data[rd])
            self.assertEqual(persian.year, data[rd].year)
            self.assertEqual(persian.month, data[rd].month)
            self.assertEqual(persian.day, data[rd].day)

    def prepare_data(self):
        """
        Test data correspond to Sample Data in Appendix C of RDM (p. 396-400).
        :return: Dictionary with the sample RD values as the keys and corresponding instances of ArithmeticPersianDate as values.
        """
        file_name = "../data/arithmetic_persian.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            year = int(cells[1])
            month = int(cells[2])
            day = int(cells[3])

            persian = ArithmeticPersianDate(year, month, day)
            data[rd] = persian

        return data
