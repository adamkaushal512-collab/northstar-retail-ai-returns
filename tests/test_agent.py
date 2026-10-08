import pytest
from fastapi.testclient import TestClient
from northstar_returns.ai.agent import InvestigationAgent
from northstar_returns.ai.models import AgentRequest, EvidenceReference
from northstar_returns.ai.explainer import explain
from northstar_returns.ai.validation import validate_explanation
from northstar_returns.api.app import app
from northstar_returns.orchestration.investigation import RefundInvestigationService

def test_grounded_explanation():
    result = InvestigationAgent().run(AgentRequest(case_id="CASE-1", order_id="ORD-1001"))
    assert result.generation_mode == "deterministic"
    assert "REFUND_STATE_CONFLICT" in result.finding_codes
    assert result.requires_human_review is True
    assert {e.source for e in result.evidence} == {"OMS", "Returns", "Payments"}
    assert "Do not issue a second refund" in result.recommended_next_step

def test_validation_accepts_grounded_output():
    result = RefundInvestigationService().investigate("CASE-1", "ORD-1001")
    validate_explanation(explain(result), result)

def test_fabricated_reference_rejected():
    result = RefundInvestigationService().investigate("CASE-1", "ORD-1001")
    output = explain(result)
    output.evidence.append(EvidenceReference(source="Payments", record_id="FAKE", field="refund_status"))
    with pytest.raises(ValueError, match="Unsupported"):
        validate_explanation(output, result)

def test_agent_endpoint():
    response = TestClient(app).post("/agent/investigate", json={"case_id": "CASE-1", "order_id": "ORD-1001"})
    assert response.status_code == 200
    assert response.json()["generation_mode"] == "deterministic"

def test_no_write_tools():
    assert InvestigationAgent.ALLOWED_TOOLS == frozenset({"investigate_refund"})

def test_missing_order_returns_404():
    response = TestClient(app).post("/agent/investigate", json={"case_id": "CASE-1", "order_id": "MISSING"})
    assert response.status_code == 404
