from db import DB
from .messageModel import MessageModel
from typing import List,Optional
from bson import ObjectId


class MongoDB_services:
    

    def __init__(self):
        self.db = DB().get_db()
        self.collection = self.db.get_collection("messages")


    '''async def create_msg(self,msg:MesaageModel):
        data = msg.model_dump(by_alias=True)
        result = await self.collection.insert_one(data)
        data['_id'] = result.inserted_id
        return MesaageModel(**data)'''
    
    async def create_msg(self, msg: MessageModel) -> MessageModel:
        # Convert model to dict
        data = msg.model_dump(by_alias=True, exclude_none=True)  # removes _id if None
        data.pop("_id", None)  # just in case

        # MongoDB auto-generates _id
        result = await self.collection.insert_one(data)

        # Fetch the document with generated _id
        created_doc = await self.collection.find_one({"_id": result.inserted_id})

        created_doc["_id"] = str(created_doc["_id"])
        return MessageModel(**created_doc)

            
    async def get_all(self) -> List[MessageModel]:
        messages = []
        async for msg in self.collection.find():
            msg["_id"] = str(msg["_id"])
            messages.append(MessageModel(**msg))
        print (messages)    
        return messages
    
    async def get_by_id(self, message_id: str) -> Optional[MessageModel]:
        msg = await self.collection.find_one({"_id": ObjectId(message_id)})
        return MessageModel(**msg) if msg else None

    async def update(self, message_id: str, message: MessageModel):
        update_data = message.dict(
            by_alias=True,
            exclude={"id", "created_at"},
            exclude_unset=True
        )

        result = await self.collection.update_one(
            {"_id": ObjectId(message_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            return None

        updated = await self.collection.find_one({"_id": ObjectId(message_id)})
        return MessageModel(**updated)

    async def delete(self, message_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(message_id)})
        return result.deleted_count == 1