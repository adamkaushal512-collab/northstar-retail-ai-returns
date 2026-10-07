from northstar_returns.orchestration.investigation import (
    RefundInvestigationService,
)


def test_investigation_reconciles_enterprise_evidence():
    service = RefundInvestigationService()

    result = service.investigate(
        case_id="CASE-3001",
        order_id="ORD-1001",
    )

    assert result.case_id == "CASE-3001"
    assert result.order.order_id == "ORD-1001"
    assert result.return_case.status.value == "COMPLETED"
    assert result.payment.refund_status.value == "FAILED"
    assert any(
        finding.code == "REFUND_STATE_CONFLICT"
        for finding in result.findings
    )
    assert "Payments Operations" in result.recommended_next_step
