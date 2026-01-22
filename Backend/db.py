from pymongo import MongoClient
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient

class DB:
    _instance = None #WYVXpjfRGIgdZbGY
    
    def __new__(cls,  url: str = MONGO_URL):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = AsyncIOMotorClient(url)
            cls._instance.db = cls._instance.client['Cluster0']
        
        return cls._instance


    def get_db(self):
        return self.db
    
    def get_collection(self,name:str):
        return self.db[name]

