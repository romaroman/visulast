import requests as req
from collections import defaultdict

import wikipedia as wiki
import pylast
import googlemaps
import musicbrainzngs
import discogs_client as discogs

from loader import extract_countries
from config import CONFIGURATION


class Scrapper:
    def __init__(self, *args, **kwargs):
        self._countries = extract_countries()
        self._gmaps = googlemaps.Client(key=CONFIGURATION.get_token_of("google.maps.api"))

    def google_normalizer(self, query):
        predictions = self._gmaps.places_autocomplete(input_text=query)
        for p in predictions:
            if 'locality' in p["types"] and 'political' in p["types"]:
                return p["terms"][0]["value"]

    def normalizer(self, country):
        norm_dict = {
            'U.S.': 'United States of America',
            'US': 'United States of America',
            'USA': 'United States of America',
            'United States': 'United States of America',
            'U.K.': 'United Kingdom',
            'UK': 'United Kingdom',
            'Soviet Union': 'Russia',
            'Scotland': 'United Kingdom',
            'Wales': 'United Kingdom',
            'England': 'United Kingdom',
            'Northern Ireland': 'United Kingdom',
        }
        if country in norm_dict.keys():
            return norm_dict[country]
        return country


class LastFMScrapper(Scrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = CONFIGURATION.keys['']

    def summary_parser(self, text):
        country_occur = defaultdict(int)
        for word in text.split(' '):
            word = word.strip('(),. ').replace("\n", "")
            if word == "":
                continue
            if word[0].isupper():
                try:
                    pos_country = self.normalizer(word)
                    if pos_country in self._countries:
                        country_occur[pos_country] += 1
                except KeyError:
                    pass
        return None if len(country_occur) == 0 else \
            max(country_occur, key=lambda i: country_occur[i])


class DiscogsScrapper(Scrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = discogs.Client(
            'visualast/0.0.1',
            consumer_key=CONFIGURATION.get_token_of('discogs.key'),
            consumer_secret=CONFIGURATION.get_token_of('discogs.secret')
        )

    def get_artist_address(self, artist_name):
        results = self.client.search(artist_name, type='artist')
        try:
            return results[0].artists[0]
        except:
            return None


class MusicBrainzScrapper(Scrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    ds = DiscogsScrapper()
    print(ds.get_artist_address('Bowery Electric'))
