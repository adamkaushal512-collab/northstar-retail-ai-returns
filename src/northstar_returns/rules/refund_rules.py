from typing import List

from northstar_returns.domain.models import (
    InvestigationFinding,
    PaymentEvidence,
    RefundStatus,
    ReturnEvidence,
    ReturnStatus,
    Severity,
)


def evaluate_refund_state(
    return_case: ReturnEvidence,
    payment: PaymentEvidence,
) -> List[InvestigationFinding]:
    findings: List[InvestigationFinding] = []

    if (
        return_case.status == ReturnStatus.COMPLETED
        and payment.refund_status == RefundStatus.FAILED
    ):
        findings.append(
            InvestigationFinding(
                code="REFUND_STATE_CONFLICT",
                severity=Severity.CRITICAL,
                summary=(
                    "Returns system reports the return as completed, "
                    "but the payment system reports the refund as failed."
                ),
                evidence_sources=["Returns", "Payments"],
            )
        )

    if return_case.refund_amount != payment.refund_amount:
        findings.append(
            InvestigationFinding(
                code="REFUND_AMOUNT_MISMATCH",
                severity=Severity.CRITICAL,
                summary="Return and payment systems disagree on refund amount.",
                evidence_sources=["Returns", "Payments"],
            )
        )

    return findings
