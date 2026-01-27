from pydantic import BaseModel

class ChatCreate(BaseModel):
    userId: str  # string representation of ObjectId

class ChatOut(BaseModel):
    id: str
    userId: str
