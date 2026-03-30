import numpy as np
from sklearn.metrics import cohen_kappa_score

def cohen_kappa(y1: list, y2: list) -> float:
    """
    Computes Cohen's kappa for an inter-rater agreement.
    Used for verifying the credibility of SASR per Algorithm 3.
    """
    if len(y1) == 0 or len(y2) == 0:
        return 0.0
    return float(cohen_kappa_score(y1, y2))
