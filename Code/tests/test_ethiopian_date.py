import unittest

from calendars.ethiopic_date import EthiopicDate


class TestEthiopicDate(unittest.TestCase):
    """
    Tests for Coptic dates.
    """

    def test_ethiopic_date_to_moment(self):
        data = self.prepare_data()

        for rd in data:
            t = data[rd].to_moment()

            self.assertEqual(rd, t)
            print(rd, t)

    def test_moment_to_ethiopic_date(self):
        data = self.prepare_data()

        for rd in data:
            greg = EthiopicDate()
            greg.from_moment(rd)

            self.assertEqual(greg.year, data[rd].year)
            self.assertEqual(greg.month, data[rd].month)
            self.assertEqual(greg.day, data[rd].day)

    def prepare_data(self):
        """
        Test data correspond to Sample Data in Appendix C of RDM (p. 396-400).
        :return: Dictionary with the sample RD values as the keys and corresponding instances of EthiopicDate as values.
        """
        file_name = "../data/ethiopic.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            year = int(cells[1])
            month = int(cells[2])
            day = int(cells[3])

            ethiopic = EthiopicDate(year, month, day)
            data[rd] = ethiopic

        return data
