import unittest
from visulast.core import tools


class TestTools(unittest.TestCase):

    def test_does_user_exist(self):
        self.assertTrue(tools.does_user_exist('niedego'))

    def test_does_album_exist(self):
        self.assertTrue(tools.does_album_exist(artist_name='DJ Shadow', title='Endtroducing.....'))

    def test_does_tag_exist(self):
        self.assertTrue(tools.does_tag_exist('hip-hop'))

    def test_does_track_exist(self):
        self.assertTrue(tools.does_track_exist(artist_name='Portishead', track_title='Roads'))

    def test_does_artist_exist(self):
        self.assertTrue(tools.does_artist_exist('Massive Attack'))


if __name__ == '__main__':
    unittest.main()
