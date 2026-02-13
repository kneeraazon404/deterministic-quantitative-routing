import numpy as np
import pandas as pd

from src.library.core import validate_input, validate_output


def bollinger_squeeze(
    prices: np.ndarray,
    window: int = 20,
    num_std: float = 2.0,
    squeeze_threshold: float = 0.05,
) -> np.ndarray:
    """
    Bollinger Band Squeeze.
    Returns 1 when Bandwidth < Threshold, indicating low volatility consolidation.
    """
    validate_input(prices)

    series = pd.Series(prices)
    sma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()

    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)

    bandwidth = (upper_band - lower_band) / sma
    bandwidth = bandwidth.fillna(1.0)  # Avoid false positives at start

    regime = np.where(bandwidth < squeeze_threshold, 1, 0)

    validate_output(regime, len(prices))
    return regime.astype(int)


def atr_expansion(prices: np.ndarray, window: int = 14) -> np.ndarray:
    """
    ATR Expansion.
    (Approximation using High-Low from Close prices as we only have Close prices in the interface)
    Returns 1 when Volatility (std dev) is rising above its SMA.
    """
    validate_input(prices)

    series = pd.Series(prices)
    # Using rolling std dev as proxy for ATR since we only have close prices
    volatility = series.pct_change().rolling(window=window).std()
    volatility_sma = volatility.rolling(window=window * 2).mean()

    volatility = volatility.fillna(0)
    volatility_sma = volatility_sma.fillna(0)

    regime = np.where(volatility > volatility_sma, 1, 0)

    validate_output(regime, len(prices))
    return regime.astype(int)
