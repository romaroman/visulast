import scrappers


class _Model:
    def __init__(self):
        super(_Model, self).__init__()

    def get_sql_data(self):
        pass


class UserModel(_Model):
    def __init__(self, name, chat_id):
        super(UserModel, self).__init__()
        self.username = name
        self.telegram_id = chat_id

    def get_scrobbles_for_all_countries(self, limit=5):
        """
        :param limit: amount of top artists
        :return: dictionary {'Country blob': #scrobbles, ...}

        CountryOfArtistScrapper.get_all_scrobbles_by_username(name='rocker', lim=25)
        """
        last_user = scrappers.lastfm_client.get_user(self.username)
        library = last_user.get_library()
        countries = {}
        for i in library.get_artists(limit=limit):
            country = scrappers.CountryOfArtistScrapper.get_one(i.item)
            scrobbles = i.playcount
            print("{}\t\t{}\t\t{}".format(i.item.name, country, scrobbles))
            if country:
                if country in countries.keys():
                    countries[country] += scrobbles
                else:
                    countries[country] = scrobbles
        return countries

    def get_artists_amount_per_country(self):

        pass

    def get_scrobbles_per_country(self):
        return

    pass


class AristModel(_Model):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def smthin(self):
        pass