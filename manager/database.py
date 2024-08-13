from redis import Redis
from localdb import Database
import json

def get_data(self, key):
    data = self.get(str(key))
    if data:
        try:
            data = eval(data)
        except BaseException:
            pass
    return data

class RedisDB:
    def __init__(self):
        MainUrl = "redis-10247.c59.eu-west-1-2.ec2.redns.redis-cloud.com:10247"
        URL = (MainUrl).split(":")[0]
        PORT = (MainUrl).split(":")[-1]
        self.db = Redis(
                host=URL,
                password="MgX2INYxyA8S5lCvZCtuITmmDkgmpPbi",
                port=int(PORT),
                decode_responses=True,
            )
        self.set = self.db.set
        self.get = self.db.get
        self.keys = self.db.keys
        self.ping = self.db.ping
        self.delete = self.db.delete
        self.recache()

    def recache(self):
        self.cache = {}
        for keys in self.keys():
            self.cache.update({keys: self.get_key(keys)})

    @property
    def name(self):
        return "Redis"

    @property
    def usage(self):
        allusage = 0
        for x in self.keys():
            usage = self.db.memory_usage(x)
            allusage += usage
        return allusage

    def set_key(self, key, value):
        value = str(value)
        try:
            value = eval(value)
        except BaseException:
            pass
        self.cache.update({key: value})
        return self.set(str(key), str(value))

    def get_key(self, key):
        if key in self.cache:
            return self.cache[key]
        get = get_data(self, key)
        self.cache.update({key: get})
        return get

    def del_key(self, key):
        if key in self.cache:
            del self.cache[key]
        return bool(self.delete(str(key)))
        
    def flushall(self):
        for x in self.keys():
            self.del_key(x)
        return True

class LocalDB:
    def __init__(self):
        self.db = Database("FidoDB")
        self.get = self.db.get
        self.set = self.db.set
        self.delete = self.db.delete
        self.cache = {}
        self.recache()

    def get_key(self, key):
        if key in self.cache:
            value = self.cache[key]
        else:
            value = self._get_data(key)
            self.cache.update({key: value})
        try:
            data = eval(value)
        except:
            data = value
        return data

    def recache(self):
        self.cache.clear()
        for key in self.keys():
            self.cache.update({key: self.get_key(key)})

    def keys(self):
        return []

    def del_key(self, key):
        if key in self.cache:
            del self.cache[key]
        self.delete(key)
        return True

    def _get_data(self, key=None, data=None):
        if key:
            data = self.get(str(key))
        if data and isinstance(data, str):
            try:
                data = ast.literal_eval(data)
            except BaseException:
                pass
        return data

    def set_key(self, key, value, cache_only=False):
        value = self._get_data(data=value)
        self.cache[key] = value
        if cache_only:
            return
        return self.set(str(key), str(value))

DB = LocalDB()
