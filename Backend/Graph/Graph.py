from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
#from langgraph.checkpoint.mongodb import MongoDBSaver
#from langgraph.checkpoint.memory import MemorySaver

from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient
from config import MONGO_URL


from services.llm_service import invoke_llm
from Graph.MessageState import State
from typing import Optional
#Agent imports
#from Graph.Agents.Rag_agent.RagAgent import RagAgent
from Graph.Agents.weather_agent.WeatherAgent import WeatherAgent
from Graph.Agents.WebScraper_agent.WebScraperAgent import WebScraper
from Graph.Agents.Decease_agent.DeaseceAgent import DeseaceAgent
import requests

class Graph:
    def __init__(self):
        #self.deseaceAgent = DeseaceAgent()
        self.weatherAgent = WeatherAgent('weather')
        self.deceaseAgent = DeseaceAgent()

        self.graph = self.build()




    def Router(self,state:State):
            
            msg = state["messages"][-1].content.lower()

            greeting_keywords = [
    "hi","hello","hey","hi there","good morning","good afternoon","good evening",
    "how are you","how's it going","what's up","nice to meet you","good to see you",
    "bye","goodbye","see you later","take care","thanks","thank you"
]
            if "decease" in msg:
                out = 'cnn'
            elif 'weather' in msg:
                out = "api"
            elif msg.strip() in greeting_keywords:
                out = "greeting"
            else :
                out = "rag"
            
            return {"query_type": out}

        
    def rag_node(self,state: State):
        q = state["messages"][-1].content

        payload = {f"query": q}
        url = "http://127.0.0.1:8801/call_rag"
        result = requests.post(url, json=payload)
        return {"agent_output": result.json()}

    def api_node(self,state: State):
        q = state["messages"][-1].content
        result =  self.weatherAgent.call(q)
        #result = f"weather running  :: coutry{result.city}condition{result.condition}feels like{result.feels_like}"
        return {"agent_output": result}

    
    def cnn_node(self,state: State):
        q = state["messages"][-1].content
        result = self.deceaseAgent.call(state["img_url"])
        return {"agent_output": result}

    def summarizer_node(self,state:State):
        q = state["messages"][-1].content
        
        if state["query_type"] != "cnn":
            result = invoke_llm(
                                f"""
                You are an assistant that summarizes information.

                Task:
                Read the following content and generate a clear, concise, and relevant answer to the user's question.

                User question: "{q}"
                Content to use: "{state['agent_output']}"

                Guidelines:
                - If the content is about a rice disease, return only the **name of the disease**. 
                - Otherwise, base your answer only on the provided content. Do not add external information.  
                - Keep the answer concise and easy to understand.  
                - Respond in a complete sentence suitable for the user.  
                - Do not repeat the content verbatim; summarize meaningfully.

                Provide only the answer.
                """)
        else:
            result = str(state["agent_output"] )       
                        
        return {
            "messages": state["messages"] + [AIMessage(content=result)]
        }

    def greeting_node(self, state: State):
        msg = state["messages"][-1].content
        res = invoke_llm(f"Respond politely to this greeting: '{msg}'. Keep it short and friendly.")
        return {
            "messages": state["messages"] + [
                AIMessage(content=res)
            ]
        }

    def build(self):
        builder = StateGraph(State)

        builder.add_node("Router", self.Router)
        builder.add_node("rag", self.rag_node)
        builder.add_node("api", self.api_node)
        builder.add_node("cnn", self.cnn_node)
        builder.add_node("greeting", self.greeting_node)
        builder.add_node("summarizer", self.summarizer_node)

        builder.add_edge(START, "Router")

        builder.add_conditional_edges(
            "Router",
            lambda s: s["query_type"],
            {"greeting": "greeting","rag": "rag", "api": "api", "cnn": "cnn"}
        )

        builder.add_edge("rag", "summarizer")
        builder.add_edge("api", "summarizer")
        builder.add_edge("cnn", "summarizer")
        builder.add_edge("greeting", END)
        builder.add_edge("summarizer", END)


        client = MongoClient(MONGO_URL)
        Checkpointer = MongoDBSaver(
            client=client,
            db_name="Cluster0",
            collection_name="checkpoints"
        )
    

        return builder.compile(checkpointer=Checkpointer)



    def invoke(self,input:str,cid:str,img_url:str = None) -> str:

       
        
        input_state = {
            "messages": [HumanMessage(content=input)],
            "img_url": img_url
        }

        result = self.graph.invoke(
            input_state,
            config={"configurable": {"thread_id": cid}}
        )

        #result = self.graph.invoke({"messages": [HumanMessage(content=input)]}, config={"configurable": {"thread_id": "user_123"}})

        #input_state['messages'].append(AIMessage(content=result))

        return result["messages"][-1].content


graph_instance = Graph() 

def invoke_graph(input:str,cid,img_url:str = None) -> str:
    res = graph_instance.invoke(input=input,cid=cid,img_url=img_url)
    return res

    
    