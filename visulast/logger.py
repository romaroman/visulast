import logging
import logging.config
import yaml

with open('../logger.yml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def get_logger(name):
    return logging.getLogger(name)
