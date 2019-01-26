from mvc import views, models


class _Controller:
    pass


class UserController(_Controller):
    def __init__(self, username, telegram_id):
        self.usermodel = models.UserModel(username, telegram_id)
        self.userview = views.UserView(username)

    def scrobbles_world_map(self, limit=5):
        return self.userview.draw_world_map(self.usermodel.get_for_all_countries(what='s', limit=limit))

    def artist_amount_world_map(self, limit=5):
        return self.userview.draw_world_map(self.usermodel.get_for_all_countries(what='a', limit=limit))


if __name__ == '__main__':
    controller = UserController('niedego', 12131)
    controller.scrobbles_world_map(2)
