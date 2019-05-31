from visulast.core import scrappers
from visulast.utils.helpers import get_logger
from visulast.config import Configuration


logger = get_logger(__name__)


class _Model:
    def __init__(self):
        super(_Model, self).__init__()

    def get_sql_data(self):
        pass


class UserModel(_Model):
    def __init__(self, name, telegram_id):
        super(UserModel, self).__init__()
        self.username = name
        self.telegram_id = telegram_id
        self.lastfm_user = Configuration().lastfm_network.get_user(self.username)
        self.library = self.lastfm_user.get_library()

    def get_for_all_countries(self, what='s', limit=5):
        """
        :param what: type of gathering data: s for scrobbles, else - artists amount (char/string, default 's')
        :param limit: amount of top artists                     (integer, default 5)
        :return: countries: {'Russia': 120, 'Germany': 44, ...} (dictionary)
        """
        countries = {}
        for i in self.library.get_artists(limit=limit):
            country = scrappers.CountryOfArtistScrapper.get_one(i.item)
            v = 1
            if what == 's':
                v = i.playcount
            if country:
                if country in countries.keys():
                    countries[country] += v
                else:
                    countries[country] = v
        return countries

    def get_scrobbles_per_country(self):
        return

    def get_classic_eight_albums(self, period):
        return self.lastfm_user.get_top_albums(period, 8)

    def get_classic_eight_artists(self, period):
        return self.lastfm_user.get_top_artists(period, 8)


class AristModel(_Model):

    def smthin(self):
        pass
