from db import DB
from .model import ChatCreate,ChatOut
from datetime import datetime,timezone
from bson import ObjectId
class ChatServices:

    def __init__(self):
        self.db = DB()
        self.chat_col = self.db.get_collection("chats")

    async def create_chat(self,chat:ChatCreate):


        result = await self.chat_col.insert_one({
            "userId": ObjectId(chat.userId),
            "created_at":  datetime.now(timezone.utc)
        })

        return {
            "id": str(result.inserted_id),
            "userId": chat.userId
        }
    
    async def get_all_chats(self,id):
        chats = []
        try:
            async for chat in self.chat_col.find({"userId":ObjectId(id)}):
                chats.append(ChatOut(
                    id=str(chat["_id"]),
                    userId=str(chat["userId"])
                ))
        except():
            print("error")
        return chats
 