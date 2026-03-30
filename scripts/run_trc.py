import sys
from datetime import datetime
from lasm import LASMEvaluator

def main():
    print("Running TRC Evaluator CLI...")
    evaluator = LASMEvaluator()
    t0 = datetime(2024, 9, 1)
    res = evaluator.compute_trc("LlamaGuard3", t0, 12, retrospective=True)
    print(f"DHL: {res.DHL} months, DR: {res.DR:.4f} SASR/month")

if __name__ == "__main__":
    main()
