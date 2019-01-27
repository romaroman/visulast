import logging
import logging.config
import yaml

from globals import PROJ_PATH

with open(PROJ_PATH + 'logger.yaml', 'r+') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def get_logger(name):
    return logging.getLogger(name)
