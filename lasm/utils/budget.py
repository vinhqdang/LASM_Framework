def compute_nqu(api_calls: int, avg_tokens: float) -> float:
    """Computes Normalized Query Units (NQU)."""
    return (api_calls * avg_tokens) / 1000.0

def get_budget_tier(nqu: float) -> str:
    if nqu <= 100:
        return "B_low"
    elif nqu <= 1000:
        return "B_mid"
    elif nqu <= 10000:
        return "B_high"
    else:
        return "B_adaptive"
