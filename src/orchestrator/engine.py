import numpy as np

from src.library.momentum import rsi_overbought, rsi_oversold
from src.library.trend import price_above_sma, sma_crossover
from src.library.volatility import atr_expansion, bollinger_squeeze
from src.orchestrator.hooks import LifecycleHooks
from src.orchestrator.stability import calculate_hamming_distance, check_stability
from src.router.interface import ExecutionBlueprint, SemanticRouter
from src.utils.data_loader import load_data
from src.utils.smoothing import smooth_regime


class Orchestrator:
    """
    Kernel-Mode Orchestrator: Coordinates execution of frozen functions.
    """

    def __init__(self, router: SemanticRouter):
        self.router = router
        self.registry = {
            "sma_crossover": sma_crossover,
            "price_above_sma": price_above_sma,
            "bollinger_squeeze": bollinger_squeeze,
            "atr_expansion": atr_expansion,
            "rsi_overbought": rsi_overbought,
            "rsi_oversold": rsi_oversold,
        }

    def execute(self, query: str) -> dict:
        """
        Main entry point: Parse intent -> Generate Blueprint -> Execute.
        """
        blueprint = self.router.parse_intent(query)

        # Determine assets (for simplicity, assume single asset first, or list)
        asset = blueprint.assets[0] if blueprint.assets else "BTC"
        prices = load_data(asset, limit=100)  # Mock data loader

        results = []
        for step in blueprint.steps:
            func = self.registry.get(step.function_name)
            if not func:
                raise ValueError(f"Function {step.function_name} not found in registry")

            # PreTool Hook
            LifecycleHooks.pre_tool_use(step.function_name, step.args, prices)

            # Execute
            try:
                # Assuming simple kwargs unpacking for now.
                # In strict "frozen" mode, args might be fixed or come from blueprint.
                res = func(prices, **step.args)
            except Exception as e:
                raise RuntimeError(f"Execution failed for {step.function_name}: {e}")

            # PostTool Hook
            LifecycleHooks.post_tool_use(step.function_name, res, len(prices))
            results.append(res)

        # Composition Logic
        final_regime = self._compose(results, blueprint.composition)

        return {
            "regime": final_regime.tolist(),
            "blueprint": blueprint.model_dump(),
            "provenance": "Executed via Quant Library Orchestrator v1.0",
        }

    def _compose(self, results: list[np.ndarray], method: str) -> np.ndarray:
        """
        Logic Gate Implementation (AND, OR, XOR, AVG).
        """
        if not results:
            return np.array([])

        if len(results) == 1:
            return results[0]

        combined = results[0]
        for i in range(1, len(results)):
            next_res = results[i]

            if method == "AND":
                combined = np.logical_and(combined, next_res)
            elif method == "OR":
                combined = np.logical_or(combined, next_res)
            elif method == "XOR":
                combined = np.logical_xor(combined, next_res)
            elif method == "AVERAGE":
                # Average is tricky for binary arrays, returns float probability
                # Just averaging 0s and 1s here
                combined = (combined + next_res) / 2.0
            elif method == "SUM":
                combined = combined + next_res
            else:
                raise ValueError(f"Unknown composition method: {method}")

        return combined.astype(int) if method != "AVERAGE" else combined

    def run_until_stable(self, query: str, max_iterations: int = 10) -> dict:
        """
        Recursive Stability Loop.
        Executing query, then iteratively applying smoothing until stable.
        """
        result = self.execute(query)
        initial_regime = np.array(result["regime"])

        history = [initial_regime]

        for k in range(max_iterations):
            prev_regime = history[-1]
            next_regime = smooth_regime(prev_regime)

            # Check stability
            d_h = calculate_hamming_distance(prev_regime, next_regime)
            is_stable = check_stability(d_h, len(prev_regime))

            history.append(next_regime)

            # Stop Hook
            if LifecycleHooks.stop_hook(k + 1, max_iterations, d_h):
                break

            if is_stable:
                break

        return {
            "regime": history[-1].tolist(),
            "iterations": len(history) - 1,
            "initial_regime": initial_regime.tolist(),
            "blueprint": result["blueprint"],
            "provenance": f"Recursive execution stable after {len(history)-1} iterations",
        }
