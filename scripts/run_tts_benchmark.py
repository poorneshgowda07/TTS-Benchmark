import argparse
import asyncio
import os
import json
from pathlib import Path
from dotenv import load_dotenv

import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.benchmark.dataset import DatasetManager
from src.providers.openai import OpenAITTS
from src.providers.elevenlabs import ElevenLabsTTS
from src.providers.deepgram import DeepgramTTS

load_dotenv()

PROVIDERS = {
    "openai": lambda: OpenAITTS(api_key=os.getenv("OPENAI_API_KEY")),
    "elevenlabs": lambda: ElevenLabsTTS(api_key=os.getenv("ELEVENLABS_API_KEY")),
    "deepgram": lambda: DeepgramTTS(api_key=os.getenv("DEEPGRAM_API_KEY")),
}

async def run_benchmark(provider_name: str, mode: str):
    print(f"Starting benchmark for {provider_name} in {mode} mode...")
    try:
        provider = PROVIDERS[provider_name]()
    except KeyError:
        print(f"Provider {provider_name} not implemented.")
        return

    manager = DatasetManager()
    categories = ["conversational", "formatting", "hinglish", "emotion"]
    
    results = []
    
    for category in categories:
        data = manager.load_dataset(category)
        for item in data:
            text = item["text"]
            item_id = item["id"]
            
            print(f"[{provider_name}] Processing [{category}] {item_id}")
            
            try:
                if mode == "batch":
                    audio, ttfa = await provider.generate_audio(text)
                    results.append({
                        "provider": provider_name,
                        "category": category,
                        "item_id": item_id,
                        "ttfa": ttfa,
                        "success": True
                    })
                elif mode == "streaming":
                    first = True
                    async for chunk, time_elapsed in provider.generate_stream(text):
                        if first:
                            results.append({
                                "provider": provider_name,
                                "category": category,
                                "item_id": item_id,
                                "ttfa": time_elapsed,
                                "success": True
                            })
                            first = False
                            break # Only measuring TTFA for now to save time
            except Exception as e:
                print(f"Error processing {item_id}: {e}")
                results.append({
                    "provider": provider_name,
                    "category": category,
                    "item_id": item_id,
                    "error": str(e),
                    "success": False
                })
                
    output_dir = Path("data/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / f"{provider_name}_results.json", "w") as f:
        json.dump(results, f, indent=4)

async def main():
    parser = argparse.ArgumentParser(description="Run TTS Benchmark")
    parser.add_argument("--model", type=str, default="all", help="Model to benchmark (e.g., openai, elevenlabs, all)")
    parser.add_argument("--mode", type=str, choices=["batch", "streaming"], default="batch")
    
    args = parser.parse_args()
    
    models_to_run = list(PROVIDERS.keys()) if args.model == "all" else [args.model]
    
    for model in models_to_run:
        await run_benchmark(model, args.mode)

if __name__ == "__main__":
    asyncio.run(main())
