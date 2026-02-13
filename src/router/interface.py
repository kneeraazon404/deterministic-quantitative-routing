from typing import Any, Dict, List, Literal, Optional, Protocol

from pydantic import BaseModel, Field


class FunctionCall(BaseModel):
    """
    Represents a single function call in the execution blueprint.
    """

    function_name: str
    args: Dict[str, Any] = Field(default_factory=dict)
    weight: float = 1.0  # For weighted combinations


class ExecutionBlueprint(BaseModel):
    """
    Structured plan for executing the user's intent.
    """

    steps: List[FunctionCall]
    composition: Literal["AND", "OR", "XOR", "AVERAGE", "SUM"] = "AND"
    timeframe: str = "1d"  # Default to daily
    assets: List[str] = Field(default_factory=list)
    description: str = ""  # Explanation of the plan


class SemanticRouter(Protocol):
    """
    Protocol for the Semantic Routing Layer.
    """

    def parse_intent(self, query: str) -> ExecutionBlueprint:
        """
        Parses a natural language query into an Execution Blueprint.
        """
        ...
