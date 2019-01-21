import scrappers
from logger import get_logger
import os
import pandas as pd


logger = get_logger(os.path.basename(__file__))


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
        self.lastfm_user = scrappers.lastfm_client.get_user(self.username)
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
            logger.info("{}\t{}\t".format(i.item.name, country))
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

    pass


class AristModel(_Model):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def smthin(self):
        pass
