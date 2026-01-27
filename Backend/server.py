import socketio
from socketio import ASGIApp
from fastapi import FastAPI,HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from db import DB
from services.Messages.message_services import message
from services.Messages.message_services import get_all_messages
from VectorDB.vectorizer import Vcetorizer
from Graph.Graph import invoke_graph
from bson import ObjectId

from Graph.Graph import Graph


from services.Auth.modles import UserSigup,UserLogin,Token
from services.Auth.auth import hash_pw,verify_pw,create_access_token,get_current_user

from services.User.model import UserCreate,UserOut
from services.User.UserServices import UserService


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
    
    return  res

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
async def gte_all(current_user: str = Depends(get_current_user)):
    return await get_all_messages()






us = UserService()
@app.post("/signup")
async def signup(user:UserSigup):
    created_user = await us.create_users(
           user
    )
    '''
         name=user.name,
            email=user.email,
            password=user.password
    '''
    return {"message": f"User created successfully{created_user}"}


fake_users_db ={}
@app.post("/login", response_model=Token)
async def login(user: UserLogin):
    db_user = await us.getuser_by_email(user.email)
    print(db_user)
    if not db_user or not verify_pw(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.email)
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/profile")
async def profile(current_user: dict = Depends(get_current_user)):
    print(current_user)
    return current_user


@app.post("/create_u")
async def create(user:UserCreate, response_model=UserOut):
     db_instance = DB()  # singleton instance
     users_col = db_instance.get_collection("users")
     result = await users_col.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hash_pw(user.password)  # hashed password
    })
     
     return {
        "id": str(result.inserted_id),  # convert ObjectId to string
        "name": user.name,
        "email": user.email
    }

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