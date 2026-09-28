import time
import httpx
from typing import AsyncGenerator
from .base import TTSProvider

class DeepgramTTS(TTSProvider):
    def __init__(self, api_key: str, model_name: str = "aura-asteria-en"):
        super().__init__(name="Deepgram", model_name=model_name, api_key=api_key)
        self.base_url = "https://api.deepgram.com/v1/speak"

    @property
    def cost_per_1m_chars(self) -> float:
        return 15.0

    async def generate_audio(self, text: str, voice_id: str = None, sample_rate: int = 16000) -> tuple[bytes, float]:
        start_time = time.perf_counter()
        
        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": text
        }
        
        model_to_use = voice_id if voice_id else self.model_name
        url = f"{self.base_url}?model={model_to_use}&encoding=linear16&sample_rate={sample_rate}"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            ttfa = time.perf_counter() - start_time
            return response.content, ttfa

    async def generate_stream(self, text: str, voice_id: str = None, sample_rate: int = 16000) -> AsyncGenerator[tuple[bytes, float], None]:
        start_time = time.perf_counter()
        
        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": text
        }
        
        model_to_use = voice_id if voice_id else self.model_name
        url = f"{self.base_url}?model={model_to_use}&encoding=linear16&sample_rate={sample_rate}"
        
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", url, headers=headers, json=payload) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes(chunk_size=4096):
                    if chunk:
                        yield chunk, time.perf_counter() - start_time
