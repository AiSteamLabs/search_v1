from abc import ABC, abstractmethod

class SearchEngineBase(ABC):
    def __init__(self):
        self.getInstanceFromEnv()
    
    @abstractmethod
    def search(self, query, **kwargs): pass
     
    @abstractmethod
    def getInstanceFromEnv(self):pass