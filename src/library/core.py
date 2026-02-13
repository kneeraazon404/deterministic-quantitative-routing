from typing import Protocol
import numpy as np

class RegimeFunction(Protocol):
    """
    Protocol for all frozen quantitative functions.
    
    Contract:
    - Input: 1D array of prices (float)
    - Output: 1D array of binary states (int) {0, 1} of the same length
    """
    def __call__(self, prices: np.ndarray) -> np.ndarray:
        ...

def validate_input(prices: np.ndarray) -> None:
    """
    Validates input price array.
    """
    if not isinstance(prices, np.ndarray):
        raise TypeError("Input must be a numpy array")
    if prices.ndim != 1:
        raise ValueError("Input must be a 1D array")
    if not np.issubdtype(prices.dtype, np.floating) and not np.issubdtype(prices.dtype, np.integer):
        raise TypeError("Input array must contain numeric values")
    if np.any(np.isnan(prices)) or np.any(np.isinf(prices)):
        raise ValueError("Input array contains NaN or Inf values")
    if len(prices) < 2:
        raise ValueError("Input array must have at least 2 data points")

def validate_output(result: np.ndarray, input_len: int) -> None:
    """
    Validates output regime array.
    """
    if not isinstance(result, np.ndarray):
        raise TypeError("Output must be a numpy array")
    if result.ndim != 1:
        raise ValueError("Output must be a 1D array")
    if len(result) != input_len:
        raise ValueError(f"Output length ({len(result)}) does not match input length ({input_len})")
    if not np.all(np.isin(result, [0, 1])):
        raise ValueError("Output must contain only binary values (0 or 1)")
