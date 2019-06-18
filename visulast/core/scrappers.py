import uuid
import re
from io import BytesIO

import requests
from PIL import Image
from bs4 import BeautifulSoup
from collections import defaultdict

import pylast
import wikipedia as wiki
import googlemaps
import musicbrainzngs
import numpy as np

from visulast.config import Configuration
from visulast.utils.helpers import get_logger, extract_countries

legal_countries = extract_countries()
logger = get_logger(__name__)
gmaps_client = googlemaps.Client(key=Configuration().tokens.google_maps_api)
musicbrainzngs.set_useragent(app=Configuration().app_name, version=Configuration().app_version)
session = uuid.uuid4()


class CountryScrapper:
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
        predictions = gmaps_client.places_autocomplete(input_text=query)
        for p in predictions:
            if 'locality' in p["types"] and 'political' in p["types"]:
                if p["terms"][0]["value"] in legal_countries:
                    return p["terms"][0]["value"]
                for term in p["terms"]:
                    norm_term = CountryScrapper.normalize_with_dictionary(term["value"])
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
                        pos_country = CountryScrapper.normalize_with_dictionary(word)
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
                t_artist = artist + f' ({var})'
                try:
                    page = wiki.page(t_artist)
                    if page:
                        soup = BeautifulSoup(page.html(), "html.parser")
                        break
                except wiki.DisambiguationError:
                    continue
                except wiki.PageError:
                    continue
            return soup
        except wiki.PageError:
            return None

        info_table = soup.find("table", {"class": "infobox"})
        if info_table:
            origin = info_table.find("span", {"class": "birthplace"})
            if not origin:
                try:
                    pattern = re.compile(r'Origin|Born|Residence')
                    origin = [elem for elem in info_table(text=pattern)][0].parent.findNext()
                except AttributeError:
                    return None
                except IndexError:
                    return None
            try:
                res_country = CountryScrapper.normalize_with_dictionary(origin.text.split(',')[-1][1:])
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
        req = requests.get(f"https://www.last.fm/music/{artist.name.replace(' ', '+')}")
        soup = BeautifulSoup(req.text, features="lxml")
        try:
            facts = soup.find("p", {"class": 'factbox-summary'}).string
            if '(' in facts:
                facts = facts[:facts.find('(') - 1]
            locations = facts.strip(',')
            for l in locations:
                nl = CountryScrapper.normalize_with_dictionary(l)
                if nl in legal_countries:
                    return nl
            return CountryScrapper.normalize_with_gmaps(facts)
        except (AttributeError, KeyError):
            summary = artist.get_bio_summary()
            country_occur = defaultdict(int)
            for word in summary.split(' '):
                word = word.strip('(),. ').replace("\n", "")
                if word == "":
                    continue
                if word[0].isupper():
                    try:
                        possible_country = CountryScrapper.normalize_with_dictionary(word)
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
                mb_art = musicbrainzngs.get_artist_by_id(id=mbid)
                country = mb_art['artist']['area']['name']
                if country not in legal_countries:
                    country = CountryScrapper.normalize_with_dictionary(country)
                if country not in legal_countries:
                    country = CountryScrapper.normalize_with_gmaps(country)
                return country
            except KeyError:
                pass
        else:
            res = musicbrainzngs.search_artists(query=lastfm_artist.name)
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
        country = CountryScrapper.get_from_musicbrainz(lastfm_artist)
        if country not in legal_countries:
            country = CountryScrapper.get_from_lastfm_summary(lastfm_artist)
        logger.info(f"Artist:\t{lastfm_artist.name}\tCountry:{country}\n")
        return country

    @staticmethod
    def get_one_by_string(artist_name):
        lastfm_artist = Configuration().lastfm_network.get_artist(artist_name=artist_name)
        return CountryScrapper.get_one(lastfm_artist)


class ImageScrapper(object):
    def __init__(self):
        super(ImageScrapper, self).__init__()

    @staticmethod
    def get_image_by_entity(entity):
        imgclass = {
            pylast.Album: 'cover-art',
            pylast.Artist: 'avatar'
        }[type(entity.item)]

        req = requests.get(entity.item.get_url())
        soup = BeautifulSoup(req.text, features="lxml")
        img_url = soup.findAll("img", {"class": imgclass})

        if not img_url:
            logger.warning(f"Cover image wasn't found for {entity.item}")
            return np.full((170, 170), 255, dtype=np.uint8)
        else:
            response = requests.get(img_url[0].attrs['src'])
            image = np.array(Image.open(BytesIO(response.content)))
            return image


class FriendsScrapper(object):
    def __init__(self):
        super(FriendsScrapper, self).__init__()

    @staticmethod
    def get_friends_by_username(username):
        target_class = 'link-block-target'
        req = requests.get(f'https://www.last.fm/user/{username}/following')
        soup = BeautifulSoup(req.text, features="lxml")
        usernames = soup.findAll("a", {"class": target_class})
        return [user.contents[0] for user in usernames][::-1]
