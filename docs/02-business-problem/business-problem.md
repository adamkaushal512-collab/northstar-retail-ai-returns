# NorthStar Retail — AI Returns & Refund Operations Platform

## Phase 2 — Business Problem

### 1. Executive Problem Statement

NorthStar Retail's standard in-policy returns can generally be processed through existing return workflows. The larger operational challenge occurs when a return or refund becomes an exception.

For exception cases, employees may need to investigate information across multiple enterprise systems, reconstruct the history of the transaction, reconcile conflicting information, determine the applicable policy, identify permitted actions, and obtain the correct approval before the case can be resolved.

This fragmented process increases investigation effort and resolution time, creates opportunities for inconsistent handling, generates unnecessary escalations and repeat customer contacts, and makes it difficult to reconstruct why a particular decision was made.

The business problem is therefore not simply that employees use multiple systems. The problem is the operational cost, delay, inconsistency, and customer impact created by manually coordinating evidence and decisions across those systems.

---

### 2. Current-State Problem

Return and refund exception investigations may require employees to work across:

- POS
- Order Management System (OMS)
- Payments
- Shipping and Fulfillment
- Customer and Loyalty
- Inventory
- Returns
- IT Service Management (ITSM)

Employees may need to determine:

- What transaction originally occurred
- Whether the order and return can be verified
- Whether the item was delivered or returned
- Whether a refund was initiated
- Whether the refund succeeded or failed
- Which system contains the authoritative status
- Which return or refund policy applies
- Whether the requested action is allowed
- Whether human approval is required
- Which team should receive an escalation

When information is incomplete or contradictory, employees must manually reconstruct the case before taking action.

---

### 3. Root Causes

Initial customer discovery indicates several contributing causes.

#### Fragmented Enterprise Data

Relevant information is distributed across multiple systems rather than presented as a unified case history.

#### Conflicting System State

Different systems may report different statuses for the same order, shipment, return, or refund.

#### Manual Timeline Reconstruction

Employees may need to manually combine events from orders, payments, shipping, returns, customer interactions, and support systems.

#### Policy Complexity

Return and refund policies can vary by product category, promotion, holiday period, payment method, operational requirement, and other conditions.

#### Unclear Decision Boundaries

Employees must determine whether they can resolve a case themselves or whether manager, Returns Operations, Payments, or Risk approval is required.

#### Incomplete Decision History

Notes, evidence, approvals, and previous actions may be distributed across systems, making previous decisions difficult to understand.

---

### 4. Business Impact

The current exception-handling process can affect both operational efficiency and customer experience.

Potential impacts include:

- Longer exception-resolution times
- Increased employee time spent searching enterprise systems
- Repeated customer contacts for unresolved cases
- Unnecessary escalations to managers and specialist teams
- Higher operational cost per exception case
- Greater risk of inconsistent return and refund decisions
- Refund delays caused by investigation or payment-processing issues
- Reduced customer satisfaction when status or reasoning is unclear
- Increased effort during internal reviews and customer disputes
- Limited auditability of evidence, recommendations, approvals, and actions

These impacts must be measured against real operational baselines before quantified benefits or ROI claims are made.

---

### 5. Affected Users and Stakeholders

Primary operational users include:

- Store associates
- Store managers
- Customer-service agents
- Returns operations specialists

Supporting stakeholders include:

- Payments teams
- Fraud and risk analysts
- Warehouse and fulfillment teams
- IT and support teams
- Legal and compliance stakeholders
- Store operations leadership

Customers are indirectly affected through resolution speed, refund-status visibility, consistency, and overall service experience.

---

### 6. Initial Problem Scope

The initial scope focuses on return and refund exception investigation and decision support.

Representative exception types include:

- Missing receipt or order
- Payment mismatch
- Damaged-item cases
- Returns outside the allowed policy window
- Shipment marked delivered but disputed by the customer
- High-value returns or refunds
- Refund-processing failures
- Conflicting information between enterprise systems

Normal, verified, in-policy returns are not the primary target of the initial solution because existing workflows can continue to process those cases.

---

### 7. Out of Scope for the Initial Solution

The initial project will not attempt to:

- Replace the enterprise POS
- Replace the OMS
- Replace the payment processor
- Replace the returns system of record
- Redesign the entire retail return policy
- Fully automate every return decision
- Allow AI to independently accuse customers of fraud
- Allow AI to deny returns solely through model judgment
- Allow AI to issue unauthorized high-value refunds
- Allow AI to override approved return or refund policy
- Allow AI to modify customer payment information

