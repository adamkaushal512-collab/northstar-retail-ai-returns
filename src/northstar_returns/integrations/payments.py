from northstar_returns.domain.models import PaymentEvidence, RefundStatus


class MockPayments:
    def get_refund_status(self, payment_transaction_id: str) -> PaymentEvidence:
        if payment_transaction_id != "PAY-7001":
            raise KeyError(
                f"Payment transaction not found: {payment_transaction_id}"
            )

        return PaymentEvidence(
            payment_transaction_id="PAY-7001",
            refund_id="REF-9001",
            refund_status=RefundStatus.FAILED,
            refund_amount=149.99,
            failure_reason="Processor rejected refund request",
        )
