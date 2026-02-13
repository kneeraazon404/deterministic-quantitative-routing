import numpy as np
import pytest

from src.library.momentum import rsi_overbought, rsi_oversold
from src.library.trend import price_above_sma, sma_crossover
from src.library.volatility import atr_expansion, bollinger_squeeze


@pytest.fixture
def sample_prices():
    # Simple sine wave + linear trend
    x = np.linspace(0, 100, 200)
    return 100 + x + 10 * np.sin(x)


def test_sma_crossover(sample_prices):
    regime = sma_crossover(sample_prices, short_window=10, long_window=20)
    assert len(regime) == len(sample_prices)
    assert np.all(np.isin(regime, [0, 1]))
    # Basic logic check: if prices rising, short SMA > long SMA eventually
    assert regime[-1] == 1


def test_bollinger_squeeze():
    # Constant prices -> 0 std dev -> squeeze
    prices = np.ones(100) * 100
    regime = bollinger_squeeze(prices, squeeze_threshold=0.1)
    assert np.all(regime[20:] == 1)  # Squeeze should be active after window


def test_rsi_overbought():
    # Rapidly increasing prices -> high RSI
    prices = np.array([100 * (1.1**i) for i in range(50)])
    regime = rsi_overbought(prices, threshold=70)
    assert regime[-1] == 1


def test_rsi_oversold():
    # Rapidly decreasing prices -> low RSI
    prices = np.array([100 * (0.9**i) for i in range(50)])
    regime = rsi_oversold(prices, threshold=30)
    assert regime[-1] == 1
