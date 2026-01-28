from .mongodbServices import MongoDB_services
from Graph.Graph import invoke_graph
from .messageModel import MessageModel
from typing import List
class Message_services:

    def __init__(self):
        self.mongo_services = MongoDB_services()


    async def message(self,msg,filepath:str=None,img_url:str=None):

        print("msh services")
        

        user_msg = MessageModel(
            message=msg,
            msgType="USER",
            img_url=img_url
        )

        if(user_msg):
            print("u created")

        u_msg = await self.mongo_services.create_msg(user_msg)

        print("did it ")

        res = invoke_graph(msg,filepath)

        ai_msg = MessageModel(
            message=res,
            msgType="AI"
        )

        crated = await self.mongo_services.create_msg(ai_msg)
        print(crated)
        print("ai msg",ai_msg)
        return [u_msg,ai_msg]

    async def get_all(self):
        messages = await self.mongo_services.get_all()
        return [
            {
                "id": str(m.id),
                "message": m.message,
                "msgType": m.msgType,
                "img_url":m.img_url
            }
            for m in messages
        ]


message_services = Message_services()

async def message(msg,filepath:str=None,img_url:str=None) -> str:
    return await message_services.message(msg,filepath,img_url)


async def get_all_messages():
    messages =  await message_services.get_all()
    return messages