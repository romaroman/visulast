import unittest
from visulast.core import controllers, models


class TestUserController(unittest.TestCase):

    def test_artists_playcount_world_map(self):
        controller = controllers.UserController(models.UserModel('niedego'))
        self.assertIsNotNone(controller.artists_playcount_world_map(limit=1))

    def test_top_artists_bar_chart(self):
        controller = controllers.UserController(models.UserModel('niedego'))
        self.assertIsNotNone(controller.top_artists_bar_chart(limit=1))

    def test_artists_classic_eight(self):
        controller = controllers.UserController(models.UserModel('niedego'))
        self.assertIsNotNone(controller.artists_classic_eight())

    def test_albums_bar_chart(self):
        controller = controllers.UserController(models.UserModel('niedego'))
        self.assertIsNotNone(controller.albums_bar_chart(limit=1))

    def test_albums_pie_chart(self):
        controller = controllers.UserController(models.UserModel('niedego'))
        self.assertIsNotNone(controller.albums_pie_chart(limit=1))

    def test_process(self):
        controller = controllers.UserController(models.UserModel('niedego'))
        self.assertIsNone(controller.process(subject='Sometinhg', representation='Graph'))


if __name__ == '__main__':
    unittest.main()
