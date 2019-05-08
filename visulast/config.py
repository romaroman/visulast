import json
import errno as err
import sys

from visulast.utils.helpers import get_logger, PROJ_PATH, Singleton

logger = get_logger(__name__)
DB_ENGINES = ['postgresql', 'sqlite']


def critical_error_handler(msg, e=None, code=-1):
    logger.critical(f'Cricitical error at {str(__name__ )}\n{msg}\n\n{e}')
    sys.exit(code)


class Configuration(metaclass=Singleton):
    def __init__(self):
        try:
            self.json_loader(PROJ_PATH + 'config.json')
            self.tokens = Configuration.TokensConfig(self.config['tokens'])
            self.database = Configuration.DatabaseConfig(self.config['database'])

            self.app_name = self.config['appName']
            self.app_version = self.config['appVersion']
        except (KeyError, TypeError) as e:
            critical_error_handler('Something went wrong', e)

    def json_loader(self, file):
        try:
            with open(file, 'r+') as jfile:
                try:
                    self.config = json.load(jfile)
                except (TypeError, json.JSONDecodeError) as e:
                    critical_error_handler(f"Couldn\'t decode {file} file, check it\'s validity", e)
        except FileNotFoundError as e:
            critical_error_handler(f'File {file} not found, check if it exists in {PROJ_PATH}', e, err.ENFILE)

    class TokensConfig:
        def __init__(self, tokens):
            self.google_maps_api = tokens['google.maps.api']
            self.telegram_bot = tokens['telegram.bot']
            self.last_fm = tokens['last.fm']
            self.aws_service = tokens['aws.service']
            self.docker_hub = tokens['docker.hub']
            self.liqpay_private_test =  tokens['liqbpay.private.test']
            self.liqpay_public_test = tokens['liqpay.public.test']

    class DatabaseConfig:
        def __init__(self, dbconfig):
            try:
                self.engine = dbconfig['engine']
                self.dbname = dbconfig['dbname']
                self.username = dbconfig['username']
                self.password = dbconfig['password']
                self.hostname = dbconfig['hostname']
                self.port = dbconfig['port']
                self.url = self._get_sql_url()
            except KeyError:
                pass

        def _get_sql_url(self):

            if self.engine not in DB_ENGINES:
                critical_error_handler('Incorrect database engine', SystemError)

            elif self.engine == 'postgresql':
                try:
                    if self.password:
                        self.password = ":" + self.password
                    if self.port:
                        self.port = ":" + self.port
                    return f'postgresql://{self.username}{self.password}@{self.hostname}{self.port}/{self.dbname}'
                except KeyError as e:
                    critical_error_handler(f'Uncorrect credits, at {self.engine} engine', e)

            elif self.engine == 'sqlite':
                try:
                    return f'sqlite:///{self.dbname}.sqlite'
                except KeyError as e:
                    critical_error_handler(f'Uncorrect credits, at {self.engine} engine', e)
            else:
                critical_error_handler(f'{self.engine} engine not yet implemented')
