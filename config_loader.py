import json


class ConfigLoader:
    def __init__(self):
        self.config = None

    def load(self):
        with open('config.json') as json_data_file:
            config = json.load(json_data_file)
            return config

    def get_config(self):
        if self.config:
           return self.config

        cfg = self.load()
        return cfg
