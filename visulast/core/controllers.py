from visulast.core import views, models
from visulast.utils.helpers import get_logger

logger = get_logger(__name__)


class _Controller:
    pass


class UserController(_Controller):
    def __init__(self, username, telegram_id):
        self.model = models.UserModel(username, telegram_id)
        self.view = views.UserView(username)

    def scrobbles_world_map(self, limit=5):
        return self.view.draw_world_map_matplotlib(self.model.get_for_all_countries(what='s', limit=limit))

    def artist_amount_world_map(self, limit=5):
        return self.view.draw_world_map_matplotlib(self.model.get_for_all_countries(what='a', limit=limit))

    def classic_eight_artists(self, period):
        return self.view.draw_classic_eight(self.model.get_classic_eight_artists(period))

    def classic_eight_albums(self, period):
        return self.view.draw_classic_eight(self.model.get_classic_eight_albums(period))


if __name__ == '__main__':
    controller = UserController('niedego', 12131)
    controller.scrobbles_world_map(2)
