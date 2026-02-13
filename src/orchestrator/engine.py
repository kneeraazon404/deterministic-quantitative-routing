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
        Support for Multi-Asset Cross-Sectional Execution and Synthetic Positions.
        """
        blueprint = self.router.parse_intent(query)
        assets = blueprint.assets if blueprint.assets else ["BTC"]

        # 1. Resolve Data (Synthetic or Direct)
        # If asset is "A-B", we compute difference.
        # For simplicity, if ANY asset string contains arithmetic, we treat it as synthetic.
        # Real implementation would have a robust parser.
        final_results = []

        for asset in assets:
            if "-" in asset and " " not in asset:  # Simple A-B check
                parts = asset.split("-")
                p1 = load_data(parts[0], limit=100)
                p2 = load_data(parts[1], limit=100)
                prices = p1 - p2  # Synthetic Position
            else:
                prices = load_data(asset, limit=100)

            asset_results = []
            for step in blueprint.steps:
                func = self.registry.get(step.function_name)
                if not func:
                    raise ValueError(
                        f"Function {step.function_name} not found in registry"
                    )

                LifecycleHooks.pre_tool_use(step.function_name, step.args, prices)
                try:
                    res = func(prices, **step.args)
                except Exception as e:
                    raise RuntimeError(
                        f"Execution failed for {step.function_name}: {e}"
                    )
                LifecycleHooks.post_tool_use(step.function_name, res, len(prices))
                asset_results.append(res)

            # Compose per asset (Vertical Composition)
            # If multiple steps, we verify how to combine them.
            # Usually strict pipeline implies sequential or composed signal.
            # Here we assume the blueprint composition applies to the Steps *Result*.
            # But wait, blueprint.composition is for combining the final results?
            # Let's clarify: Blueprint steps -> [Result1, Result2].
            # Compose -> Final Result for Asset A.

            # If we have multiple assets, we might want to return per-asset OR aggregated.
            # "Cross-sectional sum" implies aggregating across assets.

            per_asset_regime = self._compose(asset_results, blueprint.composition)
            final_results.append(per_asset_regime)

        # 2. Cross-Sectional Aggregation (if multiple assets)
        # If > 1 asset, we need a specific aggregation strategy.
        # For "Breadth", we SUM. For others, maybe just list?
        # The Orchestration logic needs to know if it's a Breadth query vs Portfolio query.
        # For this "Thin Agent", we'll infer from composition:
        # If composition is SUM/AVG and multiple assets -> Cross-Sectional.
        # Otherwise, we might default to returning the first or list.
        # The prompt says "Cross-sectional sum logic gate".

        if len(final_results) > 1:
            # We treat the list of asset regimes as inputs to compose
            final_regime = self._compose(final_results, blueprint.composition)
        else:
            final_regime = final_results[0]

        return {
            "regime": final_regime.tolist(),
            "blueprint": blueprint.model_dump(),
            "provenance": "Executed via Quant Library Orchestrator v1.1 (Multi-Asset)",
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
