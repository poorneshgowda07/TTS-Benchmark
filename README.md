# TTS Benchmarking & Evaluation Framework

A production-grade framework designed to benchmark text-to-speech (TTS) models and providers for real-time conversational Voice AI agents.

## Key Features

- **Latency Tracking**: Measures Time to First Audio (TTFA) and chunk delivery times across streaming protocols (WebSocket, Chunked HTTP).
- **Quality Evaluation**: Supports Word Error Rate (WER) via STT to assess intelligibility.
- **Cost Analysis**: Estimates the cost per 1M characters or hour of audio.
- **Provider Support**: Out-of-the-box adapters for ElevenLabs, Deepgram, OpenAI, PlayHT, Cartesia, Sarvam AI, and Cloud Providers (Azure, AWS, GCP).
- **Hinglish/Indian Languages**: Specifically tests code-mixing and regional language performance.

## Setup

1. **Install Dependencies**:
   ```bash
   poetry install
   ```

2. **Configuration**:
   Copy `.env.example` to `.env` and fill in your API keys.

3. **Data Preparation**:
   Run the dataset generator to create test text samples.
   ```bash
   poetry run python scripts/prepare_text_dataset.py
   ```

4. **Running Benchmark**:
   ```bash
   poetry run python scripts/run_tts_benchmark.py --model all --mode streaming
   ```
