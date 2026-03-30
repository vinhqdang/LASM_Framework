import json
import os
from typing import List, Dict

class AttackRegistry:
    def __init__(self, registry_path: str = "data/attack_registry.json"):
        self.registry_path = registry_path
        self.attacks = []
        if os.path.exists(registry_path):
            with open(registry_path, 'r', encoding='utf-8') as f:
                self.attacks = json.load(f)

    def get_attacks_before(self, time_limit: float) -> List[Dict]:
        """Get all attacks published before a certain time."""
        return [a for a in self.attacks if a.get('publication_time', 0) <= time_limit]

    def get_sasr(self, attack: Dict, defense: str, budget_tier: str) -> float:
        """Lookup pre-computed SASR for a given attack and defense."""
        defenses = attack.get('defenses', {})
        def_stats = defenses.get(defense, {})
        return def_stats.get(budget_tier, 0.0)
