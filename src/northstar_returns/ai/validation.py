from northstar_returns.ai.models import Explanation
from northstar_returns.domain.models import InvestigationResult

def validate_explanation(explanation: Explanation, result: InvestigationResult) -> None:
    if explanation.case_id != result.case_id:
        raise ValueError("Case mismatch")
    if set(explanation.finding_codes) != {finding.code for finding in result.findings}:
        raise ValueError("Finding mismatch")
    allowed = {
        ("OMS", result.order.order_id, "payment_transaction_id"),
        ("Returns", result.return_case.return_id, "status"),
        ("Payments", result.payment.payment_transaction_id, "refund_status"),
    }
    if not explanation.evidence or any((e.source, e.record_id, e.field) not in allowed for e in explanation.evidence):
        raise ValueError("Unsupported evidence reference")
    if explanation.recommended_next_step != result.recommended_next_step:
        raise ValueError("Unapproved recommendation")
    if explanation.requires_human_review != (bool(result.findings) or result.human_approval_required):
        raise ValueError("Human review requirement mismatch")
