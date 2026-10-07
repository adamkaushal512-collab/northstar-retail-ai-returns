from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from northstar_returns.orchestration.investigation import (
    RefundInvestigationService,
)

app = FastAPI(
    title="NorthStar Returns Investigation API",
    version="0.1.0",
    description="Phase 9 rapid prototype for refund exception investigation.",
)

service = RefundInvestigationService()


class InvestigationRequest(BaseModel):
    case_id: str
    order_id: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/investigations")
def investigate(request: InvestigationRequest):
    try:
        return service.investigate(
            case_id=request.case_id,
            order_id=request.order_id,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
