import re
import sys
import requests
from collections import defaultdict
from bs4 import BeautifulSoup

import pylast
import wikipedia as wiki
import googlemaps as gmaps
import musicbrainzngs as mbz
import discogs_client as discogs

from loader import COUNTRIES
from config import CONFIGURATION
from setup import APP_NAME, APP_VERSION


class CountryExtractor:
    def __init__(self):
        try:
            self.lastfm_c = pylast.LastFMNetwork(api_key=CONFIGURATION.last_fm)
        except pylast.WSError:
            sys.exit('Invalid API key')

        self.gclient = gmaps.Client(key=CONFIGURATION.google_maps_api)
        self.discogs_c = discogs.Client(
            '{}/{}'.format(APP_NAME, APP_VERSION),
            consumer_key=CONFIGURATION.discogs_key,
            consumer_secret=CONFIGURATION.discogs_secret
        )

        mbz.set_useragent(app=APP_NAME, version=APP_VERSION)

    @staticmethod
    def blob_normalizer(blob):
        norm_dict = {
            'United States of America': ['U.S.', 'US', 'USA', 'United States'],
            'United Kingdom': ['U.K.', 'UK', 'Scotland', 'Wales', 'England', 'Northern Ireland'],
            'Russia': ['Russian Federation', 'Soviet Union']
        }
        for k, v in norm_dict.items():
            for c in v:
                if blob == c:
                    return k
        return blob

    def google_normalizer(self, query):
        predictions = self.gclient.places_autocomplete(input_text=query)
        for p in predictions:
            if 'locality' in p["types"] and 'political' in p["types"]:
                return p["terms"][0]["value"]

    def wikipedia_getter(self, artist):
        def summary_parser(text):
            country_occur = defaultdict(int)
            for word in text.split(' '):
                word = word.strip('(),. ').replace("\n", "")
                if word == "":
                    continue
                if word[0].isupper():
                    try:
                        pos_country = self.blob_normalizer(word)
                        if pos_country in COUNTRIES:
                            country_occur[pos_country] += 1
                    except KeyError:
                        pass
            return None if len(country_occur) == 0 else max(country_occur, key=lambda i: country_occur[i])

        try:
            page = wiki.page(artist)
            soup = BeautifulSoup(page.html(), "html.parser")
        except wiki.DisambiguationError:
            possible_variants = [
                'band', 'singer', 'songwriter', 'compositor', 'musician', 'artist', 'performer'
            ]
            soup = None
            for var in possible_variants:
                page = None
                t_artist = artist + ' ({})'.format(var)
                try:
                    page = wiki.page(t_artist)
                    if page:
                        soup = BeautifulSoup(page.html(), "html.parser")
                        break
                except wiki.DisambiguationError:
                    continue
                except wiki.PageError:
                    continue
            if not soup:
                return None
        except wiki.PageError:
            return None

        info_table = soup.find("table", {"class": "infobox"})
        if info_table:
            origin = info_table.find("span", {"class": "birthplace"})
            if not origin:
                try:
                    origin = [elem for elem in info_table(text=re.compile(r'Origin|Born|Residence'))][
                        0].parent.findNext()
                except AttributeError:
                    return None
                except IndexError:
                    return None
            try:
                res_country = self.blob_normalizer(origin.text.split(',')[-1][1:])
            except AttributeError:
                return summary_parser(page.summary)
            if res_country in COUNTRIES:
                return res_country
            return summary_parser(page.summary)
        else:
            return summary_parser(page.summary)

    # def last_summary_getter(artist):
    #     req = requests.get(LAST_FM_URL.format(artist, LAST_FM_API_KEY))
    #     try:
    #         data = req.json()['artist']
    #     except KeyError:
    #         return None
    #
    #     fact_country = factbox_parser(data)
    #     if fact_country:
    #         return fact_country
    #     if 'bio' in data:
    #         if 'summary' in data['bio']:
    #             return summary_parser(data['bio']['summary'])
    #
    #     return None
    #
    # def factbox_parser(jd):  # jd variable is data in json format =)
    #     try:
    #         url = jd['url']
    #     except KeyError:
    #         return None
    #     page = requests.get(url)
    #     soup = BeautifulSoup(page.text, 'html.parser')
    #     try:
    #         facts = soup.find('p', {'class': 'factbox-summary'}).text
    #     except AttributeError:
    #         return None
    #
    #     pos_country = normalize_country(facts[:(facts.find('(') - 1)].split(',')[-1][1:])
    #     if pos_country in COUNTRIES:
    #         return pos_country
    #     return None

    def get_country_list(self, lim=50):
        user = self.lastfm_c.get_user(username=self.lastfm_c.username)
        top = user.get_top_artists(limit=lim)
        countries = dict()
        return countries


if __name__ == "__main__":
    pass
