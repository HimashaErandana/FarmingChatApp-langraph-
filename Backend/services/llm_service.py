import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from ollama import chat




from config import GOOGLE_API_KEY
class LLM:
    def __init__(self):
        #os.environ["GOOGLE_API_KEY"] = "AIzaSyCIhEOQwxNMBqE3BcAoY7eqUvzwX9rtmu0"

        # Initialize LLM once
        self.model =  "llama3.2:3b"

    def call_llm(self,prompt):
        response = chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}],
        )
        print(response.message.content)
        return response.message.content
    
llm = LLM()

def invoke_llm(prompt:str) -> str:
    res = llm.call_llm(prompt=prompt)
    #clean_text = res.encode('utf-8').decode('unicode_escape')

    return res