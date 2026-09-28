import time
import httpx
from typing import AsyncGenerator
from .base import TTSProvider

class ElevenLabsTTS(TTSProvider):
    def __init__(self, api_key: str, model_name: str = "eleven_turbo_v2_5"):
        super().__init__(name="ElevenLabs", model_name=model_name, api_key=api_key)
        self.base_url = "https://api.elevenlabs.io/v1/text-to-speech"

    @property
    def cost_per_1m_chars(self) -> float:
        return 30.0

    async def generate_audio(self, text: str, voice_id: str = "EXAVITQu4vr4xnSDxMaL", sample_rate: int = 44100) -> tuple[bytes, float]:
        start_time = time.perf_counter()
        
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": text,
            "model_id": self.model_name,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        url = f"{self.base_url}/{voice_id}?output_format=pcm_{sample_rate}"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            ttfa = time.perf_counter() - start_time
            return response.content, ttfa

    async def generate_stream(self, text: str, voice_id: str = "EXAVITQu4vr4xnSDxMaL", sample_rate: int = 44100) -> AsyncGenerator[tuple[bytes, float], None]:
        start_time = time.perf_counter()
        
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": text,
            "model_id": self.model_name
        }
        
        url = f"{self.base_url}/{voice_id}/stream?output_format=pcm_{sample_rate}"
        
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", url, headers=headers, json=payload) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes(chunk_size=4096):
                    if chunk:
                        yield chunk, time.perf_counter() - start_time
