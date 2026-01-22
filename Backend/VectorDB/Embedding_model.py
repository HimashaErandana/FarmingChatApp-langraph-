import os
from langchain_community.embeddings import HuggingFaceEmbeddings

# Optional: set a custom cache folder
os.environ["HF_HOME"] = r"D:\My projects\Agentic AI\Srilankan Rice farming field solutions\code\original\Backend\huggingface_cache"  # make sure this folder exists or it will be created

class Embedding_model:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )