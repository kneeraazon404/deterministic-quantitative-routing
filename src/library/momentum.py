import numpy as np
import pandas as pd

from src.library.core import validate_input, validate_output


def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """
    Helper to calculate RSI.
    """
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)  # Neutral RSI at start


def rsi_overbought(
    prices: np.ndarray, period: int = 14, threshold: int = 70
) -> np.ndarray:
    """
    RSI Overbought.
    Returns 1 when RSI > Threshold (Overbought), else 0.
    """
    validate_input(prices)

    rsi = calculate_rsi(pd.Series(prices), period)
    regime = np.where(rsi > threshold, 1, 0)

    validate_output(regime, len(prices))
    return regime.astype(int)


def rsi_oversold(
    prices: np.ndarray, period: int = 14, threshold: int = 30
) -> np.ndarray:
    """
    RSI Oversold.
    Returns 1 when RSI < Threshold (Oversold), else 0.
    """
    validate_input(prices)

    rsi = calculate_rsi(pd.Series(prices), period)
    regime = np.where(rsi < threshold, 1, 0)

    validate_output(regime, len(prices))
    return regime.astype(int)
