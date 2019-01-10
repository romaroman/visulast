import unittest

from visulast.scrappers import CountryOfArtist


class TestArtistScrappers(unittest.TestCase):

    def test_single_artist(self):
        self.assertEqual('Poland', CountryOfArtist.get_one_by_string('Drake'))
        self.assertEqual('United States of America', CountryOfArtist.get_one_by_string('Bowery Electric'))
        self.assertEqual('United Kingdom', CountryOfArtist.get_one_by_string('Joy Division'))


if __name__ == '__main__':
    unittest.main()
