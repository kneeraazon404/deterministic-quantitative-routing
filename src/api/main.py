from fastapi import FastAPI, HTTPException

from src.api.models import QueryRequest, RegimeResponse
from src.orchestrator.engine import Orchestrator
from src.router.mock_router import MockSemanticRouter

app = FastAPI(
    title="Quant Library Orchestrator",
    description="Deterministic Quantitative Routing API",
    version="1.0.0",
)

# dependency injection (simplified)
router = MockSemanticRouter()
orchestrator = Orchestrator(router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@app.post("/query", response_model=RegimeResponse)
async def query_endpoint(request: QueryRequest):
    """
    Process a natural language query to generate a quantitative regime.
    """
    try:
        if request.recursive_stability:
            result = orchestrator.run_until_stable(
                request.query, max_iterations=request.max_iterations
            )
        else:
            result = orchestrator.execute(request.query)

        return RegimeResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
