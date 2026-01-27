from db import DB
from model import ChatCreate,ChatOut
from datetime import datetime,timezone
class ChatServices:

    def __init__(self):
        self.db = DB()
        self.chat_col = self.db.get_collection("chats")

    async def create_chat(self,chat:ChatCreate):


        result = await self.chat_col.insert_one({
            "userId": chat.userId,
            "created_at":  datetime.now(timezone.utc)
        })

        return {
            "id": str(result.inserted_id),
            "userId": chat.userId
        }