from typing import List, TypedDict, Annotated
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

class State(TypedDict):
        messages: Annotated[List[BaseMessage], "add_messages"]
        query_type: str  
        agent_output: str
        final_answer: str