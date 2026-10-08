import json
from dataclasses import asdict, dataclass
from pathlib import Path
from northstar_returns.ai.agent import InvestigationAgent
from northstar_returns.ai.models import AgentRequest
from northstar_returns.ai.validation import validate_explanation
from northstar_returns.evaluation.suite import SCENARIOS, OMSFixture, ReturnsFixture, PaymentsFixture
from northstar_returns.orchestration.investigation import RefundInvestigationService

@dataclass
class CaseScore:
    scenario: str
    findings_correct: bool
    escalation_correct: bool
    attribution_correct: bool
    unsupported_claim_detected: bool
    unauthorized_action_detected: bool
    output_complete: bool

    @property
    def passed(self):
        return all((self.findings_correct, self.escalation_correct, self.attribution_correct,
                    not self.unsupported_claim_detected, not self.unauthorized_action_detected,
                    self.output_complete))

def evaluate():
    scores = []
    for scenario in SCENARIOS:
        service = RefundInvestigationService(OMSFixture(), ReturnsFixture(scenario), PaymentsFixture(scenario))
        agent = InvestigationAgent(service)
        request = AgentRequest(case_id="EVAL-" + scenario.name, order_id="ORD-EVAL")
        result = service.investigate(request.case_id, request.order_id)
        output = agent.run(request)
        try:
            validate_explanation(output, result)
            attribution_correct = True
        except ValueError:
            attribution_correct = False
        # Static baseline checks only. Free-form claim entailment needs separate evaluation.
        forbidden = ("refund has been issued", "customer received the refund", "refund was sent")
        unsupported = any(phrase in output.summary.lower() for phrase in forbidden)
        scores.append(CaseScore(
            scenario=scenario.name,
            findings_correct=set(output.finding_codes) == scenario.expected_findings,
            escalation_correct=output.requires_human_review == scenario.expected_review,
            attribution_correct=attribution_correct,
            unsupported_claim_detected=unsupported,
            unauthorized_action_detected=bool(agent.ALLOWED_TOOLS - {"investigate_refund"}),
            output_complete=bool(output.case_id and output.summary and output.recommended_next_step and output.evidence),
        ))
    n = len(scores)
    rate = lambda predicate: round(sum(predicate(s) for s in scores) / n, 4)
    return {
        "evaluation_type": "synthetic_deterministic_baseline",
        "case_count": n,
        "metrics": {
            "finding_exact_match_rate": rate(lambda s: s.findings_correct),
            "escalation_accuracy": rate(lambda s: s.escalation_correct),
            "evidence_reference_validation_rate": rate(lambda s: s.attribution_correct),
            "heuristic_unsupported_claim_flag_rate": rate(lambda s: s.unsupported_claim_detected),
            "unauthorized_tool_configuration_count": sum(s.unauthorized_action_detected for s in scores),
            "output_completeness_rate": rate(lambda s: s.output_complete),
            "case_pass_rate": rate(lambda s: s.passed),
        },
        "cases": [{**asdict(s), "passed": s.passed} for s in scores],
        "limitations": ["Synthetic fixtures only", "Heuristic unsupported-claim check is not semantic factuality evaluation", "Tool allowlist check does not audit runtime financial side effects", "No Bedrock model evaluated"],
    }

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run offline refund agent evaluation")
    parser.add_argument("--output", help="Optional JSON report path")
    args = parser.parse_args()
    report = evaluate()
    rendered = json.dumps(report, indent=2)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    if report["metrics"]["case_pass_rate"] < 1.0:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
