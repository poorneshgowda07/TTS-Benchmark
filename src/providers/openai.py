import time
import httpx
from typing import AsyncGenerator
from .base import TTSProvider

class OpenAITTS(TTSProvider):
    def __init__(self, api_key: str, model_name: str = "tts-1"):
        super().__init__(name="OpenAI", model_name=model_name, api_key=api_key)
        self.base_url = "https://api.openai.com/v1/audio/speech"

    @property
    def cost_per_1m_chars(self) -> float:
        return 15.0 if self.model_name == "tts-1" else 30.0

    async def generate_audio(self, text: str, voice_id: str = "alloy", sample_rate: int = 24000) -> tuple[bytes, float]:
        start_time = time.perf_counter()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_name,
            "input": text,
            "voice": voice_id,
            "response_format": "wav"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            ttfa = time.perf_counter() - start_time
            return response.content, ttfa

    async def generate_stream(self, text: str, voice_id: str = "alloy", sample_rate: int = 24000) -> AsyncGenerator[tuple[bytes, float], None]:
        start_time = time.perf_counter()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_name,
            "input": text,
            "voice": voice_id,
            "response_format": "wav"
        }
        
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", self.base_url, headers=headers, json=payload) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes(chunk_size=4096):
                    if chunk:
                        yield chunk, time.perf_counter() - start_time
