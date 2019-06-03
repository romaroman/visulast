import unittest
from visulast.core import models


class TestUserModel(unittest.TestCase):

    def test_get_friends(self):
        model = models.UserModel('niedego')
        self.assertIsNotNone(model.get_friends(limit=1))

    def test_get_top_tracks(self):
        model = models.UserModel('niedego')
        self.assertIsNotNone(model.get_top_tracks(limit=1))

    def test_get_artists(self):
        model = models.UserModel('niedego')
        self.assertIsNotNone(model.get_artists(limit=1))

    def test_get_albums(self):
        model = models.UserModel('niedego')
        self.assertIsNotNone(model.get_albums(limit=1))

    def test_get_top_artists_data(self):
        model = models.UserModel('niedego')
        self.assertIsNotNone(model.get_top_artists_data(limit=1))

    def test_get_top_albums(self):
        model = models.UserModel('niedego')
        self.assertIsNotNone(model.get_top_albums(limit=1))

    def test_get_for_all_countries(self):
        model = models.UserModel('niedego')
        self.assertIsNotNone(model.get_for_all_countries(limit=1))

    def test_get_tags_data(self):
        model = models.UserModel('niedego')
        self.assertIsNotNone(model.get_tags_data(limit=1))


if __name__ == '__main__':
    unittest.main()
