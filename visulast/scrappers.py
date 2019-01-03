import sys

import requests
from collections import defaultdict

import wikipedia as wiki
import pylast
import googlemaps as gmaps
import musicbrainzngs as mbz
import discogs_client as discogs
from networkx.algorithms.coloring.tests.test_coloring import lf_hc

from loader import extract_countries
from config import CONFIGURATION

mbz.set_useragent('visulast', '0.0.1')


class CountryExtractor:
    def __init__(self, lf_username, *args, **kwargs):
        try:
            self.lastfm_c = pylast.LastFMNetwork(api_key=CONFIGURATION.last_fm, username=lf_username)
        except pylast.WSError as e:
            sys.exit('User with {} username not found'.format(lf_username))

        self.gclient = gmaps.Client(key=CONFIGURATION.google_maps_api)
        self.discogs_c = discogs.Client(
            'visualast/0.0.1',
            consumer_key=CONFIGURATION.discogs_key,
            consumer_secret=CONFIGURATION.discogs_secret
        )

    def google_normalizer(self, query):
        predictions = self.gclient.places_autocomplete(input_text=query)
        for p in predictions:
            if 'locality' in p["types"] and 'political' in p["types"]:
                return p["terms"][0]["value"]

    def blob_normalizer(self, blob):
        norm_dict = {
            'U.S.'            : 'United States of America',
            'US'              : 'United States of America',
            'USA'             : 'United States of America',
            'United States'   : 'United States of America',
            'U.K.'            : 'United Kingdom',
            'UK'              : 'United Kingdom',
            'Soviet Union'    : 'Russia',
            'Scotland'        : 'United Kingdom',
            'Wales'           : 'United Kingdom',
            'England'         : 'United Kingdom',
            'Northern Ireland': 'United Kingdom',
        }
        if blob in norm_dict.keys():
            return norm_dict[blob]
        return blob

    def get_country_list(self, lim=50):
        user = self.lastfm_c.get_user(username=self.lastfm_c.username)
        top = user.get_top_artists(limit=lim)
        countries = dict()
        return countries

class Normalizer:


class LastFMScrapper:
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
        return None if len(country_occur) == 0 else max(country_occur, key=lambda i: country_occur[i])


class DiscogsScrapper:
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
        except KeyError:
            return None
        finally:
            return None


def wikipedia_getter(artist):
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
                origin = [elem for elem in info_table(text=re.compile(r'Origin|Born|Residence'))][0].parent.findNext()
            except AttributeError:
                return None
            except IndexError:
                return None
        try:
            res_country = normalize_country(origin.text.split(',')[-1][1:])
        except AttributeError:
            return summary_parser(page.summary)
        if res_country in COUNTRIES:
            return res_country
        return summary_parser(page.summary)
    else:
        return summary_parser(page.summary)


def brainz_getter(mbid):
    req = requests.get(MUSIC_BRAINZ_URL.format(mbid)).json()
    try:
        if 'area' in req:
            if req['area']:
                country = normalize_country(req['area']['name'])
                if country in COUNTRIES:
                    return country
                return None
        return None
    except TypeError and KeyError:
        return None


def last_summary_getter(artist):
    req = requests.get(LAST_FM_URL.format(artist, LAST_FM_API_KEY))
    try:
        data = req.json()['artist']
    except KeyError:
        return None

    fact_country = factbox_parser(data)
    if fact_country:
        return fact_country
    if 'bio' in data:
        if 'summary' in data['bio']:
            return summary_parser(data['bio']['summary'])
    return None


def factbox_parser(jd):  # jd variable is data in json format =)
    try:
        url = jd['url']
    except KeyError:
        return None
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        facts = soup.find('p', {'class': 'factbox-summary'}).text
    except AttributeError:
        return None

    pos_country = normalize_country(facts[:(facts.find('(') - 1)].split(',')[-1][1:])
    if pos_country in COUNTRIES:
        return pos_country
    return None


if __name__ == "__main__":
    ds = DiscogsScrapper()
    print(ds.get_artist_address('Bowery Electric'))
