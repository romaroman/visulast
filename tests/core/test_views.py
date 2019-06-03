import unittest
from visulast.core import views


class TestGeneralView(unittest.TestCase):

    def test_draw_heat_map(self):
        self.assertIsNotNone(views.GeneralView.draw_heat_map([]))

    def test_draw_horizontal_bar_graph(self):
        self.assertIsNotNone(views.GeneralView.draw_horizontal_bar_graph([], 's'))

    def test_draw_pie_graph(self):
        self.assertIsNotNone(views.GeneralView.draw_pie_graph([], ''))

    def test_draw_stacked_bar_graph(self):
        self.assertIsNotNone(views.GeneralView.draw_stacked_bar_graph([], ''))

    def test_draw_classic_eight_graph(self):
        self.assertIsNotNone(views.GeneralView.draw_classic_eight_graph([]))

    def test_draw_world_map(self):
        self.assertIsNotNone(views.GeneralView.draw_world_map({'Russia': 2}))


if __name__ == '__main__':
    unittest.main()
