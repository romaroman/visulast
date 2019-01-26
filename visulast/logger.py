import logging
import logging.config
import yaml
import os

path = os.path.dirname(os.path.abspath(__file__))
PROJ_PATH = path[:9 + path.find('visulast')]

with open(PROJ_PATH + 'logger.yaml', 'r+') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def get_logger(name):
    return logging.getLogger(name)
