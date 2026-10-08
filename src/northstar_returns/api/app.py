from uuid import uuid4
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from northstar_returns.ai.agent import InvestigationAgent
from northstar_returns.ai.models import AgentRequest, Explanation
from northstar_returns.integrations.errors import IntegrationError
from northstar_returns.orchestration.investigation import RefundInvestigationService

app = FastAPI(title="NorthStar Returns Investigation API", version="0.3.0")
service = RefundInvestigationService()
agent = InvestigationAgent(service)

class InvestigationRequest(BaseModel):
    case_id: str
    order_id: str

@app.middleware("http")
async def correlation_id(request: Request, call_next):
    supplied = request.headers.get("X-Correlation-ID")
    value = supplied if supplied and len(supplied) <= 128 and supplied.isascii() and all(c.isprintable() for c in supplied) else str(uuid4())
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = value
    return response

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.post("/investigations")
def investigate(request: InvestigationRequest):
    try:
        return service.investigate(case_id=request.case_id, order_id=request.order_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Requested record not found")
    except IntegrationError:
        raise HTTPException(status_code=503, detail="Enterprise evidence unavailable or invalid")

@app.post("/agent/investigate", response_model=Explanation)
def agent_investigate(request: AgentRequest):
    try:
        return agent.run(request)
    except KeyError:
        raise HTTPException(status_code=404, detail="Requested record not found")
    except IntegrationError:
        raise HTTPException(status_code=503, detail="Enterprise evidence unavailable or invalid")
