import json
import os
from typing import List

class PromptSetManager:
    def __init__(self, sets_dir: str = "data/prompt_sets"):
        self.sets_dir = sets_dir

    def load_prompt_set(self, name: str) -> List[str]:
        path = os.path.join(self.sets_dir, f"{name}.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('prompts', [])
        # Return dummy prompts if not found
        return [f"Dummy prompt {i}" for i in range(200)]
