import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from config import GOOGLE_API_KEY
class LLM:
    def __init__(self):
        #os.environ["GOOGLE_API_KEY"] = "AIzaSyCIhEOQwxNMBqE3BcAoY7eqUvzwX9rtmu0"

        # Initialize LLM once
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3,
            google_api_key=GOOGLE_API_KEY
        )

    def call_llm(self,prompt):
        response = self.llm.invoke([HumanMessage(content=prompt)]) 
        return response.content
    
llm = LLM()

def invoke_llm(prompt:str) -> str:
    '''res = llm.call_llm(prompt=prompt)
    clean_text = res.encode('utf-8').decode('unicode_escape')'''

    clean_text = f"dummy{prompt}"

    return clean_text