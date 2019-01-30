import uuid
import re
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

import pylast
import wikipedia as wiki
import googlemaps as gmaps
import musicbrainzngs as mbz

from config import Configuration
from utils import get_logger, extract_countries

legal_countries = extract_countries()
logger = get_logger(__name__)
lastfm_client = pylast.LastFMNetwork(api_key=Configuration().tokens.last_fm)
gmaps_client = gmaps.Client(key=Configuration().tokens.google_maps_api)
mbz.set_useragent(app=Configuration().app_name, version=Configuration().app_version)
session = uuid.uuid4()


class CountryOfArtistScrapper:
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

    @staticmethod
    def normalize_with_dictionary(blob):
        norm_dict = {
            'United States of America': ['U.S.', 'US', 'USA', 'United States'],
            'United Kingdom': ['U.K.', 'UK', 'Scotland', 'Wales', 'England', 'Northern Ireland'],
            'Russia': ['Russian Federation', 'Soviet Union']
        }
        for key, value in norm_dict.items():
            for country in value:
                if blob == country:
                    return key
        return blob

    @staticmethod
    def normalize_with_gmaps(query):
        predictions = gmaps_client.places_autocomplete(input_text=query, session_token=session)
        for p in predictions:
            if 'locality' in p["types"] and 'political' in p["types"]:
                if p["terms"][0]["value"] in legal_countries:
                    return p["terms"][0]["value"]
                for term in p["terms"]:
                    norm_term = CountryOfArtistScrapper.normalize_with_dictionary(term["value"])
                    if norm_term in legal_countries:
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
                        pos_country = CountryOfArtistScrapper.normalize_with_dictionary(word)
                        if pos_country in legal_countries:
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
                res_country = CountryOfArtistScrapper.normalize_with_dictionary(
                    origin.text.split(',')[-1][1:]
                )
            except AttributeError:
                return summary_parser(page.summary)
            if res_country in legal_countries:
                return res_country
            return summary_parser(page.summary)
        else:
            return summary_parser(page.summary)

    @staticmethod
    def get_from_lastfm_summary(artist):
        """
        :param artist:  pylast.Artist object
        :return: country for successful extraction, otherwise - None
        """
        req = requests.get("https://www.last.fm/music/{}".format(artist.name.replace(' ', '+')))
        soup = BeautifulSoup(req.text, features="lxml")
        try:
            facts = soup.find("p", {"class": 'factbox-summary'}).string
            if '(' in facts:
                facts = facts[:facts.find('(') - 1]
            locations = facts.strip(',')
            for l in locations:
                nl = CountryOfArtistScrapper.normalize_with_dictionary(l)
                if nl in legal_countries:
                    return nl
            return CountryOfArtistScrapper.normalize_with_gmaps(facts)
        except (AttributeError, KeyError):
            summary = artist.get_bio_summary()
            country_occur = defaultdict(int)
            for word in summary.split(' '):
                word = word.strip('(),. ').replace("\n", "")
                if word == "":
                    continue
                if word[0].isupper():
                    try:
                        possible_country = CountryOfArtistScrapper.normalize_with_dictionary(word)
                        if possible_country in legal_countries:
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
                if country not in legal_countries:
                    country = CountryOfArtistScrapper.normalize_with_dictionary(country)
                if country not in legal_countries:
                    country = CountryOfArtistScrapper.normalize_with_gmaps(country)
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
        country = CountryOfArtistScrapper.get_from_musicbrainz(lastfm_artist)
        if country not in legal_countries:
            country = CountryOfArtistScrapper.get_from_lastfm_summary(lastfm_artist)
        logger.info("Artist:\t{}\tCountry:{}\n".format(lastfm_artist.name, country))
        return country

    @staticmethod
    def get_one_by_string(artist_name):
        lastfm_artist = lastfm_client.get_artist(artist_name=artist_name)
        return CountryOfArtistScrapper.get_one(lastfm_artist)


if __name__ == '__main__':
    print(CountryOfArtistScrapper.get_one_by_string('Bowery Electric'))
