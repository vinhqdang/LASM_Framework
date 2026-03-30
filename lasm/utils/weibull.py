from scipy.stats import weibull_min
import numpy as np

def fit_weibull(data: np.ndarray):
    """Fits Webull distribution, returns shape and scale parameters."""
    if len(data) < 10:
        # Fallback to exponential
        return 1.0, np.mean(data)
    
    shape, loc, scale = weibull_min.fit(data, floc=0)
    return shape, scale

def sample_weibull(shape: float, scale: float, size: int = 1):
    return weibull_min.rvs(shape, loc=0, scale=scale, size=size)
