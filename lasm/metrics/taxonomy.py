import json
import os
from collections import defaultdict
from typing import Dict
from lasm.systems.system_model import EntryPointType

class TaxonomyManager:
    def __init__(self, taxonomy_path: str = "data/harm_taxonomy.json"):
        self.taxonomy_path = taxonomy_path
        self._harm_weights = self._load_default_weights()
        if os.path.exists(taxonomy_path):
            self._load_from_json(taxonomy_path)
            
    def _load_default_weights(self) -> Dict[EntryPointType, float]:
        # Fallback based on plan specification
        return {
            EntryPointType.SYSTEM_PROMPT: 8.0,
            EntryPointType.USER_PROMPT: 5.0,
            EntryPointType.RETRIEVED_CONTEXT: 7.0,
            EntryPointType.TOOL_API_CALL: 9.0,
            EntryPointType.AGENT_MESSAGE: 10.0,
            EntryPointType.MEMORY_STORE: 8.0
        }

    def _load_from_json(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'harm_weights' in data:
                for k, v in data['harm_weights'].items():
                    try:
                        ep = EntryPointType(k)
                        self._harm_weights[ep] = float(v)
                    except ValueError:
                        pass

    def get_harm_weight(self, ep_type: EntryPointType) -> float:
        return self._harm_weights.get(ep_type, 1.0)
