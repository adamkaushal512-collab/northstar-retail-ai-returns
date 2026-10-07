from northstar_returns.domain.models import (
    PaymentEvidence,
    RefundStatus,
    ReturnEvidence,
    ReturnStatus,
)
from northstar_returns.rules.refund_rules import evaluate_refund_state


def test_detects_refund_state_conflict():
    return_case = ReturnEvidence(
        return_id="RET-1",
        order_id="ORD-1",
        status=ReturnStatus.COMPLETED,
        refund_amount=100.0,
    )
    payment = PaymentEvidence(
        payment_transaction_id="PAY-1",
        refund_id="REF-1",
        refund_status=RefundStatus.FAILED,
        refund_amount=100.0,
        failure_reason="processor failure",
    )

    findings = evaluate_refund_state(return_case, payment)

    assert len(findings) == 1
    assert findings[0].code == "REFUND_STATE_CONFLICT"


def test_detects_refund_amount_mismatch():
    return_case = ReturnEvidence(
        return_id="RET-1",
        order_id="ORD-1",
        status=ReturnStatus.COMPLETED,
        refund_amount=100.0,
    )
    payment = PaymentEvidence(
        payment_transaction_id="PAY-1",
        refund_id="REF-1",
        refund_status=RefundStatus.COMPLETED,
        refund_amount=90.0,
    )

    findings = evaluate_refund_state(return_case, payment)

    assert any(f.code == "REFUND_AMOUNT_MISMATCH" for f in findings)
