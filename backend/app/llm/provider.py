from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def invoke(self, prompt: str) -> str:
        """Send a prompt to the model and return its text response."""
