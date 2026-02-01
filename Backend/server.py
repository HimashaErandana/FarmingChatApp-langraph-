import socketio
from socketio import ASGIApp
from fastapi import FastAPI,HTTPException, Depends,UploadFile, File, Form,Path
from fastapi.middleware.cors import CORSMiddleware
from db import DB
from services.Messages.message_services import message
from services.Messages.message_services import get_all_messages
from VectorDB.vectorizer import Vcetorizer
from Graph.Graph import invoke_graph
from bson import ObjectId
from typing import Optional
import os
from datetime import datetime
import shutil  
from fastapi.staticfiles import StaticFiles
from Graph.Graph import Graph
from services.llm_service import invoke_llm

from services.Auth.modles import UserSigup,UserLogin,Token
from services.Auth.auth import hash_pw,verify_pw,create_access_token,get_current_user

from services.User.model import UserCreate,UserOut
from services.User.UserServices import UserService
from services.Chat.ChatServices import ChatServices
from services.Chat.model import ChatCreate
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
    res = invoke_llm(req.message)
    return  res





UPLOAD_DIR = "Backend/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)




app.mount("/images", StaticFiles(directory=UPLOAD_DIR), name="images")


#msgess
@app.post('/ask_i')
async def aski(
    msg:str = Form(...),
    image:Optional[UploadFile] = File(None),
    chat_id:str = Form(...)
):
    
    req = AskRequest(message=msg)
    image_link=None
    filepath = None
    if(image):
        print(image.filename)
        # Create a unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{image.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        # Save file locally
        with open(filepath, "wb") as f:
            shutil.copyfileobj(image.file, f)

        image_link = f"/images/{filename}"
        print("Saved file:", filepath)
   
    res = await message(req.message,str(chat_id),filepath,image_link)

    return res    



@app.post('/askg')
async def askg(req:AskRequest):
    print(req.message)
    res = (req.message)
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


@app.get('/all_messages/{cid}')
async def gte_all(current_user: str = Depends(get_current_user),cid: str = Path(...)):
    return await get_all_messages(cid)


#chat
chatser = ChatServices()
@app.post('/create_chat')
async def create_chat(chat:ChatCreate):
    res = await chatser.create_chat(chat)
    return res

@app.get('/get_all_chats/{uid}')
async def get_all_chats(uid: str = Path(...)):
    res = await chatser.get_all_chats(uid)
    return res



#user


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



@app.post("/login", response_model=Token)
async def login(user: UserLogin):
    db_user = await us.getuser_by_email(user.email)
    print(db_user)
    if not db_user or not verify_pw(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.email)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id":str(db_user['id'])
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