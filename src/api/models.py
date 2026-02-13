from typing import Any, List, Optional

from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    recursive_stability: bool = False
    max_iterations: int = 10


class RegimeResponse(BaseModel):
    regime: List[int]
    blueprint: dict
    provenance: str
    iterations: Optional[int] = None
    initial_regime: Optional[List[int]] = None
