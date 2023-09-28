import unittest

from calendars.mayan_long_count import MayanLongCountDate


class TestMayanLongCountDate(unittest.TestCase):
    """
    Tests for MayanLongCount dates.
    """
    def test_mayan_long_count_date_to_moment(self):
        data = self.prepare_data()

        for rd in data:
            t = data[rd].to_moment()

            self.assertEqual(rd, t)
            print(rd, t)

    def test_moment_to_mayan_long_count_date(self):
        data = self.prepare_data()

        for rd in data:
            mayan = MayanLongCountDate()
            mayan.from_moment(rd)

            self.assertEqual(mayan.baktun, data[rd].baktun)
            self.assertEqual(mayan.katun, data[rd].katun)
            self.assertEqual(mayan.tun, data[rd].tun)
            self.assertEqual(mayan.uinal, data[rd].uinal)
            self.assertEqual(mayan.kin, data[rd].kin)

    def prepare_data(self):
        """
        Test data correspond to Sample Data in Appendix C of RDM (p. 396-400).
        :return: Dictionary with the sample RD values as the keys and corresponding instances of MayanLongCountDate as values.
        """
        file_name = "../data/mayan_long_count.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            baktun = int(cells[1])
            katun = int(cells[2])
            tun = int(cells[3])
            uinal = int(cells[4])
            kin = int(cells[5])

            mayan = MayanLongCountDate(baktun, katun, tun, uinal, kin)
            data[rd] = mayan

        return data
