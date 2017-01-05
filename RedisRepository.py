import redis
from config_loader import ConfigLoader
import pickle

class RedisRepository:
    def __init__(self):
        cfg = ConfigLoader()
        self.config = cfg.get_config()
        host = self.config.get('redis_host')
        port = self.config.get('redis_port')
        db = self.config.get('redis_db')
        self.ttl = self.config.get('redis_ttl')
        self.db = redis.StrictRedis(host=host, port=port, db=db)

    def store(self, key, data):
        """Saves values to db """
        if self.ttl:
            self.db.setex(key, self.ttl, data)
        else:
            self.db.set(key, data)

    def store_binary(self, key, data):
        """Saves data in binary to db"""

        if self.ttl:
            self.db.setex(key,  self.ttl, pickle.dumps(data))
        else:
            self.db.set(key, pickle.dumps(data))
        print('processed key {0}'.format(key))

    def read(self, key):
        data = self.db.get(key)
        return data

    def read_binary(self, key):
        data = pickle.loads(self.db.get(key))
        return data

    def remove(self, key):

        self.db.remove(key)

    def exits(self, key):
        return self.db.exists(key)

