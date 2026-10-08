from dataclasses import dataclass
from northstar_returns.domain.models import OrderEvidence, ReturnEvidence, PaymentEvidence, ReturnStatus, RefundStatus

@dataclass(frozen=True)
class Scenario:
    name: str
    return_status: ReturnStatus
    refund_status: RefundStatus
    return_amount: float
    payment_amount: float
    expected_findings: frozenset[str]
    expected_review: bool

SCENARIOS = (
    Scenario("failed_refund", ReturnStatus.COMPLETED, RefundStatus.FAILED, 149.99, 149.99, frozenset({"REFUND_STATE_CONFLICT"}), True),
    Scenario("amount_mismatch", ReturnStatus.COMPLETED, RefundStatus.COMPLETED, 149.99, 129.99, frozenset({"REFUND_AMOUNT_MISMATCH"}), True),
    Scenario("both_conflicts", ReturnStatus.COMPLETED, RefundStatus.FAILED, 149.99, 129.99, frozenset({"REFUND_STATE_CONFLICT", "REFUND_AMOUNT_MISMATCH"}), True),
    Scenario("normal_completed", ReturnStatus.COMPLETED, RefundStatus.COMPLETED, 149.99, 149.99, frozenset(), False),
    Scenario("pending_refund", ReturnStatus.APPROVED, RefundStatus.PENDING, 149.99, 149.99, frozenset(), False),
    Scenario("open_return", ReturnStatus.OPEN, RefundStatus.NOT_FOUND, 149.99, 149.99, frozenset(), False),
)

class OMSFixture:
    def get_order(self, order_id):
        return OrderEvidence(order_id=order_id, customer_id="SYNTHETIC", total_amount=149.99, payment_transaction_id="PAY-EVAL")

class ReturnsFixture:
    def __init__(self, scenario): self.scenario = scenario
    def get_return(self, order_id):
        return ReturnEvidence(return_id="RET-EVAL", order_id=order_id, status=self.scenario.return_status, refund_amount=self.scenario.return_amount)

class PaymentsFixture:
    def __init__(self, scenario): self.scenario = scenario
    def get_refund_status(self, payment_transaction_id):
        return PaymentEvidence(payment_transaction_id=payment_transaction_id, refund_status=self.scenario.refund_status, refund_amount=self.scenario.payment_amount)
