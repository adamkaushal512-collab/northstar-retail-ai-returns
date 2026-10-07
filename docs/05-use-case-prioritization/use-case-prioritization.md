# NorthStar Retail — AI Returns & Refund Operations Platform

## Phase 5 — Use-Case Prioritization

## 1. Purpose

The purpose of this phase is to identify the best initial AI-enabled use case for NorthStar Retail's returns and refund exception workflow.

The objective is not to apply AI everywhere.

The FDE objective is to select a narrow vertical slice that:

- solves a meaningful customer problem
- has measurable business value
- has sufficient enterprise data
- can be integrated realistically
- benefits from AI reasoning
- preserves deterministic controls
- maintains human authority for high-impact decisions
- creates reusable capabilities for future workflows

---

## 2. Candidate Use Cases

The discovery and workflow phases identified the following candidates:

1. Cross-system return case summarization
2. Refund-status investigation
3. Refund-failure investigation
4. Policy determination
5. Conflicting-system-state investigation
6. Disputed-delivery investigation
7. High-value return investigation
8. Damaged-item assessment

---

## 3. Prioritization Criteria

Each use case is evaluated using:

1. Business value
2. Operational frequency
3. Investigation effort
4. Data availability
5. Integration feasibility
6. Suitability for deterministic automation
7. Suitability for AI assistance
8. Human-approval requirements
9. Operational/compliance risk
10. Ability to measure success
11. Reusability

---

## 4. Prioritization Assessment

| Use Case | Business Value | AI Fit | Data Readiness | Risk | Initial Priority |
|---|---|---|---|---|---|
| Cross-system case summarization | High | High | High | Low | High |
| Refund-status investigation | High | High | High | Medium | **Very High** |
| Refund-failure investigation | High | High | High | Medium | **Very High** |
| Policy determination | High | High | Medium | Medium | High |
| Conflicting-system-state investigation | High | High | Medium | Medium | High |
| Disputed delivery | High | Medium | Medium | High | Medium |
| High-value return | High | Medium | Medium | High | Medium |
| Damaged-item assessment | Medium | High | Low/Medium | High | Later |

---

## 5. Selected Initial Vertical Slice

The selected initial use case is:

> **AI-assisted refund exception investigation for cases with unclear, conflicting, delayed, or failed refund status.**

This combines refund-status and refund-failure investigation into a coherent operational workflow.

---

## 6. Why This Use Case Was Selected

### Strong Business Value

Refund exceptions directly affect:

- customer satisfaction
- repeat contacts
- employee investigation time
- specialist escalations
- operational cost
- refund delays

### Strong Data Availability

Relevant evidence already exists across:

- Returns Management
- OMS
- Payments
- POS
- Shipping
- Policy systems

The primary problem is not absence of data.

The problem is fragmented evidence across enterprise systems.

### Strong AI Fit

AI is useful for:

- synthesizing evidence
- reconstructing timelines
- explaining conflicting states
- summarizing investigation findings
- interpreting retrieved policy
- generating evidence-grounded recommendations

### Strong Deterministic Control Opportunities

AI does not need to control:

- authentication
- authorization
- payment state
- refund execution
- approval thresholds
- policy effective dates
- idempotency
- financial controls

These should remain deterministic.

### Measurable

The workflow supports clear metrics including:

- resolution time
- systems manually accessed
- escalation rate
- repeat contacts
- evidence accuracy
- policy accuracy
- recommendation quality
- tool accuracy
- latency
- cost

---

## 7. Target Workflow

The initial workflow should:

1. Receive a refund exception case.
2. Identify the associated return.
3. Correlate the original order.
4. Retrieve Returns evidence.
5. Retrieve OMS evidence.
6. Retrieve Payments/refund evidence.
7. Retrieve additional evidence when necessary.
8. Detect missing or conflicting information.
9. Retrieve the applicable approved policy.
10. Apply deterministic business rules.
11. Construct an evidence-grounded investigation summary.
12. Explain the likely current refund state.
13. Recommend the allowed next operational step.
14. Determine whether human approval or specialist escalation is required.
15. Preserve the evidence, reasoning context, tool activity, approvals, and final action.

---

## 8. Role of AI

AI may:

- summarize case evidence
- reconstruct timelines
- explain conflicts
- identify missing evidence
- explain applicable policy
- generate evidence-grounded recommendations
- communicate uncertainty

AI does not become the source of truth.

Enterprise systems remain authoritative.

---

## 9. Role of RAG

Retrieval-Augmented Generation will be used for approved policy knowledge.

The system should retrieve:

