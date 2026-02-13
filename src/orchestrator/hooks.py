from typing import Any, Callable

import numpy as np

from src.library.core import validate_input, validate_output


class LifecycleHooks:
    """
    Deterministic Lifecycle Hooks for the Orchestrator.
    """

    @staticmethod
    def pre_tool_use(func_name: str, args: dict, prices: np.ndarray) -> None:
        """
        Intercept tool calls to validate input schema compliance.
        """
        try:
            validate_input(prices)
            # Add more specific validation here if needed
        except Exception as e:
            raise ValueError(f"PreToolUse Hook Failed for {func_name}: {str(e)}")

    @staticmethod
    def post_tool_use(func_name: str, result: np.ndarray, input_len: int) -> None:
        """
        Validate outputs. If a function returns non-binary values or misaligned lengths, the hook rejects the result.
        """
        try:
            validate_output(result, input_len)
        except Exception as e:
            raise ValueError(f"PostToolUse Hook Failed for {func_name}: {str(e)}")

    @staticmethod
    def stop_hook(
        iteration: int, max_iterations: int, hamming_distance: int, threshold: int = 0
    ) -> bool:
        """
        Stop Hook (Compaction Gate): Block the orchestrator from exiting if stability check has not converged.
        Returns True if should stop.
        """
        if iteration >= max_iterations:
            return True
        if hamming_distance <= threshold:
            return True
        return False
