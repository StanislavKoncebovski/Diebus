import unittest

from calendars.islamic_date import IslamicDate


class TestCopticDate(unittest.TestCase):
    """
    Tests for Islamic dates.
    """
    def test_islamic_date_to_moment(self):
        data = self.prepare_data()

        for rd in data:
            t = data[rd].to_moment()

            self.assertEqual(rd, t)
            print(rd, t)

    def test_moment_to_islamic_date(self):
        data = self.prepare_data()

        for rd in data:
            islamic = IslamicDate()
            islamic.from_moment(rd)

            self.assertEqual(islamic.year, data[rd].year)
            self.assertEqual(islamic.month, data[rd].month)
            self.assertEqual(islamic.day, data[rd].day)

    def prepare_data(self):
        """
        Test data correspond to Sample Data in Appendix C of RDM (p. 396-400).
        :return: Dictionary with the sample RD values as the keys and corresponding instances of IslamicDate as values.
        """
        file_name = "../data/islamic.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            year = int(cells[1])
            month = int(cells[2])
            day = int(cells[3])

            islamic = IslamicDate(year, month, day)
            data[rd] = islamic

        return data
