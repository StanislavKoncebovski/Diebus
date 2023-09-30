import math
import unittest

from calendars.gregorian_date import GregorianDate
from times import equation_of_time


class TestEquationOfTime(unittest.TestCase):
    """
    Tests for Equation of time.
    """

    def test_equation_of_time(self):
        """
        Test data obtained by running Java code of calendrica for days of 2023.
        """
        file_name = "../data/equation_of_time.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')

            year = int(cells[0])
            month = int(cells[1])
            day = int(cells[2])

            gregorian = GregorianDate(year, month, day)

            t = gregorian.to_moment()

            et = equation_of_time(t) * 24 * 60

            et_expected = float(cells[3])

            error = math.fabs(et - et_expected) * 60
            print(f"et = {et}\t expected = {et_expected}, \terror={error} s")
