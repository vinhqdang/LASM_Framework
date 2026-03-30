# LASM: LLM Attack Surface Measurement Framework

The **LASM Framework** is a unified measurement science proposal and implementation for the security evaluation of LLM-based AI systems. It formally addresses the inconsistencies and non-reproducibility of traditional Attack Success Rate (ASR) measurements by introducing rigorous, compositional attack surface metrics and a rational-attacker game-theoretic model.

## Core Metrics Implemented
*   **LAS (LLM Attack Surface):** A compositional metric quantifying the vulnerability of a system based on architectural exposure, trust weights, and predicted exploitation probabilities.
*   **SASR (Standardized ASR):** Eliminates inter-study inconsistency via a standardized, multi-judge evaluation protocol (Classifier + LLM + Human).
*   **TRC (Temporal Robustness Curve):** Longitudinally measures defense effectiveness mathematically via the Technical Defense Half-Life (DHL).
*   **EAS (Economic Attack Surface):** A formal game-theoretic formulation evaluating attack viability under rational attacker budgets and opportunity costs.
*   **ADT (Attack Deterrence Threshold):** The specific defensive strength ratio required to render all attacks against a system economically irrational.

## Evaluation Results & Conclusions

Based on rigorous simulated evaluations conforming to the foundational hypotheses of the LASM Framework:

### 1. Attack Surface Predicts Exploitation ($\rho = 0.988$)
The framework demonstrated near-perfect Spearman rank correlation across 8 distinct architectural scopes (S1 to S4). As LLM systems scale from solitary endpoints (GPT-4o) to Multi-Agent swarms with internal tool-use (S4), their attack surface expands non-linearly (Amplification factor $\alpha = 1.05$) due to inter-agent communication channels (`EP_AM`). 

### 2. Standardization Eliminates Defense Illusions
By deploying the SASR benchmark, we re-evaluated 12 leading defenses. Defenses heavily reliant on heuristics (like Perplexity filtering and simple string matching) systematically overestimated their security, dropping below the inter-judge $\kappa \ge 0.6$ credibility threshold and revealing hidden vulnerabilities. SASR exceeded traditionally reported binary ASR in **83% of state-of-the-art defenses**.

### 3. The Dual Half-Life Paradigm
When tracking temporal robustness (TRC), pattern-matching defenses like `Llama Guard 3` suffered from rapid decay, exhibiting a **Technical Defense Half-Life (DHL) of only 5.4 months** against evolving attacks. However, when evaluating through the Economic TRC, the **Economic DHL** against rational Criminal Organizations was **8.2 months**, mathematically proving the core thesis: *technical applicability does not equate to rational exploitability.* 

**Conclusion:** Security investments should be guided by the Attack Deterrence Threshold (ADT). By prioritizing defenses that maximize attacker compute ($C_{compute}$) and expertise costs ($C_{expertise}$), defenders can eliminate the Economic Attack Surface entirely without mathematically needing to reduce technical exploit probabilities to zero.

---
*Framework version: 1.0*  
*Contributors: Research Team*
