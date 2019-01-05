import re

import requests
from collections import defaultdict
from bs4 import BeautifulSoup

import pylast
import wikipedia as wiki
import googlemaps as gmaps
import musicbrainzngs as mbz

from loaders import COUNTRIES
from config import CONFIGURATION


lastfm_client = pylast.LastFMNetwork(api_key=CONFIGURATION.last_fm)
gmaps_client = gmaps.Client(key=CONFIGURATION.google_maps_api)
mbz.set_useragent(app=CONFIGURATION.app_name, version=CONFIGURATION.app_version)


class ArtistCountryScrapper:
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

    @staticmethod
    def normalize_with_dictionary(blob):
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

    @staticmethod
    def normalize_with_gmaps(query):
        predictions = gmaps_client.places_autocomplete(input_text=query)
        for p in predictions:
            if 'locality' in p["types"] and 'political' in p["types"]:
                if p["terms"][0]["value"] in COUNTRIES:
                    return p["terms"][0]["value"]
                for term in p["terms"]:
                    norm_term = ArtistCountryScrapper.normalize_with_dictionary(term["value"])
                    if norm_term in COUNTRIES:
                        return norm_term

    @staticmethod
    def get_from_wiki(artist):
        def summary_parser(text):
            country_occur = defaultdict(int)
            for word in text.split(' '):
                word = word.strip('(),. ').replace("\n", "")
                if word == "":
                    continue
                if word[0].isupper():
                    try:
                        pos_country = ArtistCountryScrapper.normalize_with_dictionary(word)
                        if pos_country in COUNTRIES:
                            country_occur[pos_country] += 1
                    except KeyError:
                        pass
            return None if len(country_occur) == 0 else max(
                country_occur,
                key=lambda i: country_occur[i]
            )

        page = None
        try:
            page = wiki.page(artist)
            soup = BeautifulSoup(page.html(), "html.parser")
        except wiki.DisambiguationError:
            possible_variants = [
                'band', 'singer', 'songwriter', 'compositor', 'musician', 'artist', 'performer'
            ]
            soup = None
            for var in possible_variants:
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
                    origin = [elem for elem in info_table(
                        text=re.compile(r'Origin|Born|Residence'))
                        ][0].parent.findNext()
                except AttributeError:
                    return None
                except IndexError:
                    return None
            try:
                res_country = ArtistCountryScrapper.normalize_with_dictionary(
                    origin.text.split(',')[-1][1:]
                )
            except AttributeError:
                return summary_parser(page.summary)
            if res_country in COUNTRIES:
                return res_country
            return summary_parser(page.summary)
        else:
            return summary_parser(page.summary)

    '''
    param: pylast.Artist
    '''
    @staticmethod
    def get_from_lastfm_summary(artist):
        req = requests.get("https://www.last.fm/music/{}".format(artist.name.replace(' ', '+')))
        soup = BeautifulSoup(req.text, features="lxml")
        try:
            facts = soup.find("p", {"class": 'factbox-summary'}).string
            if '(' in facts:
                facts = facts[:facts.find('(') - 1]
            locations = facts.strip(',')
            for l in locations:
                nl = ArtistCountryScrapper.normalize_with_dictionary(l)
                if nl in COUNTRIES:
                    return nl
            return ArtistCountryScrapper.normalize_with_gmaps(facts)
        except (AttributeError, KeyError):
            summary = artist.get_bio_summary()
            country_occur = defaultdict(int)
            for word in summary.split(' '):
                word = word.strip('(),. ').replace("\n", "")
                if word == "":
                    continue
                if word[0].isupper():
                    try:
                        possible_country = ArtistCountryScrapper.normalize_with_dictionary(word)
                        if possible_country in COUNTRIES:
                            country_occur[possible_country] += 1
                    except KeyError:
                        pass
            return None if len(country_occur) == 0 else max(country_occur, key=lambda i: country_occur[i])
        

    @staticmethod
    def get_from_musicbrainz(lastfm_artist):
        mbid = lastfm_artist.get_mbid()
        if mbid:
            try:
                mb_art = mbz.get_artist_by_id(id=mbid)
                country = mb_art['artist']['area']['name']
                if country not in COUNTRIES:
                    country = ArtistCountryScrapper.normalize_with_dictionary(country)
                if country not in COUNTRIES:
                    country = ArtistCountryScrapper.normalize_with_gmaps(country)
                return country
            except KeyError:
                pass
        else:
            res = mbz.search_artists(query=lastfm_artist.name)
            if res:
                for entry in res['artist-list']:
                    if entry['name'] and entry['name'].lower() == lastfm_artist.name.lower():
                        try:
                            return entry['area']['name']
                        except KeyError:
                            pass
        return None

    @staticmethod
    def get_one(lastfm_artist):
        country = ArtistCountryScrapper.get_from_musicbrainz(lastfm_artist)
        if country not in COUNTRIES:
            country = ArtistCountryScrapper.get_from_lastfm_summary(lastfm_artist)
        return country

    @staticmethod
    def get_one_by_string(artist_name):
        lastfm_artist = lastfm_client.get_artist(artist_name=artist_name)
        return ArtistCountryScrapper.get_one(lastfm_artist)

    @staticmethod
    def get_all_by_user(username):
        # last_user = lastfm_client.
        pass


if __name__ == "__main__":
    # s = lastfm_client.get_artist("drake")
    lib = lastfm_client.get_user(username='Florian_y').get_library().get_artists()
    for a in lib[:20]:
        print(a.item.name, ArtistCountryScrapper.get_one(a.item))

