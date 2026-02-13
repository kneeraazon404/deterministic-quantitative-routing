import numpy as np
import pytest

from src.orchestrator.engine import Orchestrator
from src.router.interface import ExecutionBlueprint, FunctionCall, SemanticRouter


class MockRouter(SemanticRouter):
    def parse_intent(self, query: str) -> ExecutionBlueprint:
        if "synthetic" in query:
            return ExecutionBlueprint(
                steps=[
                    FunctionCall(function_name="price_above_sma", args={"window": 10})
                ],
                composition="AND",
                assets=["A-B"],
            )
        elif "breadth" in query:
            return ExecutionBlueprint(
                steps=[
                    FunctionCall(function_name="price_above_sma", args={"window": 10})
                ],
                composition="SUM",
                assets=["A", "B", "C"],
            )
        return ExecutionBlueprint(steps=[], composition="AND", assets=[])


def test_synthetic_execution():
    router = MockRouter()
    orchestrator = Orchestrator(router)
    # The data loader is mock, so A-B should just work as random-random
    result = orchestrator.execute("Show me synthetic A-B")
    assert "provenance" in result
    assert result["provenance"].endswith("(Multi-Asset)")
    assert len(result["regime"]) == 100


def test_breadth_execution():
    router = MockRouter()
    orchestrator = Orchestrator(router)
    # 3 assets, SUM composition.
    # Mock data loader returns random walks.
    # price_above_sma returns 0 or 1.
    # Sum should be between 0 and 3.
    result = orchestrator.execute("Show me breadth")
    regime = np.array(result["regime"])
    assert len(regime) == 100
    assert np.all(regime >= 0)
    assert np.all(regime <= 3)
