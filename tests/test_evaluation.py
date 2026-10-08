from northstar_returns.evaluation.runner import evaluate
from northstar_returns.evaluation.suite import SCENARIOS

def test_six_synthetic_scenarios():
    assert len(SCENARIOS) == 6

def test_baseline_findings_and_escalation():
    report = evaluate()
    assert report["metrics"]["finding_exact_match_rate"] == 1.0
    assert report["metrics"]["escalation_accuracy"] == 1.0
    assert report["metrics"]["case_pass_rate"] == 1.0

def test_attribution_and_read_only_configuration():
    report = evaluate()
    assert report["metrics"]["evidence_reference_validation_rate"] == 1.0
    assert report["metrics"]["unauthorized_tool_configuration_count"] == 0
    assert all(case["output_complete"] for case in report["cases"])

def test_report_is_explicitly_limited():
    report = evaluate()
    assert report["evaluation_type"] == "synthetic_deterministic_baseline"
    assert any("No Bedrock" in item for item in report["limitations"])
