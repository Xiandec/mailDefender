import yaml
import logging


class Config(object):
    def __init__(self) -> None:
        with open('config.yaml') as file:
            self._yaml = yaml.safe_load(file)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def get_value(self, key: str) -> any:
        try:
            return self._yaml[key]
        except:
            return None
