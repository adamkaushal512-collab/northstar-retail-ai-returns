from northstar_returns.ai.explainer import explain
from northstar_returns.ai.models import AgentRequest, Explanation
from northstar_returns.ai.validation import validate_explanation
from northstar_returns.orchestration.investigation import RefundInvestigationService

class InvestigationAgent:
    """Exactly one approved read-only investigation; no refund write capability."""
    ALLOWED_TOOLS = frozenset({"investigate_refund"})
    MAX_TOOL_CALLS = 1

    def __init__(self, investigation: RefundInvestigationService | None = None):
        self.investigation = investigation if investigation is not None else RefundInvestigationService()

    def run(self, request: AgentRequest) -> Explanation:
        result = self.investigation.investigate(request.case_id, request.order_id)
        explanation = explain(result)
        validate_explanation(explanation, result)
        return explanation
