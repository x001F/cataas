import logging.config
import yaml

with open('./logs/.log', 'w'): pass


def get_logger(name: str) -> logging.Logger:
    with open('./src/config/config.yaml') as f:
        logging.config.dictConfig(yaml.load(f, yaml.FullLoader).get('logging'))
        return logging.getLogger(name)
