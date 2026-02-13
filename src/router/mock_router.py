from typing import List

from src.router.interface import ExecutionBlueprint, FunctionCall, SemanticRouter


class MockSemanticRouter(SemanticRouter):
    """
    A deterministic router for testing without an LLM.
    """

    def parse_intent(self, query: str) -> ExecutionBlueprint:
        query = query.lower()

        if "trend" in query:
            return ExecutionBlueprint(
                steps=[
                    FunctionCall(
                        function_name="sma_crossover",
                        args={"short_window": 20, "long_window": 50},
                    )
                ],
                composition="AND",
                timeframe="1d",
                assets=["BTC"],
                description="Trend following strategy using SMA Crossover (20/50)",
            )
        elif "volatility" in query or "squeeze" in query:
            return ExecutionBlueprint(
                steps=[
                    FunctionCall(
                        function_name="bollinger_squeeze",
                        args={"window": 20, "num_std": 2.0},
                    )
                ],
                composition="AND",
                timeframe="1d",
                assets=["BTC"],
                description="Volatility strategy using Bollinger Band Squeeze",
            )
        elif "momentum" in query or "rsi" in query:
            return ExecutionBlueprint(
                steps=[
                    FunctionCall(
                        function_name="rsi_overbought", args={"threshold": 70}
                    ),
                    FunctionCall(function_name="rsi_oversold", args={"threshold": 30}),
                ],
                composition="OR",  # Trigger on either OB or OS
                timeframe="1d",
                assets=["BTC"],
                description="Momentum strategy using RSI (Overbought or Oversold)",
            )
        elif "combine" in query:
            return ExecutionBlueprint(
                steps=[
                    FunctionCall(function_name="sma_crossover"),
                    FunctionCall(function_name="rsi_oversold"),
                ],
                composition="AND",
                timeframe="1d",
                assets=["BTC"],
                description="Combined strategy: SMA Crossover AND RSI Oversold",
            )
        else:
            # Default fallback
            return ExecutionBlueprint(
                steps=[FunctionCall(function_name="sma_crossover")],
                composition="AND",
                timeframe="1d",
                assets=["BTC"],
                description="Default: SMA Crossover",
            )
