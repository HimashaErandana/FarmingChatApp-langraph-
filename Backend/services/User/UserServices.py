from db import DB
from .model import UserCreate,UserOut
from datetime import datetime,timezone
from services.Auth.auth import hash_pw

class UserService:

    def __init__(self):
        self.db = DB()
        self.user_col = self.db.get_collection("users")
        

    async def create_users(self,user:UserCreate):


        result = await self.user_col.insert_one({
            "name": user.name,
            "email": user.email,
            "password": hash_pw(user.password)
        })

        return {
            "id": str(result.inserted_id),
            "name": user.name,
            "email": user.email
        }
    
    async def getuser_by_email(self,email:str):
        """Fetch user by name from database (async)"""
        
        user = await self.user_col.find_one({"email": email})
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]  # remove ObjectId to prevent serialization errors
        return user