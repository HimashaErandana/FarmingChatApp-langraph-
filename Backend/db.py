from pymongo import MongoClient



class DB:
    _instance = None
    
    def __new__(cls,  url: str = "mongodb+srv://himashaerandana1234_db_user:WYVXpjfRGIgdZbGY@cluster0.bopzoec.mongodb.net/?appName=Cluster0"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = MongoClient(url)
            cls._instance.db = cls._instance.client['Cluster0']
        
        return cls._instance


    def get_db(self):
        return self.db

