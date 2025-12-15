import socketio
from socketio import ASGIApp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import DB

from Graph.Graph import Graph

sio = socketio.AsyncServer(
    cors_allowed_origins='*',
    async_mode="asgi"                           
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

socket_app = ASGIApp(sio, other_asgi_app=app)


mongo = DB()
db = mongo.get_db()

if hasattr(db,"db"):
    print("ok")




@sio.event
async def Ask(sid, data=None):
    print("From user:", data)
    print("SID:", sid)
    print(data)
    msg = {
        "user": "Himasha",
        "content": "hello",
    }

    
    s = Graph()


    # ✅ reply ONLY to this user
    await sio.emit("reply", msg, to=sid)

