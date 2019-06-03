from visulast.core import models
from visulast.core.views import GeneralView
from visulast.utils.helpers import get_logger
from visulast.core import vars


logger = get_logger(__name__)


class UserController:
    def __init__(self, model):
        self.model = model

    # <editor-fold desc="Artists">
    def artists_playcount_world_map(self, limit=10):
        return GeneralView.draw_world_map(self.model.get_for_all_countries(what='s', limit=limit))

    def artists_amount_world_map(self, limit=10):
        return GeneralView.draw_world_map(self.model.get_for_all_countries(what='a', limit=limit))

    def top_artists_bar_graph(self, limit=10, title='top artists'):
        return GeneralView.draw_horizontal_bar_graph(self.model.get_top_artists_data(limit=limit), title=title)

    def top_artists_pie_graph(self, limit=10, title='top artists'):
        return GeneralView.draw_pie_graph(self.model.get_top_artists_data(limit=limit), title=title)

    def artists_classic_eight(self, period=vars.PERIOD_OVERALL):
        return GeneralView.draw_classic_eight_graph(self.model.get_classic_eight_artists(period))

    def artists_bar_graph(self, period=vars.PERIOD_OVERALL, limit=10, title='artists'):
        return GeneralView.draw_horizontal_bar_graph(self.model.get_artists_data(period=period, limit=limit), title=title)

    def artists_pie_graph(self, period=vars.PERIOD_OVERALL, limit=10, title='artists'):
        return GeneralView.draw_pie_graph(self.model.get_artists_data(period=period, limit=limit), title=title)
    # </editor-fold>

    # <editor-fold desc="Albums">
    def albums_classic_eight(self, period=vars.PERIOD_OVERALL):
        return GeneralView.draw_classic_eight_graph(self.model.get_classic_eight_albums(period))

    def top_albums_bar_graph(self, limit=10, title='top albums'):
        return GeneralView.draw_horizontal_bar_graph(self.model.get_top_albums_data(limit=limit), title=title)

    def albums_bar_graph(self, period=vars.PERIOD_OVERALL, limit=10, title='albums'):
        return GeneralView.draw_horizontal_bar_graph(self.model.get_albums_data(period=period, limit=limit), title=title)

    def albums_pie_graph(self, period=vars.PERIOD_OVERALL, limit=10, title='albums'):
        return GeneralView.draw_pie_graph(self.model.get_albums_data(period=period, limit=limit), title=title)
    # </editor-fold>

    # <editor-fold desc="Tags">
    def tags_pie_graph(self, limit=10, title='The most heavy tags'):
        return GeneralView.draw_pie_graph(self.model.get_tags_data(limit=limit), title=title)
    # </editor-fold>

    # <editor-fold desc="Tracks">
    # </editor-fold>

    # <editor-fold desc="Friends">
    def friends_bar_graph(self, limit=10, title='top friends'):
        return GeneralView.draw_horizontal_bar_graph(self.model.get_friends_playcount(limit=limit), title=title)
    # </editor-fold>

    def process(self, subject, representation, period=vars.PERIOD_OVERALL, amount=10,  *args, **kwargs):
        if subject == 'Artists':
            if representation == 'Bar diagram':
                return self.artists_bar_graph(period=period, limit=amount)
            elif representation == 'Pie diagram':
                return self.artists_pie_graph(period=period, limit=amount)
            elif representation == 'World map':
                return self.artists_playcount_world_map(limit=amount)
            elif representation == 'Stack diagram':
                return
            elif representation == 'Heat map':
                return
            elif representation == 'Classic eight':
                return self.artists_classic_eight(period=period)
            elif representation == '5x5 covers':
                return
            elif representation == '4x4 covers':
                return
        elif subject == 'Albums':
            if representation == 'Bar diagram':
                return self.albums_bar_graph(period=period, limit=amount)
            elif representation == 'Pie diagram':
                return self.albums_pie_graph(period=period, limit=amount)
            elif representation == 'Classic eight':
                return self.albums_classic_eight(period=period)
        elif subject == 'Tracks':
            if representation == 'Bar diagram':
                return self.artists_bar_graph(period=period, limit=amount)
            elif representation == 'Pie diagram':
                return self.artists_pie_graph(period=period, limit=amount)
        elif subject == 'Tags':
            if representation == 'Bar diagram':
                return self.artists_bar_graph(period=period, limit=amount)
            elif representation == 'Pie diagram':
                return self.artists_pie_graph(period=period, limit=amount)
        elif subject == 'Friends':
            if representation == 'Bar diagram':
                return self.artists_bar_graph(period=period, limit=amount)
            elif representation == 'Pie diagram':
                return self.artists_pie_graph(period=period, limit=amount)
        else:
            return None


class AlbumController:
    def __init__(self, model):
        self.model = model

    def tracks_bar_graph(self, title='tracks'):
        return GeneralView.draw_horizontal_bar_graph(self.model.get_tracks_playcount(), title)

    def tracks_pie_graph(self, title='tracks'):
        return GeneralView.draw_pie_graph(self.model.get_tracks_playcount(), title)

    def process(self, subject, representation):
        if subject == 'Tracks':
            if representation == 'Pie graph':
                return self.tracks_bar_graph()
            elif representation == 'Bar graph':
                return self.tracks_pie_graph()