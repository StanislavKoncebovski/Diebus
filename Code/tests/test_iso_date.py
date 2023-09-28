import unittest

from calendars.iso_date import IsoDate


class TestIsoDate(unittest.TestCase):
    def test_iso_date_to_moment(self):
        data = self.prepare_data()

        for rd in data:
            t = data[rd].to_moment()

            self.assertEqual(rd, t)
            print(rd, t)

    def test_moment_to_iso_date(self):
        data = self.prepare_data()

        for rd in data:
            iso = IsoDate()
            iso.from_moment(rd)

            self.assertEqual(iso.year, data[rd].year)
            self.assertEqual(iso.week, data[rd].week)
            self.assertEqual(iso.day, data[rd].day)

    def prepare_data(self):
        """
        Test data correspond to Sample Data in Appendix C of RDM (p. 396-400).
        :return: Dictionary with the sample RD values as the keys and corresponding instances of IsoDate as values.
        """
        file_name = "../data/iso.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            year = int(cells[1])
            week = int(cells[2])
            day = int(cells[3])

            iso = IsoDate(year, week, day)
            data[rd] = iso

        return data
