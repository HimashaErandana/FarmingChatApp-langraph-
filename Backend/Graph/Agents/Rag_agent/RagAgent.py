from ..BaseAgent import BaseAgent
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from VectorDB.Embedding_model import Embedding_model

class RagAgent(BaseAgent):

    
    def __init__(self):

        embedding_model = Embedding_model().embedding_model

        self.vectorstore = Chroma(
        persist_directory="D:\My projects\Agentic AI\Srilankan Rice farming field solutions\code\original\Backend\VectorDB\db",
        embedding_function=embedding_model
    )
    
    def call(self,q:str):

        res = self.vectorstore.similarity_search(
            query=q,
            k=3
        )

        print("res",res)
        context = [f"{doc.page_content}\n(Source: {doc.metadata.get('source','unknown')})" for doc in res]
        print(context)
        

        return context