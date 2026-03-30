import sys
from datetime import datetime
import json
import os
from lasm import LASMEvaluator

def main():
    print("Running LAS Evaluator CL...")
    evaluator = LASMEvaluator()
    sys_path = "tests/fixtures/sample_systems.json"
    
    # Ensure dir exists for dummy
    os.makedirs(os.path.dirname(sys_path), exist_ok=True)
    if not os.path.exists(sys_path):
        with open(sys_path, 'w') as f:
            json.dump({"name": "CLI_SYS", "scope": "S2"}, f)
            
    system = evaluator.load_system(sys_path)
    res = evaluator.compute_las(system, datetime.now(), "B_mid")
    print(f"LAS_norm: {res.LAS_norm:.1f}/100")

if __name__ == "__main__":
    main()
