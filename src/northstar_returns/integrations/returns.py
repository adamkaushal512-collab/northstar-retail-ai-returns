from northstar_returns.domain.models import ReturnEvidence, ReturnStatus


class MockReturnsSystem:
    def get_return(self, order_id: str) -> ReturnEvidence:
        if order_id != "ORD-1001":
            raise KeyError(f"Return not found for order: {order_id}")

        return ReturnEvidence(
            return_id="RET-2001",
            order_id="ORD-1001",
            status=ReturnStatus.COMPLETED,
            refund_amount=149.99,
        )
