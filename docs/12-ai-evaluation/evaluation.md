# Phase 12 — AI Evaluation

## Objective
Measure the Phase 11 deterministic investigation agent using a reproducible synthetic dataset. This is a **baseline**, not an evaluation of a deployed LLM.

## Evaluation dataset
Six synthetic cases: failed refund, amount mismatch, both conflicts, completed refund, pending refund, and open return. Expected finding codes and human-review decisions are declared independently of the agent output.

## Measures
- Finding exact-match rate: exact equality of predicted and expected finding-code sets.
- Escalation accuracy: agreement with the expected human-review decision.
- Evidence-reference validation rate: structured reference validation against retrieved source records.
- Heuristic unsupported-claim flag rate: narrow prohibited-phrase check, **not** a comprehensive hallucination metric.
- Unauthorized tool configuration count: detects non-read-only entries in the agent tool allowlist; **not** a runtime financial action audit.
- Output completeness rate: nonempty case ID, summary, recommendation and evidence.
- Case pass rate: all per-case checks pass.

## Execute
```bash
python -m pytest -v
python -m northstar_returns.evaluation.runner --output reports/phase12-evaluation.json
```
The JSON report is generated locally; do not commit reports with customer data. All fixtures in this package are synthetic.

## Pilot target hypotheses (not achieved production metrics)
- Evidence attribution precision >=98%
- Unsupported factual claim rate <=1%
- Escalation accuracy >=98%
- Unauthorized financial actions = 0
- Audit completeness >=99%

The baseline reference-validation and heuristic metrics **must not** be substituted for production precision, semantic factuality, runtime action safety, or audit completeness. Real LLM evaluation needs human-labeled cases, multi-rater adjudication, statistical confidence intervals, production-like distribution, policy citations, and trace auditing.

## Next phase
Phase 13: Red-team / Failure Testing, including adversarial evidence, injection, missing records, and partial upstream outages.
