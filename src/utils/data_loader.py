import numpy as np
import pandas as pd


def load_data(symbol: str, timeframe: str = "1d", limit: int = 100) -> np.ndarray:
    """
    Mock data loader.
    Returns random walk data for testing.
    """
    np.random.seed(42)  # Deterministic for testing

    returns = np.random.normal(0, 0.02, limit)
    price = 100 * (1 + returns).cumprod()

    return price
