from visulast.core import scrappers
from visulast.utils.helpers import get_logger
from visulast.config import Configuration
from visulast.core import vars

logger = get_logger(__name__)


class UserModel:
    def __init__(self, lastfm_name):
        pass

    def __new__(cls, lastfm_name, *args, **kwargs):
        instance = super(UserModel, cls).__new__(cls)
        instance.__init__(lastfm_name)
        entity = Configuration().lastfm_network.get_user(username=lastfm_name)
        if entity.get_playcount():
            instance.entity = entity
            return instance
        else:
            return None

    def get_for_all_countries(self, what='s', limit=5):
        """
        :param what: type of gathering data: s for scrobbles, else - artists amount (char/string, default 's')
        :param limit: amount of top artists                     (integer, default 5)
        :return: countries: {'Russia': 120, 'Germany': 44, ...} (dictionary)
        """
        countries = {}
        for i in self.entity.get_top_artists(limit=limit):
            country = scrappers.CountryOfArtistScrapper.get_one(i.item)
            v = 1
            if what == 's':
                v = int(i.weight)
            if country:
                if country in countries.keys():
                    countries[country] += v
                else:
                    countries[country] = v
        return countries

    # <editor-fold desc="Artists">
    def get_classic_eight_artists(self, period=vars.PERIOD_OVERALL):
        return self.entity.get_top_artists(period, limit=8)

    def get_top_artists(self, limit=10):
        return self.entity.get_top_artists(vars.PERIOD_OVERALL, limit=limit)

    def get_top_artists_data(self, limit=10):
        return [(artist.item.name, artist.weight) for artist in self.entity.get_top_artists(limit=limit)][::-1]

    def get_artists(self, period=vars.PERIOD_OVERALL, limit=10):
        return self.entity.get_top_artists(period=period, limit=limit)

    def get_artists_data(self, period=vars.PERIOD_OVERALL, limit=10):
        return [(artist.item.name, artist.weight) for artist in self.entity.get_top_artists(period=period, limit=limit)][::-1]
    # </editor-fold>

    # <editor-fold desc="Albums">
    def get_classic_eight_albums(self, period=vars.PERIOD_OVERALL):
        return self.entity.get_top_albums(period=period, limit=8)

    def get_albums(self, period=vars.PERIOD_OVERALL, limit=10):
        return self.entity.get_top_albums(period=period, limit=limit)

    def get_top_albums(self, limit=10):
        return self.entity.get_top_albums(vars.PERIOD_OVERALL, limit=limit)

    def get_top_albums_data(self, limit=10):
        return [(album.item.title, album.weight) for album in self.entity.get_top_albums(limit=limit)][::-1]

    def get_albums_data(self, period=vars.PERIOD_OVERALL, limit=10):
        return [(album.item.title, album.weight) for album in self.entity.get_top_albums(period=period, limit=limit)][::-1]
    # </editor-fold>

    # <editor-fold desc="Tracks">
    def get_top_tracks(self, limit=10):
        return self.entity.get_top_tracks(vars.PERIOD_OVERALL, limit=limit)
    # </editor-fold>

    # <editor-fold desc="Tags">
    def get_tags_data(self, limit=5):
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
    # </editor-fold>

    # <editor-fold desc="Friends">
    def get_friends(self, limit=10):
        return scrappers.FriendsScrapper.get_friends_by_username(self.entity.get_name())[:limit]

    def get_friends_playcount(self, limit=10):
        friends = self.get_friends(limit=limit)
        data = [(friend, Configuration().lastfm_network.get_user(friend).get_playcount()) for friend in friends]
        return sorted(data, key=lambda x: x[1], reverse=True)
    # </editor-fold>

    def get_compatibility_by_friends_and_tags(self, friends_limit=10, tags_limit=10):
        friends = self.get_friends(limit=friends_limit)
        return [(friend, UserModel(friend).get_tags_data(limit=tags_limit)) for friend in friends]


class AlbumModel:
    def __init__(self, artist_name, title):
        pass

    def __new__(cls, artist_name, title, *args, **kwargs):
        instance = super(AlbumModel, cls).__new__(cls)
        instance.__init__(artist_name, title)
        entity = Configuration().lastfm_network.get_album(artist=artist_name, title=title)
        if entity.get_mbid():
            instance.entity = entity
            return instance
        else:
            return None

    def get_tracks_userplaycount(self, username):
        # TODO: realize
        return [(track, track.get_userplaycount(username)) for track in self.entity.get_tracks()]

    def get_tracks(self):
        return self.entity.get_tracks()

    def get_tracks_playcount(self):
        return [(track.get_name(), track.get_playcount()) for track in self.entity.get_tracks()]

    def get_info(self):
        return self.entity.get_wiki_summary()


class ArtistModel:
    def __init__(self, name):
        pass

    def __new__(cls, name, *args, **kwargs):
        instance = super(ArtistModel, cls).__new__(cls)
        instance.__init__(name)
        entity = Configuration().lastfm_network.get_artist(artist_name=name)
        if entity.get_mbid():
            instance.entity = entity
            return instance
        else:
            return None

    def get_albums(self, limit=5):
        return self.entity.get_top_albums(limit=limit)


class TagModel:
    def __init__(self, name):
        pass

    def __new__(cls, name, *args, **kwargs):
        instance = super(TagModel, cls).__new__(cls)
        instance.__init__(name)
        entity = Configuration().lastfm_network.get_tag(name=name)
        if entity.get_mbid():
            instance.entity = entity
            return instance
        else:
            return None


class TrackModel:
    def __init__(self, artist_name, track_title):
        pass

    def __new__(cls, artist_name, track_title, *args, **kwargs):
        instance = super(TrackModel, cls).__new__(cls)
        instance.__init__(artist_name, track_title)
        entity = Configuration().lastfm_network.get_track(artist=artist_name, title=track_title)
        if entity.get_mbid():
            instance.entity = entity
            return instance
        else:
            return None
