from abc import ABC, abstractmethod
from typing import AsyncGenerator
import time

class TTSProvider(ABC):
    def __init__(self, name: str, model_name: str, api_key: str = None):
        self.name = name
        self.model_name = model_name
        self.api_key = api_key

    @abstractmethod
    async def generate_audio(self, text: str, voice_id: str, sample_rate: int = 16000) -> tuple[bytes, float]:
        """
        Generate audio in batch mode.
        Returns:
            bytes: The audio payload (wav/mp3 format)
            float: Time to first audio (TTFA) in seconds.
        """
        pass

    @abstractmethod
    async def generate_stream(self, text: str, voice_id: str, sample_rate: int = 16000) -> AsyncGenerator[tuple[bytes, float], None]:
        """
        Generate audio in streaming mode.
        Yields:
            bytes: Audio chunk
            float: Time since the start of the request.
        """
        pass
    
    @property
    def cost_per_1m_chars(self) -> float:
        """Return the estimated cost per 1M characters in USD."""
        return 0.0
