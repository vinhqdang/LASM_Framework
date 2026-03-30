import sys
from lasm import LASMEvaluator

def main():
    print("Running SASR Evaluator CLI...")
    evaluator = LASMEvaluator()
    res = evaluator.compute_sasr("GCG", "NeMoGuardrails", "harmbench_200", "B_mid")
    print(f"SASR: {res.SASR_score:.3f}, credible: {res.credible}")

if __name__ == "__main__":
    main()
