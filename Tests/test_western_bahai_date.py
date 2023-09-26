import unittest

from calendars.western_bahai_date import WesternBahaiDate


class TestWesternBahaiDate(unittest.TestCase):
    def test_western_bahai_date_to_moment(self):
        data = self.prepare_data()

        for rd in data:
            t = data[rd].to_moment()

            self.assertEqual(rd, t)
            print(rd, t)

    def test_moment_to_western_bahai_date(self):
        data = self.prepare_data()

        for rd in data:
            wbd = WesternBahaiDate()
            wbd.from_moment(rd)

            self.assertEqual(wbd.major, data[rd].major)
            self.assertEqual(wbd.cycle, data[rd].cycle)
            self.assertEqual(wbd.year, data[rd].year)
            self.assertEqual(wbd.month, data[rd].month)
            self.assertEqual(wbd.day, data[rd].day)

    def prepare_data(self):
        file_name = "../data/western_bahai.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            major = int(cells[1])
            cycle = int(cells[2])
            year = int(cells[3])
            month = int(cells[4])
            day = int(cells[5])

            wesbah = WesternBahaiDate(major, cycle, year, month, day)
            data[rd] = wesbah

        return data
