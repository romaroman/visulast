from visulast.core import views, models
from visulast.utils.helpers import get_logger
import visulast.core.vars as vars


logger = get_logger(__name__)


class UserController:
    def __init__(self, username, telegram_id):
        self.model = models.UserModel(username, telegram_id)
        self.view = views.UserView(username)

    def scrobbles_world_map(self, limit=10):
        return self.view.draw_world_map_matplotlib(self.model.get_for_all_countries(what='s', limit=limit))

    def artist_amount_world_map(self, limit=10):
        return self.view.draw_world_map_matplotlib(self.model.get_for_all_countries(what='a', limit=limit))

    def classic_eight_artists(self, period=vars.PERIOD_OVERALL):
        return self.view.draw_classic_eight(self.model.get_classic_eight_artists(period))

    def classic_eight_albums(self, period=vars.PERIOD_OVERALL):
        return self.view.draw_classic_eight(self.model.get_classic_eight_albums(period))

    def tags_piechart(self, limit=10, title='The most heavy tags'):
        return self.view.draw_tags_piechart(self.model.get_top_tags(limit=limit), title=title)

    def barchart_top_albums(self, limit=10, title='Bar chart weight representation of top albums'):
        return self.view.draw_horizontal_barchart(self.model.get_top_albums_data(limit=limit), title=title)

    def barchart_top_artists(self, limit=10, title='Bar chart weight representation of top artists'):
        return self.view.draw_horizontal_barchart(self.model.get_top_artists_data(limit=limit), title=title)

    def barchart_friends(self, limit=10, title='Bar chart weight representation of top friends'):
        return self.view.draw_horizontal_barchart(self.model.get_friends_playcounts(limit=limit), title=title)
