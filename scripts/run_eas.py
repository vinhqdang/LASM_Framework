import sys
from datetime import datetime
from lasm import LASMEvaluator

def main():
    print("Running EAS & ADT Evaluator CLI...")
    evaluator = LASMEvaluator()
    system = evaluator.load_system("tests/fixtures/sample_systems.json")
    
    eas_res = evaluator.compute_eas(system, datetime.now(), "B_mid", "criminal", 50000)
    print(f"EAS_norm: {eas_res.EAS_norm:.1f}/100")
    print(f"Deterrence ratio: {eas_res.deterrence_ratio:.2%}")
    
    adt_res = evaluator.compute_adt("LlamaGuard3", "criminal", system, (0.5, 5.0))
    print(f"ADT: {adt_res.ADT:.2f}x baseline defense strength")
    print(f"Technical DHL: {adt_res.DHL_tech} months")
    print(f"Economic DHL (criminal): {adt_res.DHL_econ} months")

if __name__ == "__main__":
    main()
