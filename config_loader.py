import json


class ConfigLoader:
    def __init__(self):
        self.config = {}

    def load(self):
        with open('config.json') as json_data_file:
            config_raw = json.load(json_data_file)
            # Build up the config object
            self.config["server"] = config_raw.get('server').get('host')
            self.config["port"] = config_raw.get('server').get('port')
            self.config['mysql_host'] = config_raw.get('mysql').get('host')
            self.config['mysql_database'] = config_raw.get('mysql').get('database')
            self.config['mysql_user'] = config_raw.get('mysql').get('username')
            self.config['mysql_pass'] = config_raw.get('mysql').get('password')
            self.config['similarity_cuttoff'] = config_raw.get('cb').get('similarity_cutoff')
            self.config['mongo_host'] = config_raw.get('mongo').get('host')
            self.config['mongo_port'] = config_raw.get('mongo').get('port')
            self.config['data_user_limit'] = config_raw.get('data').get('user_limit')
            self.config['data_doc_limit'] = config_raw.get('data').get('doc_limit')
            self.config['data_download_history'] = config_raw.get('data').get('download_history_days')
            self.config['data_min_downloads'] = config_raw.get('data').get('min_downloads')
            self.config['redis_host'] = config_raw.get('redis').get('host')
            self.config['redis_port'] = config_raw.get('redis').get('port')
            self.config['redis_db'] = config_raw.get('redis').get('db')
            self.config['redis_ttl'] = config_raw.get('redis').get('ttl')
        return self.config

    def get_config(self):
        if self.config:
           return self.config

        cfg = self.load()
        return cfg
