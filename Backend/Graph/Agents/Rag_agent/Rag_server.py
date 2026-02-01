from fastapi import FastAPI
from pydantic import BaseModel
from chromadb import Client
from .RagAgent import RagAgent
from VectorDB.vectorizer import Vcetorizer


app = FastAPI(title="Chroma Vector DB Server")


class AgentRequest(BaseModel):
    query: str

agent = RagAgent()

@app.post("/call_rag")
def call_agent(req:AgentRequest):
    print("rag ran")
    return agent.call(req.query)

@app.get("/hello")
def run_function():
    return {"message": "hello"}
  

'''''
@app.get("/create_vec_db")
def run_function():
    result = Vcetorizer()
    if result == True:
        return {"message": "vec db created sccesssfully"}
    return None
    '''