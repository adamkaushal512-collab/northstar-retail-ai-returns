from northstar_returns.domain.models import InvestigationResult
from northstar_returns.integrations.oms import MockOMS
from northstar_returns.integrations.payments import MockPayments
from northstar_returns.integrations.returns import MockReturnsSystem
from northstar_returns.rules.refund_rules import evaluate_refund_state


class RefundInvestigationService:
    def __init__(self, oms=None, returns=None, payments=None) -> None:
        self.oms = oms if oms is not None else MockOMS()
        self.returns = returns if returns is not None else MockReturnsSystem()
        self.payments = payments if payments is not None else MockPayments()

    def investigate(self, case_id: str, order_id: str) -> InvestigationResult:
        order = self.oms.get_order(order_id)
        return_case = self.returns.get_return(order_id)
        payment = self.payments.get_refund_status(order.payment_transaction_id)

        findings = evaluate_refund_state(return_case, payment)

        if any(f.code == "REFUND_STATE_CONFLICT" for f in findings):
            recommendation = (
                "Escalate to Payments Operations for refund failure investigation. "
                "Do not issue a second refund automatically."
            )
        elif findings:
            recommendation = "Route the case for manual review."
        else:
            recommendation = "No refund-state exception detected."

        return InvestigationResult(
            case_id=case_id,
            order=order,
            return_case=return_case,
            payment=payment,
            findings=findings,
            recommended_next_step=recommendation,
            human_approval_required=False,
        )