These boundaries keep the initial project focused on investigation, evidence synthesis, policy-aware decision support, workflow coordination, and controlled actions.

---

### 8. Target Operational Outcome

The desired future state is an operational capability that helps authorized employees quickly understand a return or refund exception without manually reconstructing the entire case across disconnected systems.

The capability should help users:

- View a consolidated case history
- Identify relevant source-system evidence
- Understand conflicting information
- Determine the applicable approved policy and version
- Understand which actions are permitted
- Identify whether approval is required
- Route escalations to the appropriate team
- Preserve evidence and reasoning
- Record approvals and operational actions
- Maintain a traceable audit history

The system should assist employees while preserving deterministic business rules and required human authority.

---

### 9. Decision and Automation Boundaries

The solution must distinguish between assistance and authority.

Potential AI-assisted capabilities may include:

- Summarizing case history
- Identifying relevant evidence
- Highlighting conflicting system information
- Retrieving applicable policy
- Explaining why escalation may be required
- Recommending appropriate next steps

Sensitive or high-impact actions must remain governed by deterministic rules, authorization controls, and human approval where required.

AI must not become the authoritative source for transaction state, policy ownership, payment state, or approval authority.

---

### 10. Enterprise Constraints

Any future solution must account for:

- Personally identifiable information (PII)
- Payment-data protection
- Role-based access control
- Least-privilege access
- Audit logging
- Data-retention requirements
- Legacy enterprise systems and APIs
- Service rate limits
- Upstream-system latency and availability
- Restrictions on exposing sensitive enterprise data to unauthorized AI services

The platform must not become a single point of failure for normal return operations.

If the platform is unavailable, normal in-policy returns should continue through existing systems, while complex exception cases should fall back to established manual investigation and escalation procedures.

---

### 11. Auditability Requirements

For a resolved exception case, NorthStar should be able to reconstruct:

- Who investigated the case
- Which source systems and records were accessed
- Which policy and policy version were used
- What evidence was considered
- What recommendations were produced
- Whether AI participated in the investigation
- Which tools or operational actions were executed
- Who approved or rejected sensitive actions
- Relevant timestamps
- The final outcome

Auditability is a core operational requirement rather than an optional reporting feature.

---

### 12. Initial Scale Assumptions

For portfolio design purposes, the project currently assumes approximately:

- 50,000 returns per week
- 10–15% requiring exception investigation or approval
- Approximately 5,000–7,500 exception cases per week
- 5–10 minutes for a typical normal return
- 30 minutes to several hours for many exception investigations
- Multiple days for some complex cases

These values are assumptions, not validated NorthStar production statistics.

They will be treated as discovery hypotheses until validated through operational data.

---

### 13. Initial Business Hypothesis

If NorthStar can provide employees with a unified, policy-aware, auditable investigation workflow for return and refund exceptions, then employees should be able to resolve cases with less manual system searching and more consistent decision support.

This should create opportunities to reduce:

- Exception-resolution time
- Manual investigation effort
- Systems searched per case
- Repeat customer contacts
- Unnecessary escalations
- Operational handling cost
- Decision inconsistency

while improving:

- Auditability
- Policy adherence
- Employee confidence
- Customer experience

The hypothesis will be tested using explicit success metrics and operational baselines in later phases.

---

### 14. FDE Problem Definition

The Forward Deployed Engineering challenge is to determine how NorthStar's existing systems, business rules, policies, operational workflows, and AI capabilities can be combined into a reliable enterprise workflow without transferring inappropriate decision authority to an AI model.

The solution must determine which parts of the workflow belong to:

- Deterministic business logic
- Enterprise integrations
- Data reconciliation
- Search and retrieval
- Generative AI
- Tool calling
- Agentic orchestration
- Human review and approval

The architecture should be driven by the business problem and operational constraints rather than by a requirement to use AI everywhere.

---

## Phase 2 Outcome

Phase 2 defines the core problem as fragmented and manually intensive return and refund exception investigation rather than ordinary return processing.

The next phase will map the current workflow in detail, including actors, systems, decision points, handoffs, exception paths, waiting states, and escalation boundaries before solution architecture is designed.
