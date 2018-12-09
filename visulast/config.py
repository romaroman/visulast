import json
import sys
import errno as err

import utils

DB_ENGINES = ['postgresql', 'sqlite']


def errmsg(msg):
    print(msg+'.\nChange configuration at config.json')
    sys.exit(err.ENODATA)


class Configuration(metaclass=utils.Singleton):
    def __init__(self, db='default'):
        try:
            jdict = self.json_loader('config.json')
            self.db = jdict['database'][db]
            self.tokens = jdict['tokens']
        except (KeyError, TypeError) as e:
            errmsg('Something went wrong.\n{}' % e)
            sys.exit(-1)

    def get_sql_url(self):
        try:
            engine = self.db['engine']
        except KeyError as e:
            errmsg('Couldn\'t extract database engine. Aborting.')

        if engine not in DB_ENGINES:
            errmsg('Incorrect database engine')
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
            except:
                errmsg('Uncorrect credits, at {} engine' % engine)
        elif engine == 'sqlite':
            try:
                dbname = self.db['dbname']
                return 'sqlite:///{}.sqlite'.format(dbname)
            except:
                errmsg('Uncorrect credits, at {} engine' % engine)

    def json_loader(self, file):
        try:
            with open(file, 'r+') as jfile:
                try:
                    data = json.load(jfile)
                    return data
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
