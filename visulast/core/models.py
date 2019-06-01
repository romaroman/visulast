from visulast.core import scrappers
from visulast.utils.helpers import get_logger
from visulast.config import Configuration
import visulast.core.vars as vars

logger = get_logger(__name__)


class UserModel:
    def __init__(self, name, telegram_id):
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

    def get_classic_eight_albums(self, period):
        return self.lastfm_user.get_top_albums(period, 8)

    def get_classic_eight_artists(self, period):
        return self.lastfm_user.get_top_artists(period, 8)

    def get_top_artists(self, limit=10):
        return self.lastfm_user.get_top_artists(vars.PERIOD_OVERALL, limit)

    def get_top_albums(self, limit=10):
        return self.lastfm_user.get_top_albums(vars.PERIOD_OVERALL, limit)

    def get_top_tracks(self, limit=10):
        return self.lastfm_user.get_top_tracks(vars.PERIOD_OVERALL, limit)

    def get_top_tags(self, limit=5):
        artists = self.get_top_artists(limit=5)
        tags = {}
        for artist in artists:
            artist_tags = artist.item.get_top_tags(limit=5)
            for artist_tag in artist_tags:
                tag_name = artist_tag.item.name.lower()
                if tag_name in tags.keys():
                    tags[tag_name] += 1
                else:
                    tags[tag_name] = 1

        return [(k, tags[k]) for k in sorted(tags, key=tags.get, reverse=True)][:limit]

    def get_friends_playcounts(self, limit=10):
        friends = scrappers.FriendsScrapper.get_friends_by_username(self.username)[:limit]
        data = [(friend, Configuration().lastfm_network.get_user(friend).get_playcount()) for friend in friends]
        return sorted(data, key=lambda x: x[1], reverse=True)

    def get_top_albums_data(self, limit=10):
        return [(album.item.title, album.weight) for album in self.lastfm_user.get_top_albums(limit=limit)][::-1]

    def get_top_artists_data(self, limit=10):
        return [(artist.item.name, artist.weight) for artist in self.lastfm_user.get_top_artists(limit=limit)][::-1]


if __name__ == '__main__':
    UserModel('niedego', 'asda').get_top_albums_data()