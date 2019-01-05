import unittest

from visulast.scrappers import ArtistCountryScrapper


class TestArtistScrappers(unittest.TestCase):

    def test_single_artist(self):
        self.assertEqual('Poland', ArtistCountryScrapper.get_one_by_string('Drake'))
        self.assertEqual('United States of America', ArtistCountryScrapper.get_one_by_string('Bowery Electric'))
        self.assertEqual('United Kingdom', ArtistCountryScrapper.get_one_by_string('Joy Division'))


if __name__ == '__main__':
    unittest.main()
