import numpy as np


def calculate_hamming_distance(array1: np.ndarray, array2: np.ndarray) -> int:
    """
    Calculate the Hamming distance between two binary arrays.
    Number of positions at which the corresponding symbols are different.
    """
    if len(array1) != len(array2):
        raise ValueError("Arrays must have the same length")

    return np.count_nonzero(array1 != array2)


def check_stability(d_h: int, input_len: int, threshold_pct: float = 0.01) -> bool:
    """
    Check if the Hamming distance is within the stability threshold.
    """
    return d_h <= (input_len * threshold_pct)
