from northstar_returns.ai.models import EvidenceReference, Explanation
from northstar_returns.domain.models import InvestigationResult

def explain(result: InvestigationResult) -> Explanation:
    findings = [f.code for f in result.findings]
    if "REFUND_STATE_CONFLICT" in findings:
        summary = (
            f"Return {result.return_case.return_id} is {result.return_case.status.value}, "
            f"but payment transaction {result.payment.payment_transaction_id} "
            f"reports refund status {result.payment.refund_status.value}. "
            "Do not infer that the customer received a refund."
        )
    elif "REFUND_AMOUNT_MISMATCH" in findings:
        summary = "Returns and Payments disagree on refund amount; manual review is required."
    else:
        summary = "No supported refund exception was detected in the retrieved evidence."
    return Explanation(
        case_id=result.case_id, summary=summary, finding_codes=findings,
        evidence=[
            EvidenceReference(source="OMS", record_id=result.order.order_id, field="payment_transaction_id"),
            EvidenceReference(source="Returns", record_id=result.return_case.return_id, field="status"),
            EvidenceReference(source="Payments", record_id=result.payment.payment_transaction_id, field="refund_status"),
        ],
        recommended_next_step=result.recommended_next_step,
        requires_human_review=bool(findings) or result.human_approval_required,
    )
