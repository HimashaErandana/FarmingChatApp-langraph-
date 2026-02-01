from ..BaseAgent import BaseAgent
from .model_service import ModelService

class DeseaceAgent(BaseAgent):

    def __init__(self):
        self.service = ModelService()

    def call(self,img_url):
        path = 'D:\My projects\Agentic AI\Srilankan Rice farming field solutions\code\original\Bacterial Leaf Blight.jpg'
        pred = self.service.getService(img_url)
        print(pred)
        return pred