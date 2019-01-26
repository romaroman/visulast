import json
import sys
import errno as err
import utils
import os

from logger import get_logger

path = os.path.dirname(os.path.abspath(__file__))
PROJ_PATH = path[:9 + path.find('visulast')]

logger = get_logger(__name__)

DB_ENGINES = ['postgresql', 'sqlite']


def errmsg(msg, e=None, code=-1):
    logger.error('Configuration error\n{}\n\n{}' % msg % e)
    # print(msg + '.\nChange configuration at config.json\n' % e)
    sys.exit(code)


class Configuration(metaclass=utils.Singleton):
    class Tokens:
        def __init__(self, tokens):
            self.google_maps_api = tokens['google.maps.api']
            self.telegram_bot = tokens['telegram.bot']
            self.last_fm = tokens['last.fm']
            self.aws_service = tokens['aws.service']
            self.docker_hub = tokens['docker.hub']

    class Database:
        def __init__(self, dbconfig):
            try:
                self.engine = dbconfig['engine']
                self.dbname = dbconfig['dbname']
                self.username = dbconfig['username']
                self.password = dbconfig['password']
                self.hostname = dbconfig['hostname']
                self.port = dbconfig['port']
            except KeyError as e:
                pass
                #errmsg('Uncorrect credits, check database configuration', e)

        def get_sql_url(self):

            if self.engine not in DB_ENGINES:
                errmsg('Incorrect database engine', SystemError)

            elif self.engine == 'postgresql':
                try:
                    if self.password:
                        self.password = ":" + self.password
                    if self.port:
                        self.port = ":" + self.port
                    return 'postgresql://{}{}@{}{}/{}'. \
                        format(self.username, self.password, self.hostname, self.port, self.dbname)
                except KeyError as e:
                    errmsg('Uncorrect credits, at {} engine'.format(self.engine), e)

            elif self.engine == 'sqlite':
                try:
                    return 'sqlite:///{}.sqlite'.format(self.dbname)
                except KeyError as e:
                    errmsg('Uncorrect credits, at {} engine'.format(self.engine), e)

    def __init__(self, engine='default'):
        try:
            self.json_loader(PROJ_PATH + 'config.json')
            self.tokens = Configuration.Tokens(self.config['tokens'])
            self.database = Configuration.Database(self.config['database'][engine])

            self.app_name = self.config['appName']
            self.app_version = self.config['appVersion']
        except (KeyError, TypeError) as e:
            errmsg('Something went wrong', e)

    def json_loader(self, file):
        try:
            with open(file, 'r+') as jfile:
                try:
                    self.config = json.load(jfile)
                except (TypeError, json.JSONDecodeError) as e:
                    errmsg("Couldn\'t decode {} file, check it\'s validity".format(file), e)
        except FileNotFoundError as e:
            errmsg('File {} not found, check if it exists in {}'.format(file, PROJ_PATH), e, err.ENFILE)


CONFIGURATION = Configuration('default')
