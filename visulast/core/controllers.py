from visulast.core import models
from visulast.core.views import GeneralView
from visulast.utils.helpers import get_logger
import visulast.core.vars as vars


logger = get_logger(__name__)


class UserController:
    def __init__(self, model):
        self.model = model

    def scrobbles_world_map(self, limit=10):
        return GeneralView.draw_world_map_matplotlib(self.model.get_for_all_countries(what='s', limit=limit))

    def artist_amount_world_map(self, limit=10):
        return GeneralView.draw_world_map_matplotlib(self.model.get_for_all_countries(what='a', limit=limit))

    def artists_classic_eight(self, period=vars.PERIOD_OVERALL):
        return GeneralView.draw_classic_eight(self.model.get_classic_eight_artists(period))

    def albums_classic_eight(self, period=vars.PERIOD_OVERALL):
        return GeneralView.draw_classic_eight(self.model.get_classic_eight_albums(period))

    def tags_piechart(self, limit=10, title='The most heavy tags'):
        return GeneralView.draw_tags_piechart(self.model.get_top_tags(limit=limit), title=title)

    def top_albums_bar_chart(self, limit=10, title='top albums'):
        return GeneralView.draw_horizontal_barchart(self.model.get_top_albums_data(limit=limit), title=title)

    def top_artists_bar_chart(self, limit=10, title='top artists'):
        return GeneralView.draw_horizontal_barchart(self.model.get_top_artists_data(limit=limit), title=title)

    def friends_bar_chart(self, limit=10, title='top friends'):
        return GeneralView.draw_horizontal_barchart(self.model.get_friends_playcounts(limit=limit), title=title)


class AlbumController:
    def __init__(self, model):
        self.model = model

    def tracks_bar_chart(self, limit=10, title='tracks'):
        return GeneralView.draw_horizontal_barchart(self.model.get_tracks_playcount(), title)


if __name__ == '__main__':
    controller = AlbumController(models.AlbumModel('DJ Shadow', 'Endtroducing.....'))
    image = controller.tracks_bar_chart()