- applicable policy
- correct policy version
- effective date
- relevant policy sections

The AI should reason only over approved retrieved policy evidence.

RAG should not be used as a substitute for transactional system lookups.

---

## 10. Role of Tool Calling

The AI/orchestration layer may use controlled tools such as:

- `get_order`
- `get_return_case`
- `get_refund_status`
- `get_payment_transaction`
- `get_policy`
- `get_case_history`

Future controlled action tools may include:

- `create_escalation`
- `request_approval`
- `add_case_note`
- `retry_eligible_refund`

Write tools require stronger authorization and audit controls than read tools.

---

## 11. Role of Agentic Orchestration

The investigation may require conditional evidence gathering.

Example:

Return lookup  
→ identify order  
→ inspect refund state  
→ detect missing/conflicting evidence  
→ retrieve additional source evidence  
→ retrieve policy  
→ apply deterministic checks  
→ produce recommendation  
→ request human approval when required.

The agent must operate inside explicit tool, authorization, step, and policy boundaries.

---

## 12. Human-in-the-Loop Boundary

Human review remains required for situations including:

- high-value refunds
- out-of-policy exceptions
- payment mismatches
- manual overrides
- ambiguous authoritative evidence
- unusual risk conditions
- actions requiring explicit approval

AI may assist the decision.

AI does not replace required authority.

---

## 13. Prohibited AI Actions

The solution must not allow AI to autonomously:

- accuse a customer of fraud
- deny a return solely from AI judgment
- override approved policy
- modify customer payment information
- issue unauthorized high-value refunds
- bypass approval requirements
- fabricate missing evidence
- silently resolve conflicting source-of-truth records

---

## 14. Initial Inputs

Potential investigation inputs:

- return case ID
- return ID
- order ID
- customer reference where permitted
- refund ID where available
- authenticated investigator identity
- investigation reason

---

## 15. Expected Outputs

The workflow should produce:

- case summary
- event timeline
- evidence used
- source references
- missing evidence
- conflicting evidence
- applicable policy
- policy version
- deterministic rule results
- current refund state
- recommended next step
- required approval/escalation
- uncertainty indicators
- audit record

---

## 16. Evaluation Potential

The selected use case supports evaluation of:

- evidence retrieval
- evidence attribution
- policy retrieval
- policy citation
- tool selection
- tool sequencing
- conflict detection
- unsupported claims
- recommendation quality
- escalation correctness
- latency
- cost

This makes it particularly suitable for a production-oriented AI project rather than a demonstration-only chatbot.

---

## 17. Initial User

The initial user is an authorized:

- Returns Operations investigator
- customer-service employee
- refund specialist

handling refund exception cases.

---

## 18. Initial Triggers

Examples:

- customer reports refund not received
- refund remains pending beyond expected timing
- refund processing failed
- Returns and Payments show conflicting status
- expected refund transaction cannot be located
- manual investigation requested
- specialist review required

---

## 19. Non-Goals

The initial vertical slice will not attempt to:

- automate every return type
- replace OMS
- replace Payments
- replace Returns Management
- make fraud determinations
- autonomously approve high-value refunds
- perform AI-only denials
- override policy
- modify payment information
- allow unrestricted autonomous actions

---

## 20. Reusable Capabilities Created

Although the initial use case is narrow, it creates reusable enterprise AI capabilities:

- enterprise tool adapters
- canonical evidence model
- identity correlation
- provenance tracking
- policy retrieval
- deterministic rule evaluation
- constrained agent orchestration
- human approval workflow
- audit logging
- AI evaluation
- security boundaries
- observability

These capabilities can later support additional returns workflows.

---

## 21. Expansion Sequence

After the initial vertical slice proves successful, expansion may proceed toward:

1. broader refund failures
2. complex policy exceptions
3. cross-system conflicts
4. out-of-policy returns
5. disputed deliveries
6. high-value returns
7. damaged-item workflows
8. additional customer-service exception workflows

Expansion should depend on measured evidence rather than assumed success.

---

## 22. FDE Decision

The FDE recommendation is to start with refund exception investigation because it provides the strongest combination of:

- meaningful business value
- available enterprise evidence
- clear AI reasoning opportunities
- measurable outcomes
- manageable initial risk
- human-control boundaries
- reusable technical components

This is intentionally a vertical slice rather than an enterprise-wide AI transformation.

---

## Phase 5 Outcome

NorthStar Retail now has a prioritized initial AI use case:

**AI-assisted refund exception investigation for unclear, conflicting, delayed, or failed refund status.**

The next phase will define measurable success criteria before architecture and implementation begin.
