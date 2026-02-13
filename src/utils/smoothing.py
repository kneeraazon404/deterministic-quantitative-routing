import numpy as np


def smooth_regime(regime: np.ndarray, window: int = 3) -> np.ndarray:
    """
    Simple majority voting smoothing to reduce noise.
    """
    if len(regime) < window:
        return regime

    result = np.copy(regime)
    for i in range(len(regime)):
        start = max(0, i - window // 2)
        end = min(len(regime), i + window // 2 + 1)
        # Majority vote
        if np.sum(regime[start:end]) > (end - start) / 2:
            result[i] = 1
        else:
            result[i] = 0

    return result
