# Singleton template for using in Configuration and others classes
import logging
import os
import shapefile

import warnings
import functools
import logging.config
import yaml


_path = os.path.dirname(os.path.abspath(__file__))
PROJ_PATH = _path[:9 + _path.find('visulast')]
SHAPE_FILE = PROJ_PATH + "assets/shapefiles/worldmaps/small/ne_110m_admin_0_countries_lakes"

with open(PROJ_PATH + 'logger.yaml', 'r+') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def get_logger(name):
    return logging.getLogger(name)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def deprecated(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn(f"Call to deprecated function {func.__name__}.",
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func


def extract_countries():
    countries = []
    for record in shapefile.Reader(SHAPE_FILE, 'countries').iterRecords():
        countries.append(record['SOVEREIGNT'])
    return countries
