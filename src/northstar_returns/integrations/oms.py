from northstar_returns.domain.models import OrderEvidence


class MockOMS:
    def get_order(self, order_id: str) -> OrderEvidence:
        if order_id != "ORD-1001":
            raise KeyError(f"Order not found: {order_id}")

        return OrderEvidence(
            order_id="ORD-1001",
            customer_id="CUS-501",
            total_amount=149.99,
            payment_transaction_id="PAY-7001",
        )
