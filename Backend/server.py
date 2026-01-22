import socketio
from socketio import ASGIApp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import DB
from services.message_services import message
from services.message_services import get_all_messages
from VectorDB.vectorizer import Vcetorizer
from Graph.Graph import invoke_graph

from Graph.Graph import Graph

'''''
sio = socketio.AsyncServer(
    cors_allowed_origins='*',
    async_mode="asgi",
    logger=True                         
)
'''
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from pydantic import BaseModel

class AskRequest(BaseModel):
    message: str




@app.post('/ask')
async def ask(req:AskRequest):
    print(req.message)
    res = await message(req.message)
    print(res)
    return res

@app.post('/askg')
async def askg(req:AskRequest):
    print(req.message)
    res = invoke_graph(req.message)
    print(res)
    return res


@app.post('/ask_temp')
async def askg(req:AskRequest):
    print(req.message)
    res = {
    "name": "AI",
    "content": f"this reply is dummy {req.message}"
    }
    return res


@app.get('/all_messages')
async def gte_all():
    return await get_all_messages()


@app.get('/allm')
async def get_all():
    return [
        {
    "name": "AI",
    "content": f"this reply is dummy "
    },
    {
    "name": "hello",
    "content": f"this reply is dummy"
    },
    {
    "name": "AI",
    "content": '''NFO:     Started server process [9716]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:52427 - "GET /allm HTTP/1.1" 200 OK
INFO:     127.0.0.1:52427 - "GET /allm HTTP/1.1" 200 OK
INFO:     127.0.0.1:51826 - "OPTIONS /ask_temp HTTP/1.1" 200 OK
h
INFO:     127.0.0.1:51826 - "POST /ask_temp HTTP/'''
    }
    ,{
    "name": "nimal",
    "content": f"this reply is dummy"
    }
]


@app.get('/ask')
async def ask():

    return "hello there"


mongo = DB()
db = mongo.get_db()

if hasattr(db,"db"):
    print("ok")


# Create a GET endpoint


#socket_app = ASGIApp(sio, other_asgi_app=app)

'''''





@sio.event
async def Ask(sid, data=None):
    print("From user:", data)
    print("SID:", sid)
    print(data)
    msg = {
        "user": "Himasha",
        "content": "hello",
    }

    
    #s = Graph("hello")


    # ✅ reply ONLY to this user
    await sio.emit("reply", msg, to=sid)



'''