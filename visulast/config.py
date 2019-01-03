import json
import sys
import errno as err

import utils

DB_ENGINES = ['postgresql', 'sqlite']


def errmsg(msg, e):
    print(msg + '.\nChange configuration at config.json\n' % e)
    sys.exit(err.ENODATA)


class Configuration(metaclass=utils.Singleton):
    def __init__(self, db='default'):
        try:
            self.json_loader('config.json')
            self.db = self.config['database'][db]
            self.tokens = self.config['tokens']
            self.fill_tokens()
        except (KeyError, TypeError) as e:
            errmsg('Something went wrong.', e)
            sys.exit(-1)

    # noinspection PyAttributeOutsideInit
    def fill_tokens(self):
        self.google_maps_api = self.get_token_of('google.maps.api')
        self.telegram_bot = self.get_token_of('telegram.bot')
        self.discogs_key = self.get_token_of('discogs.key')
        self.discogs_secret = self.get_token_of('discogs.secret')
        self.last_fm = self.get_token_of('last.fm')
        self.aws_service = self.get_token_of('aws.service')
        self.docker_hub = self.get_token_of('docker.hub')

    def get_sql_url(self):
        try:
            engine = self.db['engine']
        except KeyError as e:
            errmsg('Couldn\'t extract database engine. Aborting.', e)
            return

        if engine not in DB_ENGINES:
            errmsg('Incorrect database engine', SystemError)
        elif engine == 'postgresql':
            try:
                dbname = self.db['dbname']
                username = self.db['username']
                password = self.db['password']
                hostname = self.db['hostname']
                port = self.db['port']
                if password != "":
                    password = ":" + password
                if port != "":
                    port = ":" + port
                return 'postgresql://{}{}@{}{}/{}'.\
                    format(username, password, hostname, port, dbname)
            except KeyError as e:
                errmsg('Uncorrect credits, at {} engine'.format(engine), e)
        elif engine == 'sqlite':
            try:
                dbname = self.db['dbname']
                return 'sqlite:///{}.sqlite'.format(dbname)
            except KeyError as e:
                errmsg('Uncorrect credits, at {} engine'.format(engine), e)

    def json_loader(self, file):
        try:
            with open(file, 'r+') as jfile:
                try:
                    self.config = json.load(jfile)
                except (TypeError, json.JSONDecodeError) as e:
                    print("Couldn\'t decode {} file, check it\'s validity.\nError message:{}".format(file, e))
                    sys.exit(-1)
        except FileNotFoundError:
            print('File {} not found, check if it exists in project directory')
            sys.exit(err.ENFILE)

    """
    Possible parameters: google.maps.api | telegram.bot | discogs | last.fm | aws.service | docker.hub
    """
    def get_token_of(self, service):
        if service not in self.tokens.keys:
            return ""
        return self.tokens[service]


CONFIGURATION = Configuration('postgresql')
