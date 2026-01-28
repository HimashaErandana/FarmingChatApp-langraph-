from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
#from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.checkpoint.memory import MemorySaver
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

            #qType = invoke_llm(f"using this {msg} give me an exact type this message belongs wether it belongs to api: means weather or cnn : means disease or rag: rag means if it doenst belong to ther two categories just guve me the type ")

            if 'weather' in msg:
                out = 'api'
            elif "disease" in msg:
                out = "cnn"
            else:
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
        result = invoke_llm(f"act as a summarizer give me a suitble answer for the question {q} , use this contnet for this {state['agent_output']} ")
        
        return {
            "messages": state["messages"] + [AIMessage(content=result)]
        }


    def build(self):
        builder = StateGraph(State)

        builder.add_node("Router", self.Router)
        builder.add_node("rag", self.rag_node)
        builder.add_node("api", self.api_node)
        builder.add_node("cnn", self.cnn_node)
        builder.add_node("summarizer", self.summarizer_node)

        builder.add_edge(START, "Router")

        builder.add_conditional_edges(
            "Router",
            lambda s: s["query_type"],
            {"rag": "rag", "api": "api", "cnn": "cnn"}
        )

        builder.add_edge("rag", "summarizer")
        builder.add_edge("api", "summarizer")
        builder.add_edge("cnn", "summarizer")
        builder.add_edge("summarizer", END)

        '''checkpointer = MongoDBSaver(
            uri="mongodb+srv://himashaerandana1234_db_user:WYVXpjfRGIgdZbGY@cluster0.bopzoec.mongodb.net/?appName=Cluster0",
            db_name="Cluster0",
            collection_name="checkpoints_demo"
        )
    '''

        return builder.compile(checkpointer=MemorySaver())



    def invoke(self,input:str,img_url:str = None) -> str:

       
        
        input_state = {
            "messages": [HumanMessage(content=input)],
            "img_url": img_url
        }

        result = self.graph.invoke(
            input_state,
            config={"configurable": {"thread_id": "user_123"}}
        )

        #result = self.graph.invoke({"messages": [HumanMessage(content=input)]}, config={"configurable": {"thread_id": "user_123"}})

        #input_state['messages'].append(AIMessage(content=result))

        return result["messages"][-1].content


graph_instance = Graph() 

def invoke_graph(input:str,img_url:str = None) -> str:
    res = graph_instance.invoke(input=input,img_url=img_url)
    return res

    
    