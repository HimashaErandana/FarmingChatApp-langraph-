from abc import ABC,abstractmethod

class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.active = True

    @abstractmethod
    def call(self):
        "every agents must implemnt"
        pass