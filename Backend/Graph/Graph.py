from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
#from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.checkpoint.memory import MemorySaver

from Graph.MessageState import State

#Agent imports
from Graph.Agents.Rag_agent.RagAgent import RagAgent
from Graph.Agents.weather_agent.WeatherAgent import WeatherAgent
from Graph.Agents.WebScraper_agent.WebScraperAgent import WebScraper
from Graph.Agents.Decease_agent.DeaseceAgent import DeseaceAgent

def Graph():

    deseaceAgent = DeseaceAgent("deseace_agent")
    weatherAgent = WeatherAgent("weather_agent")
    ragAgent = RagAgent("rag_agent")





    input_state: State = {
    "messages": [HumanMessage(content="Tell me about AI models")],
    "user_query": "Tell me about AI models",
    "query_type": "",
    "agent_output": "",
    "final_answer": ""
    }

    def Router(state:State):
        msg = state['messages'][-1].content.lower()

        if 'weather' in msg:
            out = 'api'
        elif "disease" in msg:
            out = "cnn"
        else:
            out = "rag"
        return {"query_type": out}

    
    def rag_node(state: State):
        q = state["user_query"]
        result = ragAgent.call(q)
        return {"agent_output": result}

    def api_node(state: State):
        q = state["user_query"]
        result = weatherAgent.call(q)
        return {"agent_output": result}

    
    def cnn_node(state: State):
        q = state["user_query"]
        result = deseaceAgent.call(q)
        return {"agent_output": result}

    def summarizer_node(state:State):
        result = f"summarized for{state['agent_output']} "
        return {"messages": [AIMessage(content=result)]}

    builder = StateGraph(State)
    builder.add_node("Router", Router)
    builder.add_node("rag", rag_node)
    builder.add_node("api", api_node)
    builder.add_node("cnn", cnn_node)
    builder.add_node("summarizer",summarizer_node)

    # Edges
    builder.add_edge(START, "Router")

    builder.add_conditional_edges(
        "Router",
        lambda s: s["query_type"],
        {
            "rag": "rag",
            "api": "api",
            "cnn": "cnn",
        },
    )

    builder.add_edge("rag", "summarizer")
    builder.add_edge("api", "summarizer")
    builder.add_edge("cnn", "summarizer")

    builder.add_edge( "summarizer",END)


    '''checkpointer = MongoDBSaver(
        uri="mongodb+srv://himashaerandana1234_db_user:WYVXpjfRGIgdZbGY@cluster0.bopzoec.mongodb.net/?appName=Cluster0",
        db_name="Cluster0",
        collection_name="checkpoints_demo"
    )
'''
    checkpointer = MemorySaver()  # 🔹 Use memory saver for testing
    graph = builder.compile(checkpointer=checkpointer)

    result = graph.invoke(input_state, config={"configurable": {"thread_id": "user_123"}})
    return result