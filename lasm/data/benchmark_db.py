import json
import os
from typing import List

class BenchmarkDB:
    """Mock implementation of Benchmark Results Database"""
    def __init__(self, db_path: str = "data/benchmark_results.json"):
        self.db_path = db_path
        self.results = []
        if os.path.exists(db_path):
            with open(db_path, 'r', encoding='utf-8') as f:
                self.results = json.load(f)

    def query_results(self, entry_point_type: str, time_range: List[float]) -> List[dict]:
        """Query DB for results matching criteria."""
        matches = []
        for r in self.results:
            if r.get('entry_point_type') == entry_point_type:
                t = r.get('time', 0.0)
                if time_range[0] <= t <= time_range[1]:
                    matches.append(r)
        return matches
