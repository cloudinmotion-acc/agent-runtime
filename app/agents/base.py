from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, router, memory):
        self.router = router
        self.memory = memory

    @abstractmethod
    async def run(self, session_id: str, input_text: str, model: str):
        pass
