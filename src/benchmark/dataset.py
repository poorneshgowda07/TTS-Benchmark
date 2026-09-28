import os
import json
from pathlib import Path
import hashlib

DATA_DIR = Path(__file__).parent.parent / "data" / "datasets"

class DatasetManager:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def get_text_hash(self, text: str) -> str:
        """Create a short hash of the text for unique filenames."""
        return hashlib.md5(text.encode("utf-8")).hexdigest()[:8]

    def load_dataset(self, category: str) -> list[dict]:
        file_path = self.data_dir / f"{category}.json"
        if not file_path.exists():
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_dataset(self, category: str, data: list[dict]):
        file_path = self.data_dir / f"{category}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
