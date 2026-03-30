import sys
from datetime import datetime
from lasm import LASMEvaluator

def main():
    print("Running Full LASM Evaluation...")
    evaluator = LASMEvaluator()
    system = evaluator.load_system("tests/fixtures/sample_systems.json")
    time_now = datetime.now()
    
    las = evaluator.compute_las(system, time_now, "B_mid")
    sasr = evaluator.compute_sasr("GCG", "NeMoGuardrails", "harmbench_200", "B_mid")
    trc = evaluator.compute_trc("LlamaGuard3", datetime(2024, 9, 1), 12, retrospective=True)
    eas = evaluator.compute_eas(system, time_now, "B_mid", "criminal")
    adt = evaluator.compute_adt("LlamaGuard3", "criminal", system, (0.5, 5.0))
    
    report = evaluator.generate_report(las, sasr, trc, eas, adt)
    report.to_latex("evaluation_report.tex")
    print("Full evaluation completed. Report generated at evaluation_report.tex")

if __name__ == "__main__":
    main()
