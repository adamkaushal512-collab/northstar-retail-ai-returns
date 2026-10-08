# Phase 11 — AI / Agent Build

## Objective
Implement a bounded, evidence-grounded, read-only agent workflow over the Phase 10 enterprise integration foundation.

## Implemented
- Agent request and explanation schemas using Pydantic.
- One allowlisted investigation tool and a maximum of one tool call.
- Deterministic explanation grounded in OMS, Returns, and Payments evidence.
- Evidence references identifying source, record, and field.
- Post-generation validation of case, finding codes, references, recommendation, and human review requirement.
- `POST /agent/investigate` endpoint with existing correlation-ID middleware.
- Automated tests for normal flow, unsupported references, missing orders, and the read-only tool boundary.

## Security and operational boundaries
The workflow cannot issue refunds, override policy, or approve financial actions. A failed refund requires human review. The agent does not infer successful payment from a completed return.

## Important limitation
This is a **deterministic agent scaffold**, not an LLM or Amazon Bedrock implementation. No model is invoked, no RAG index is queried, and no production enterprise data is accessed. An optional Bedrock-backed generator, approved policy retrieval, prompt governance, and model-output evaluation remain future engineering tasks.

## Verification
Run `python -m pip install -e ".[dev]"` and `python -m pytest -v`.

For manual API testing, run `uvicorn northstar_returns.api.app:app --reload` and POST `{"case_id":"CASE-1","order_id":"ORD-1001"}` to `/agent/investigate`.

## Next phase
Phase 12 — Evaluation: define datasets and measure correctness, attribution, escalation behavior, and failure rates. Real LLM evaluation will require a model-backed implementation.
