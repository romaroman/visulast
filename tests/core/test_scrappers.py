import unittest
from visulast.core import scrappers
from visulast.config import Configuration


class TestScrappers(unittest.TestCase):

    def test_country_scrapper_get_from_lastfm_summary(self):
        artist = Configuration().lastfm_network.get_artist("DJ Shadow")
        self.assertIsNotNone(scrappers.CountryScrapper.get_from_lastfm_summary(artist))

    def test_country_scrapper_get_from_wiki(self):
        artist = "DJ Shadow"
        self.assertIsNotNone(scrappers.CountryScrapper.get_from_wiki(artist))

    def test_country_scrapper_get_from_musicbrainz(self):
        artist = Configuration().lastfm_network.get_artist("DJ Shadow")
        self.assertIsNotNone(scrappers.CountryScrapper.get_from_musicbrainz(artist))

    def test_country_scrapper_normalize_with_gmaps(self):
        self.assertIsNone(scrappers.CountryScrapper.normalize_with_gmaps("United States"))

    def test_country_scrapper_normalize_with_dictionary(self):
        self.assertIsNotNone(scrappers.CountryScrapper.normalize_with_dictionary("US"))

    def test_friends_scrapper_get_friends_by_username(self):
        self.assertIsNotNone(scrappers.FriendsScrapper.get_friends_by_username('niedego'))

    def test_image_scrapper_get_image_by_entity(self):
        artist = Configuration().lastfm_network.get_top_artists(limit=1)[0]
        self.assertIsNotNone(scrappers.ImageScrapper.get_image_by_entity(artist))

    # def test_(self):
    #     self.assertIsNotNone(scrappers.)


if __name__ == '__main__':
    unittest.main()
