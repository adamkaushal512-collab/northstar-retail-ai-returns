# NorthStar Retail — Customer Discovery Notes

## Project

NorthStar Retail — AI Returns & Refund Operations Platform

## Current Returns Workflow

A typical return currently follows this high-level process:

1. Customer brings or ships an item for return.
2. Employee looks up the original order.
3. Employee checks the returned item.
4. Employee processes the return.
5. Refund is sent to the customer's original payment method.

## Initial Customer Pain Points

NorthStar identified several recurring problems:

- Refund status can be unclear.
- Returned-item condition can be difficult to determine.
- Refund/payment processing can fail.
- Exception cases frequently require manager or specialist approval.
- Employees must search across multiple enterprise systems.
- Information in different systems may conflict.
- Employees may not know which return policy applies.
- Case notes may be incomplete.
- Employees often reconstruct the case timeline manually.
- It can be difficult to understand why a previous decision was made.


## Systems Involved in Return Investigations

Employees may need to access several enterprise systems during a return/refund exception:

- POS — point-of-sale transaction information
- OMS — order and fulfillment information
- Payments — payment and refund transaction status
- Shipping/Fulfillment — shipment and delivery information
- Customer/Loyalty — customer account and loyalty information
- Inventory — item and inventory status
- Returns — return case and disposition information
- ITSM — operational incidents and support tickets

## People and Teams Involved

Return/refund exceptions may involve:

- Store associate
- Store manager
- Customer-service agent
- Returns operations specialist
- Payments team
- Fraud/risk analyst
- Warehouse/fulfillment team
- IT/support


## Common Return and Refund Exceptions

A return may require additional investigation or approval when:

- Original receipt or order cannot be found
- Payment information does not match
- Item is damaged
- Return is outside the allowed return window
- Shipment is marked delivered but the customer disputes receipt
- Return involves an unusually high-value item or refund
- Refund processing fails
- Different enterprise systems contain conflicting information


## Decision and Approval Boundaries

### Associate-Level Decisions

A store associate may process a normal return when:

- The return is within policy
- The original transaction can be verified
- The payment method is valid
- No significant exception or escalation condition exists

### Human Approval Required

Additional approval is required for cases such as:

- Out-of-policy returns
- High-value refunds
- Unusual return patterns
- Payment mismatches
- Manual refund overrides

Approvals may involve a store manager, returns operations, payments, or risk team depending on the exception.


## Operational Scale and Timing Assumptions

The following numbers are initial project assumptions and should be validated with production data during a real customer engagement.

- Approximately 50,000 returns are processed per week.
- Approximately 10–15% of returns require exception investigation or approval.
- This represents roughly 5,000–7,500 exception cases per week.
- A normal return typically takes approximately 5–10 minutes to process.
- An exception may require 30 minutes to several hours of investigation.
- Complex cases involving another team or approval may remain unresolved for days.


## Desired Operational Capability

NorthStar wants employees investigating return/refund exceptions to be able to:

- Quickly understand the complete case history
- Determine which return/refund policy applies
- Identify conflicting information across systems
- Understand which actions are permitted
- Know when a case requires escalation
- Know which team or approver should receive the escalation
- Reduce manual searching across multiple enterprise systems
- Preserve a clear record of evidence, actions, approvals, and decisions

## Desired Business Outcomes

NorthStar wants to achieve:

- Shorter exception-resolution time
- Fewer systems employees must manually search
- Fewer repeat customer contacts
- Fewer unnecessary escalations
- Lower refund-processing operational cost
- Fewer processing errors
- Better auditability
- Improved customer satisfaction



## AI Trust Boundaries

NorthStar does not want an AI system to autonomously:

- Accuse a customer of fraud
- Deny a return based solely on AI judgment
- Issue a high-value refund without required authorization
- Override company return or refund policy
- Change customer payment information
- Make operational decisions without a traceable audit record

AI may assist investigation and operational decision-making, but sensitive or high-impact actions must respect established business rules, authorization requirements, and human approval boundaries.


## Enterprise Constraints

NorthStar identified the following constraints that must be respected:

- Protect customer PII and sensitive customer information
- Protect payment-related data
- Enforce role-based access control (RBAC)
- Apply least-privilege access
- Maintain audit logs for investigations, decisions, approvals, and actions
- Respect enterprise data-retention requirements
- Integrate with legacy systems and APIs
- Respect API and service rate limits
- Account for availability limitations of upstream enterprise systems
- Restrict sensitive enterprise data from being sent to unauthorized external AI models

## Availability and Operational Fallback

The future platform must not become a single point of failure for normal retail operations.

- Normal in-policy returns must continue through existing systems if the investigation platform is unavailable.
- Complex exception cases must be able to fall back to the existing manual investigation and escalation process.


## Auditability and Explainability Requirements

NorthStar must be able to reconstruct the complete history of a return/refund exception.

The audit record should capture:

- Who investigated the case
- Which source systems and records were accessed
- Which return/refund policy and policy version applied
- What evidence was considered during the investigation
- What recommendations were produced
- Whether AI participated in the investigation
- Which tools or operational actions were executed
- Who approved or rejected the proposed action
- Timestamps for investigations, recommendations, approvals, and actions
- The final case outcome

Audit records must support internal reviews, customer disputes, and applicable compliance requirements.


## Initial Systems of Record

The following are initial discovery assumptions about authoritative systems and must be validated during Data + System Discovery:

- OMS — authoritative source for order and fulfillment state
- Payments — authoritative source for payment and refund transaction state
- Shipping/Fulfillment — authoritative source for shipment and carrier events
- POS — authoritative source for store transaction data
- Returns — authoritative source for return case and disposition

When information conflicts across systems, the platform must not assume that all sources have equal authority. Source-of-truth rules must be validated with NorthStar system owners before implementation.


## Return and Refund Policy Ownership

NorthStar's core return and refund policy is owned by Returns Operations.

Other stakeholders may contribute requirements or rules, including:

- Legal/Compliance
- Payments
- Risk
- Store Operations

Return and refund policies may change because of:

- Promotions
- Holiday return periods
- Product categories
- Payment requirements
- Regulatory or compliance requirements
- Operational changes

Employees must use the currently approved policy version when investigating or resolving a return/refund case.

Policy ownership, approval workflow, versioning, effective dates, and distribution mechanisms must be investigated further before implementation.


## Open Questions and Validation Items

The following items remain open and should be validated in later phases:

- Confirm actual weekly return volume and exception rate using NorthStar operational data
- Measure actual normal-return and exception-resolution times
- Confirm system owners and authoritative sources for each data domain
- Identify APIs, events, batch feeds, and other integration mechanisms available from each enterprise system
- Determine API rate limits, latency expectations, and availability characteristics
- Confirm exact approval thresholds for high-value and out-of-policy refunds
- Define which unusual return patterns require Risk review
- Confirm payment-data and PII handling requirements
- Identify data that must never be exposed to an AI model
- Confirm return/refund policy storage, versioning, approval, and effective-date processes
- Determine required audit-log retention periods
- Identify existing manual fallback and escalation procedures
- Establish baseline operational metrics before measuring improvement

