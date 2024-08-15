from manager import DB_NAME
import json
import os

class Database:
    def __init__(self):
        self.dbname = DB_NAME
        self.cache = {}
        self.re_data()

    def get_data(self):
        if os.path.isfile(self.dbname):
            fdata = open(self.dbname, "r")
            data = fdata.read()
        else:
            data = str({})
            ndata = open(self.dbname, "w")
            ndata.write(data)
        return data

    def re_data(self):
        data = self.get_data()
        self.cache = eval(self.get_data()) if isinstance(data, str) else data

    def get(self, key):
        if key in self.cache:
            return self.cache.get(key)

    def set(self, key=None, value=None, delete_key=None):
        data = self.cache
        if delete_key:
            try:
                del data[delete_key]
            except KeyError:
                pass
        if key and value:
            data.update({key: value})
        with open(self.dbname, "w") as dbfile:
            json.dump(data, dbfile)
        self.re_data()
        return True

    def delete(self, key):
        if key in self.cache:
            return self.set(delete_key=key)

class LocalDB:
    def __init__(self):
        self.db = Database()
        self.get = self.db.get
        self.set = self.db.set
        self.delete = self.db.delete
        self.cache = {}
        self.recache()

    def keys(self):
        return []
        
    def recache(self):
        self.cache.clear()
        for key in self.keys():
            self.cache.update({key: self.get_key(key)})

    def get_data(self, key=None, data=None):
        if key:
            data = self.get(str(key))
        if data and isinstance(data, str):
            try:
                data = eval(data)
            except:
                pass
        return data

    def set_key(self, key, value):
        value = self.get_data(data=value)
        self.cache[key] = value
        return self.set(str(key), str(value))

    def del_key(self, key):
        if key in self.cache:
            del self.cache[key]
        self.delete(key)
        return True

    def get_key(self, key):
        if key in self.cache:
            value = self.cache[key]
        else:
            value = self.get_data(key)
            self.cache.update({key: value})
        try:
            data = eval(value)
        except:
            data = value
        return data

DB = LocalDB()