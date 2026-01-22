#pip install langchain langchain-community chromadb python-docx tiktoken docx2txt sentence-transformers

import os
from langchain_community.document_loaders import Docx2txtLoader
import re
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

from .Embedding_model import Embedding_model

def Vcetorizer() -> bool:
    dir = "D:\My projects\Agentic AI\Srilankan Rice farming field solutions\code\original\Backend\VectorDB\docs"

    domain = [
        'pest_control',
        'organic_farming',
        'fertilizer',
        'farming_basics',
        'Decease'
    ]

    documents = []

    for idx,file in enumerate(os.listdir(dir)):
        if file.endswith(".docx"):
                loader = Docx2txtLoader(os.path.join(dir, file))
                docs = loader.load()

                for doc in docs:
                    doc.metadata["domain"] = domain[idx]
                    doc.metadata["source"] = file

                documents.extend(docs)


    def clean(text:str) -> str:
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,%()-]', '', text)

        return text

    for doc in documents:
        doc.page_content = clean(doc.page_content)        



    text_splitter = CharacterTextSplitter(
            separator="",
            chunk_size=450,
            chunk_overlap=70,
        )  

    chunks = text_splitter.split_documents(documents)


    embedding_model_instance = Embedding_model().embedding_model

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model_instance,
        persist_directory="D:\My projects\Agentic AI\Srilankan Rice farming field solutions\code\original\Backend\VectorDB\db"
    )

    vectorstore.persist()

    return True