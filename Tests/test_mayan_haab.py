import unittest

from calendars.mayan_haab_date import MayanHaabDate


class TestMayanHaabDate(unittest.TestCase):
    """
    Tests for MayanHaab dates.
    """


    def test_moment_to_mayan_haab_date(self):
        data = self.prepare_data()

        for rd in data:
            mayan = MayanHaabDate()
            mayan.from_moment(rd)

            self.assertEqual(mayan.month, data[rd].month)
            self.assertEqual(mayan.day, data[rd].day)

    def prepare_data(self):
        file_name = "../data/mayan_haab.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            month = int(cells[1])
            day = int(cells[2])

            mayan = MayanHaabDate(month, day)
            data[rd] = mayan

        return data
