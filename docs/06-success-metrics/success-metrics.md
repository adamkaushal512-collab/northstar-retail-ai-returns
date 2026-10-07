# NorthStar Retail — AI Returns & Refund Operations Platform

## Phase 6 — Success Metrics

## 1. Purpose

The purpose of Phase 6 is to define measurable success criteria for the initial vertical slice selected in Phase 5:

> **AI-assisted refund exception investigation for cases with unclear, conflicting, delayed, or failed refund status.**

The Forward Deployed Engineer must define success before solution architecture and implementation begin.

A successful AI demonstration is not sufficient.

The solution must demonstrate measurable improvement across:

1. Business outcomes
2. Operational efficiency
3. Investigation quality
4. AI quality
5. RAG quality
6. Agent and tool behavior
7. Human escalation
8. Safety and governance
9. Reliability and performance
10. Auditability
11. Cost

---

# 2. Measurement Philosophy

NorthStar will use three categories of metrics.

## 2.1 Business Metrics

Measure whether the solution improves the actual returns/refund operation.

## 2.2 AI and Engineering Metrics

Measure whether AI, retrieval, tools, integrations, and orchestration behave correctly.

## 2.3 Safety Metrics

Measure whether the system respects authorization, policy, data boundaries, and human approval requirements.

Safety release gates take precedence over aggregate AI quality scores.

---

# 3. Baseline Requirement

Before pilot deployment, NorthStar should establish a baseline using historical or manually investigated refund exception cases.

Baseline measurements should include:

- Median resolution time
- P90 resolution time
- Investigator active work time
- Systems manually accessed per case
- Repeat customer contacts
- Escalation frequency
- Case reopen rate
- Policy errors
- Refund investigation errors
- Audit completeness
- Cost per exception where measurable

Baseline definitions should be frozen before pilot comparison.

This prevents success criteria from being changed after results are observed.

---

# 4. Primary Business Metric

## Refund Exception Resolution Time

Definition:

Time between the beginning of an eligible refund exception investigation and operational resolution.

Measure:

- Median
- P90
- P95

### Initial Pilot Hypothesis

Reduce median resolution time by:

**≥ 30%**

Reduce P90 resolution time by:

**≥ 20%**

These numbers are portfolio pilot targets.

They are not claims about achieved NorthStar performance.

---

# 5. Investigator Productivity

## 5.1 Systems Manually Accessed

Measure how many enterprise applications the investigator manually opens during an exception.

Examples:

- OMS
- Returns
- Payments
- POS
- Shipping
- Policy repository

### Target Hypothesis

Reduce manual application navigation by:

**≥ 40%**

The platform may still access these systems through controlled APIs or tools.

The goal is reducing employee context switching, not eliminating systems of record.

---

## 5.2 Investigator Active Work Time

Measure active employee time spent:

- locating records
- reconstructing timelines
- comparing statuses
- searching policy
- identifying missing evidence
- determining escalation
- documenting findings

Target:

Meaningful reduction against the established baseline.

---

# 6. Customer Experience Metrics

## Repeat Customer Contacts

Measure cases where the customer must contact NorthStar again because the original interaction could not determine:

- refund status
- expected timing
- required action
- escalation status

### Initial Target Hypothesis

Reduce repeat contacts for eligible cases by:

**≥ 20%**

---

# 7. Escalation Metrics

## 7.1 Unnecessary Escalation Rate

Measure cases escalated to:

- Payments
- Returns Operations
- Store management
- Risk
- technical support

that could have been correctly resolved without specialist intervention.

### Initial Target Hypothesis

Reduce unnecessary escalations by:

**≥ 20%**

This metric must never be optimized by suppressing required escalations.

---

## 7.2 Escalation Correctness

Measure whether the system correctly identifies cases requiring specialist or human approval.

### Initial Evaluation Target

**≥ 98%**

on labeled evaluation cases.

---

# 8. Refund-State Accuracy

The system should correctly classify operational refund states such as:

- refund not found
- initiated
- pending
- settled
- failed
- reversed
- conflicting
- insufficient evidence

Ground truth should come from validated authoritative system evidence.

AI must not establish transactional truth independently.

---

# 9. Conflict Detection

Measure whether the workflow correctly detects contradictory evidence.

Examples:

Returns:
> Refund completed.

Payments:
> Refund failed.

Or:

Returns:
> Return received.

Payments:
> No refund transaction exists.

The platform should surface the conflict rather than allow AI to silently select a preferred answer.

---

# 10. Missing Evidence Detection

The system should explicitly identify missing required evidence.

Examples:

- payment transaction unavailable
- order lookup failed
- refund identifier missing
- policy unavailable
- stale system response

AI must not fabricate missing information.

---

# 11. Policy Accuracy

Measure whether the workflow:

- retrieves the correct policy
- retrieves the approved policy
- uses the correct version
- respects effective dates
- identifies applicable rules
- identifies required approvals

### Initial Target Hypothesis

**≥ 99% policy adherence**

on the evaluated pilot dataset.

---

# 12. RAG Metrics

Policy knowledge will use Retrieval-Augmented Generation.

RAG evaluation should include:

## 12.1 Recall@K

Determine whether relevant approved policy evidence appears in the retrieved candidate set.

### Initial Target

**Recall@5 ≥ 95%**

---

## 12.2 Retrieval Precision

Measure how much retrieved context is actually relevant.

Poor precision increases:

- model distraction
- token cost
- latency
- incorrect reasoning risk

---

## 12.3 Citation Correctness

A policy citation must actually support the statement attributed to it.

---

## 12.4 Policy-Version Accuracy

The workflow must retrieve the policy version applicable to the transaction/event date.

This is critical because return policies may change due to:

- promotions
- holidays
- product category
- payment requirements
- legal requirements
- operational changes

---

# 13. AI Grounding Metrics

## Evidence Attribution Precision

AI-generated factual statements should be traceable to supplied evidence.

### Initial Target

**≥ 98%**

---

## Unsupported Factual Claim Rate

Definition:

Percentage of factual claims presented as established facts without support from enterprise evidence or approved policy.

### Initial Target

**≤ 1%**

for non-critical explanatory content.

Unsupported material claims must not drive high-impact operational actions.

---

# 14. Recommendation Quality

Evaluate recommendations for:

- evidence consistency
- policy consistency
- operational usefulness
- correct escalation
- appropriate uncertainty
- allowed action

Recommendation evaluation may combine:

- deterministic graders
- labeled expected outcomes
- domain expert review
- carefully controlled AI-assisted evaluation

Human/domain evaluation remains important for subjective operational quality.

---

# 15. Tool-Calling Metrics

The investigation workflow may use tools such as:

- `get_order`
- `get_return_case`
- `get_refund_status`
- `get_payment_transaction`
- `get_policy`
- `get_case_history`

Measure:

## Tool Selection Accuracy

Did the system select the correct tool?

### Initial Target

**≥ 95%**

---

## Tool Argument Accuracy

Did the system provide valid:

- identifiers
- parameters
- scopes
- request structures?

---

## Tool Success Rate

Track:

- successful calls
- timeout
- 429/rate limiting
- 5xx
- authentication failure
- authorization failure
- malformed response
- missing record

---

# 16. Agentic Workflow Metrics

The AI workflow may conditionally gather additional evidence.

Measure:

- tool calls per investigation
- repeated tool calls
- unnecessary tool calls
- maximum-step termination
- workflow completion
- tool sequencing
- agent loop rate

The orchestration layer must prevent uncontrolled autonomous loops.

---

# 17. Human-in-the-Loop Metrics

## Human Approval Bypass

Target:

**0**

The system must never execute an action requiring human approval without authorization.

---

## Human Override Rate

Measure how often investigators reject or modify AI recommendations.

Capture reason codes such as:

- incorrect evidence
- missing evidence
- wrong policy
- incorrect recommendation
- unnecessary escalation
- missing escalation
- system limitation

Overrides become valuable FDE feedback for improving the system.

---

# 18. Safety Metrics

The following are zero-tolerance conditions.

## Unauthorized High-Impact Action

Target:

**0**

## Cross-Customer Evidence Leakage

Target:

**0**

## AI-Only Return Denial

Target:

**0**

## Autonomous Fraud Accusation

Target:

**0**

## AI Policy Override

Target:

**0**

## Unauthorized Payment Information Modification

Target:

**0**

## Approval Bypass

Target:

**0**

## Successful Prompt-Injection Authorization Bypass

Target:

**0**

Customer notes, retrieved policy, tool responses, or other untrusted content must never be able to expand AI/tool permissions.

---

# 19. Auditability

Every investigation should record required provenance.

Examples:

- investigator identity
- case identifier
- correlation identifier
- source systems accessed
- source records
- retrieval timestamps
- policy identifier
- policy version
- evidence considered
- deterministic rule results
- AI involvement
- model/version where applicable
- tool calls
- human approvals
- actions
- final outcome

### Initial Pilot Target

**≥ 99% audit completeness**

Sensitive actions require complete audit records.

---

# 20. Reliability Metrics

Measure:

- platform availability
- API error rate
- workflow completion rate
- integration availability
- tool failure rate
- timeout rate
- retry rate
- event-processing failure
- dead-letter events
- stale data rate

Platform reliability should be measured separately from upstream system reliability.

### Initial Design Target

**99.9% platform availability**

during the supported operating window.

This is an architecture target, not an achieved production SLA.

---

# 21. Performance Metrics

## API Latency

Initial architecture target:

**P95 < 500 ms**

for non-AI platform operations excluding external dependency latency.

---

## Investigation Completion Latency

Initial target hypothesis:

**P95 < 15 seconds**

for normal automated evidence sets.

Human approval and unavailable upstream dependencies are measured separately.

---

# 22. Idempotency

Controlled actions must not create duplicate financial side effects.

Track:

- duplicate requests
- duplicate actions
- idempotency conflicts
- ambiguous writes
- reconciliation outcomes

### Target

**0 duplicate financial side effects caused by platform retry behavior.**

---

# 23. Cost Metrics

Track per investigation:

- model input tokens
- model output tokens
- model cost
- retrieval operations
- tool-call count
- compute cost
- storage cost where applicable

Calculate:

## Cost Per Assisted Investigation

Platform operating cost / assisted investigations.

## Cost Per Successfully Resolved Exception

Platform operating cost / successfully resolved eligible exceptions.

AI quality and safety take precedence over minimizing token cost.

---

# 24. Evaluation Dataset

Create a versioned, de-identified or synthetic evaluation dataset containing representative cases.

Examples:

1. Settled refund
2. Pending refund
3. Delayed refund
4. Failed refund
5. Missing refund
6. Conflicting Returns/Payments state
7. Missing order
8. Stale evidence
9. Policy-version boundary
10. High-value approval
11. Out-of-policy exception
12. Upstream unavailable
13. Duplicate event
14. Ambiguous payment outcome
15. Prompt-injection attempt
16. Unauthorized-action attempt

The evaluation dataset becomes part of the engineering release process in later phases.

---

# 25. Release Gates

A build must not progress toward production if testing identifies:

- authorization bypass
- cross-customer leakage
- unauthorized refund action
- missing required human approval
- material policy-version error
- fabricated source evidence
- untraceable sensitive action
- critical prompt-injection vulnerability
- duplicate financial side effects

These conditions override aggregate model scores.

---

# 26. Pilot Scorecard

The future pilot should report:

## Business

- Median resolution-time improvement
- P90 resolution-time improvement
- Repeat-contact reduction
- Escalation reduction
- Investigator effort reduction

## AI Quality

- Grounding
- Unsupported claims
- RAG Recall@K
- Citation correctness
- Recommendation quality

## Agent Quality

- Tool selection
- Tool argument accuracy
- Tool sequencing
- Loop rate
- Workflow completion

## Safety

- Authorization violations
- Approval bypasses
- Data leakage
- Prompt-injection failures

## Engineering

- Availability
- Error rate
- Latency
- Integration failures

## Economics

- Cost per investigation
- Estimated labor savings
- Net operational benefit

---

# 27. Success Decision

The project should not be declared successful merely because the AI produces impressive responses.

The vertical slice succeeds when evidence demonstrates that it:

1. Reduces investigation effort or resolution time.
2. Maintains or improves policy adherence.
3. Produces grounded and traceable conclusions.
4. Correctly uses enterprise tools.
5. Preserves human authority.
6. Prevents unauthorized actions.
7. Remains auditable.
8. Operates reliably.
9. Provides measurable business value.
10. Operates at acceptable cost.

---

# 28. FDE Perspective

The Forward Deployed Engineer is responsible for connecting model performance to customer outcomes.

This means the FDE must understand:

Customer workflow  
→ enterprise systems  
→ data quality  
→ integration behavior  
→ AI behavior  
→ human decision boundaries  
→ production reliability  
→ business KPI.

A high-performing LLM does not compensate for incorrect enterprise data, unsafe authorization, poor workflow design, or lack of user adoption.

---

# Phase 6 Outcome

NorthStar Retail now has a measurable definition of success for the initial AI-assisted refund exception investigation vertical slice.

The project will evaluate:

- business impact
- investigator productivity
- customer experience
- evidence quality
- policy correctness
- RAG quality
- AI grounding
- tool behavior
- agent behavior
- human escalation
- safety
- auditability
- reliability
- latency
- idempotency
- cost

Baseline values still require validation using real operational data.

Therefore, numerical targets in this phase are explicitly treated as **pilot hypotheses and engineering targets**, not fabricated production achievements.

Phase 7 will use these requirements to design the end-to-end solution architecture.
