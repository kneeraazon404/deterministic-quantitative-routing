import numpy as np
import pandas as pd

from src.library.core import validate_input, validate_output


def sma_crossover(
    prices: np.ndarray, short_window: int = 20, long_window: int = 50
) -> np.ndarray:
    """
    Simple Moving Average Crossover.
    Returns 1 when Short SMA > Long SMA, else 0.
    """
    validate_input(prices)

    series = pd.Series(prices)
    short_sma = series.rolling(window=short_window).mean()
    long_sma = series.rolling(window=long_window).mean()

    # Fill NaN values with initial price or 0 to maintain shape and avoid comparison issues
    short_sma = short_sma.bfill().fillna(0)
    long_sma = long_sma.bfill().fillna(0)

    regime = np.where(short_sma > long_sma, 1, 0)

    validate_output(regime, len(prices))
    return regime.astype(int)


def price_above_sma(prices: np.ndarray, window: int = 50) -> np.ndarray:
    """
    Price above SMA.
    Returns 1 when Price > SMA, else 0.
    """
    validate_input(prices)

    series = pd.Series(prices)
    sma = series.rolling(window=window).mean()
    sma = sma.bfill().fillna(0)

    regime = np.where(series > sma, 1, 0)

    validate_output(regime, len(prices))
    return regime.astype(int)
