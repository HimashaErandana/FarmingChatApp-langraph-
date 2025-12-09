from pymongo import MongoClient
from typing_extensions import Type



class DB(Type):
    _instance = None
    
    def _new_(cls,  url: str = "mongodb://localhost:27017/"):
        if cls._instance is None:
            cls._instance = super()._new_(cls)
            cls._instance.client = MongoClient(url)
            cls._instance.db = cls._instance.client['db_name']
        
        return cls._instance


    def get_db(self):
        return self.db



def db_connect():
    client = MongoClient(url)
    db = client["mydb"]
    return db