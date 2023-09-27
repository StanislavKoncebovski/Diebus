import unittest

from calendars.mayan_tzolkin_date import MayanTzolkinDate


class TestMayanHaabDate(unittest.TestCase):
    """
    Tests for Mayan Tzolkin dates.
    """

    def test_moment_to_mayan_tzolkin_date(self):
        data = self.prepare_data()

        for rd in data:
            mayan = MayanTzolkinDate()
            mayan.from_moment(rd)

            self.assertEqual(mayan.number, data[rd].number)
            self.assertEqual(mayan.name, data[rd].name)

    def prepare_data(self):
        file_name = "../data/mayan_tzolkin.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            number = int(cells[1])
            name = int(cells[2])

            mayan = MayanTzolkinDate(number, name)
            data[rd] = mayan

        return data
