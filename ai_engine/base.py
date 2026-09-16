from abc import ABC, abstractmethod

class AIProvider(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def available(self):
        pass

    @abstractmethod
    def chat(self, messages, **kwargs):
        pass
