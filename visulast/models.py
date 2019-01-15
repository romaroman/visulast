import scrappers as scrap


class _Model:
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def get_sql_data(self):
        pass


class UserModel(_Model):
    def __init__(self, name, chat_id, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.username = name
        self.telegram_id = chat_id

    def get_artists_amount_per_country(self):
        pass

    def get_scrobbles_per_country(self):
        return

    pass


class AristModel(_Model):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def