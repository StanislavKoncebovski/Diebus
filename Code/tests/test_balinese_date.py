import unittest

from calendars.balinese_date import BalineseDate


class TestBalineseDate(unittest.TestCase):
    """
    Tests for Balinese dates.
    """

    def test_moment_to_balinese_date(self):
        data = self.prepare_data()

        for rd in data:
            print(rd)
            balinese = BalineseDate()
            balinese.from_moment(rd)

            self.assertEqual(balinese.luang, data[rd].luang)
            self.assertEqual(balinese.dwiwara, data[rd].dwiwara)
            self.assertEqual(balinese.triwara, data[rd].triwara)
            self.assertEqual(balinese.caturwara, data[rd].caturwara)
            self.assertEqual(balinese.pancawara, data[rd].pancawara)
            self.assertEqual(balinese.sadwara, data[rd].sadwara)
            self.assertEqual(balinese.saptawara, data[rd].saptawara)
            self.assertEqual(balinese.asatawara, data[rd].asatawara)
            self.assertEqual(balinese.sangawara, data[rd].sangawara)
            self.assertEqual(balinese.dasawara, data[rd].dasawara)


    def prepare_data(self):
        """
        Test data correspond to Sample Data in Appendix C of RDM (p. 396-400).
        :return: Dictionary with the sample RD values as the keys and corresponding instances of BalineseDate as values.
        """
        file_name = "../data/balinese.csv"
        with open(file_name, "r") as file:
            lines = file.read().split()

        data = {}
        for line in lines[1:]:
            cells = line.split(',')
            rd = int(cells[0])
            luang = cells[1] != 'f'
            dwiwara = int(cells[2])
            triwara = int(cells[3])
            caturwara = int(cells[4])
            pancawara = int(cells[5])
            sadwara  = int(cells[6])
            saptawara = int(cells[7])
            asatawara = int(cells[8])
            sangawara = int(cells[9])
            dasawara = int(cells[10])

            balinese = BalineseDate(luang, dwiwara, triwara, caturwara, pancawara, sadwara, saptawara, asatawara, sangawara, dasawara)
            data[rd] = balinese

        return data
