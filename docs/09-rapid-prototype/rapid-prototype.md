# Phase 9 — Rapid Prototype

## Objective

Build the first executable vertical slice of the NorthStar Retail AI Returns & Refund Operations Platform.

The prototype validates the workflow before introducing production integrations, RAG, LLM reasoning, or agentic execution.

## Vertical Slice

The initial scenario represents a refund exception where enterprise systems disagree:

- OMS identifies the order and payment transaction.
- Returns reports the return as `COMPLETED`.
- Payments reports the refund as `FAILED`.
- Deterministic rules identify `REFUND_STATE_CONFLICT`.
- The orchestration service recommends escalation to Payments Operations.
- The platform explicitly avoids issuing another refund automatically.

## Components

### Domain Models

Pydantic models define typed enterprise evidence and investigation results.

### Mock Enterprise Integrations

The prototype includes mock adapters for:

- OMS
- Returns
- Payments

These simulate systems of record without requiring production credentials.

### Deterministic Rules

The rules layer detects:

- completed return + failed refund
- refund amount mismatch

Rules are deterministic because these conditions should not depend on generative AI judgment.

### Investigation Orchestration

The orchestration layer retrieves evidence, applies rules, and creates a structured investigation result.

### FastAPI

The prototype exposes:

- `GET /health`
- `POST /investigations`

### Tests

Pytest validates the rule and end-to-end investigation behavior.

## Why AI Is Not Added Yet

The purpose of Phase 9 is to prove the workflow and software boundaries.

The future AI layer will operate over structured evidence produced by this foundation rather than directly replacing deterministic business logic.

Later phases will add:

- production-style integrations
- policy retrieval
- LLM evidence summarization
- constrained tool calling
- agent orchestration
- evaluation
- red-team testing
- guardrails
- production infrastructure

## Example

Request:

```json
{
  "case_id": "CASE-3001",
  "order_id": "ORD-1001"
}
```

Expected investigation:

```text
OMS: order exists
Returns: COMPLETED
Payments: FAILED

Finding:
REFUND_STATE_CONFLICT

Recommendation:
Escalate to Payments Operations.
Do not issue a second refund automatically.
```

## Phase 9 Outcome

Phase 9 converts the project from architecture documentation into executable software.

The prototype demonstrates:

1. typed enterprise evidence
2. system-of-record adapters
3. cross-system investigation
4. deterministic exception detection
5. safe recommendation behavior
6. API exposure
7. automated testing

The next phase is **Phase 10 — Data / Integration Build**, where the mock integration layer is evolved toward production-style enterprise connectors, resilience, correlation, retries, timeouts, and integration contracts.
