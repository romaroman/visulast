import unittest

from visulast.core.scrappers import CountryOfArtistScrapper


class TestArtistScrappers(unittest.TestCase):

    def test_single_artist(self):
        self.assertEqual('Poland', CountryOfArtistScrapper.get_one_by_string('Drake'))
        self.assertEqual('United States of America', CountryOfArtistScrapper.get_one_by_string('Bowery Electric'))
        self.assertEqual('United Kingdom', CountryOfArtistScrapper.get_one_by_string('Joy Division'))

    def test_user(self):
        #self.assertEq
        pass


if __name__ == '__main__':
    unittest.main()
