import pytest

from src.orchestrator.engine import Orchestrator
from src.router.mock_router import MockSemanticRouter


def test_orchestrator_trend_query():
    router = MockSemanticRouter()
    orchestrator = Orchestrator(router)

    result = orchestrator.execute("Show me the trend of BTC")
    assert "regime" in result
    assert "blueprint" in result
    assert len(result["regime"]) == 100
    assert (
        result["blueprint"]["description"]
        == "Trend following strategy using SMA Crossover (20/50)"
    )


def test_recursive_stability():
    router = MockSemanticRouter()
    orchestrator = Orchestrator(router)

    # "Run until stable" implies recursive loop
    result = orchestrator.run_until_stable("Show me the trend of BTC", max_iterations=5)

    assert "regime" in result
    assert "iterations" in result
    assert result["iterations"] >= 0
    assert len(result["regime"]) == 100
