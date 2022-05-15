import random
import redis
<<<<<<< HEAD
from accountpool.setting import *
=======
from setting import *
>>>>>>> 3bd9a02e0b0537a70c1b67d45c712c56bdb002f0


class RedisClient(object):
    """
    redis client
    """
<<<<<<< HEAD
    
=======

>>>>>>> 3bd9a02e0b0537a70c1b67d45c712c56bdb002f0
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        init redis client
        :param host: redis host
        :param port: redis port
        :param password: redis password
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = type
        self.website = website
<<<<<<< HEAD
    
=======

>>>>>>> 3bd9a02e0b0537a70c1b67d45c712c56bdb002f0
    def name(self):
        """
        get hash name
        :return: name of hash
        """
        return f'{self.type}:{self.website}'
<<<<<<< HEAD
    
=======

>>>>>>> 3bd9a02e0b0537a70c1b67d45c712c56bdb002f0
    def set(self, username, value):
        """
        set key-value
        :param username: username
        :param value: password or cookies
        :return:
        """
        return self.db.hset(self.name(), username, value)
<<<<<<< HEAD
    
=======

>>>>>>> 3bd9a02e0b0537a70c1b67d45c712c56bdb002f0
    def get(self, username):
        """
        get value
        :param username: username
        :return:
        """
        return self.db.hget(self.name(), username)
<<<<<<< HEAD
    
=======

>>>>>>> 3bd9a02e0b0537a70c1b67d45c712c56bdb002f0
    def delete(self, username):
        """
        delete key-value
        :param username: username
        :return: result
        """
        return self.db.hdel(self.name(), username)
<<<<<<< HEAD
    
=======

>>>>>>> 3bd9a02e0b0537a70c1b67d45c712c56bdb002f0
    def count(self):
        """
        get count
        :return: count
        """
        return self.db.hlen(self.name())
<<<<<<< HEAD
    
=======

>>>>>>> 3bd9a02e0b0537a70c1b67d45c712c56bdb002f0
    def random(self):
        """
        get random cookies or password
        :return: random cookies or password
        """
        return random.choice(self.db.hvals(self.name()))
<<<<<<< HEAD
    
=======

>>>>>>> 3bd9a02e0b0537a70c1b67d45c712c56bdb002f0
    def usernames(self):
        """
        get all usernames
        :return: all usernames
        """
        return self.db.hkeys(self.name())
<<<<<<< HEAD
    
=======

>>>>>>> 3bd9a02e0b0537a70c1b67d45c712c56bdb002f0
    def all(self):
        """
        get all key-values
        :return: map of key-values
        """
        return self.db.hgetall(self.name())
