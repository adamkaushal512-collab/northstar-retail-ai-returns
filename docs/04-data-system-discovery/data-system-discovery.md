# NorthStar Retail — AI Returns & Refund Operations Platform

## Phase 4 — Data + System Discovery

### 1. Objective

Phase 4 identifies the enterprise systems, authoritative data sources, identifiers, integration patterns, security boundaries, data-quality risks, and operational failure modes involved in return and refund exception investigations.

The purpose is to understand the existing enterprise environment before designing the solution architecture.

The future platform should operate as an investigation and orchestration layer over existing systems of record rather than becoming a competing transactional source of truth.

---

### 2. Enterprise System Landscape

#### Order Management System (OMS)

Responsibilities:

- Order identity
- Order lines
- Order status
- Fulfillment method
- Fulfillment status
- Cancellation information
- Order timestamps

Initial authority assumption:

OMS is authoritative for order and fulfillment state.

Important identifiers:

- order_id
- order_line_id
- customer_id
- sku
- fulfillment_id
- store_id

Potential integrations:

- REST APIs
- Internal service APIs
- Events
- Batch feeds

Validation required:

- API availability
- Rate limits
- Historical state availability
- Event support
- Retention period
- Split-shipment representation

---

#### Point of Sale (POS)

Responsibilities:

- Store transactions
- Receipt information
- Tender information
- Store and register identifiers
- Transaction timestamps
- Store-originated returns

Initial authority assumption:

POS is authoritative for store transaction records.

Important identifiers:

- transaction_id
- receipt_id
- store_id
- register_id
- order_id
- sku

Validation required:

- Central transaction availability
- Offline transaction synchronization
- Receipt-less return representation
- E-commerce order correlation
- Historical retention

---

#### Returns Management System

Responsibilities:

- Return cases
- Returned items
- Return reasons
- Inspection results
- Exception status
- Return disposition
- Approval state
- Final resolution

Initial authority assumption:

The Returns system is authoritative for return-case lifecycle and disposition.

Important identifiers:

- return_id
- return_case_id
- order_id
- order_line_id
- customer_id
- approval_id

Validation required:

- Case data model
- Exception representation
- Status history
- Approval model
- External evidence support
- Idempotent action APIs

---

#### Payments Platform

Responsibilities:

- Original payment transaction
- Payment authorization and capture
- Refund initiation
- Refund status
- Refund failures
- Processor references

Initial authority assumption:

Payments is authoritative for payment and refund transaction state.

Important identifiers:

- payment_id
- refund_id
- order_id
- processor_reference
- payment_method_token

Validation required:

- Refund lifecycle
- Pending/settled/failed/reversed states
- Retry behavior
- Partial refunds
- Idempotency
- Processor latency
- Security boundaries

Raw card data must not be exposed to the investigation platform or AI layer.

Only approved tokenized or masked payment metadata should be used.

---

#### Shipping and Fulfillment

Responsibilities:

- Shipment creation
- Carrier information
- Tracking information
- Delivery events
- Delivery timestamps
- Return shipments
- Warehouse receipt

Important identifiers:

- shipment_id
- fulfillment_id
- tracking_number
- order_id
- return_id
- warehouse_id

Validation required:

- Carrier integration
- Event availability
- Event retention
- Proof-of-delivery availability
- Return-shipment correlation
- Internal versus carrier authority

---

#### Inventory Platform

Responsibilities:

- Store inventory
- Warehouse inventory
- Returned-item state
- Restock state
- Damaged or quarantined inventory

Initial authority assumption:

Inventory is authoritative for inventory state but not return approval or refund state.

Important identifiers:

- sku
- location_id
- inventory_item_id
- return_id

Validation required:

- Update frequency
- Eventual consistency
- Return-to-inventory timing
- Damaged-item representation

---

#### Customer and Loyalty Platform

Responsibilities:

- Customer profile
- Loyalty identity
- Account relationships
- Relevant interaction information

Important identifiers:

- customer_id
- loyalty_id
- account_id

This domain may contain PII.

Only information required for an authorized operational investigation should be exposed.

Validation required:

- PII classification
- Field-level access
- Retention
- Role permissions
- Operationally necessary attributes

---

#### IT Service Management (ITSM)

Responsibilities:

- Incidents
- Problems
- Known outages
- Technical escalations
- Service-impact information

Important identifiers:

- incident_id
- problem_id
- service_id
- return_case_id
- order_id

ITSM information can help determine whether an apparent case-specific problem is actually caused by a known Payments, OMS, POS, or integration outage.

---

#### Return Policy Repository

Responsibilities:

- Approved return policies
- Refund rules
- Policy versions
- Effective dates
- Product/category exceptions
- Promotional or seasonal rules

Initial authority assumption:

Returns Operations owns the core policy, with contributions from Legal/Compliance, Payments, Risk, and Store Operations.

Validation required:

- Repository location
- Machine-readable access
- Versioning
- Effective dates
- Approval workflow
- Historical policy access

---

### 3. Initial Source-of-Truth Matrix

| Data Domain | Initial Authoritative System | Status |
|---|---|---|
| Order state | OMS | Validate |
| Fulfillment state | OMS / Fulfillment | Boundary requires validation |
| Store transaction | POS | Validate |
| Return case | Returns | Validate |
| Return disposition | Returns | Validate |
| Payment transaction | Payments | Validate |
| Refund transaction | Payments | Validate |
| Shipment events | Shipping / Carrier | Authority boundary requires validation |
| Inventory state | Inventory | Validate |
| Customer profile | Customer/Loyalty | Validate |
| Technical incidents | ITSM | Validate |
| Return policy | Returns Operations policy repository | Validate |

These are discovery assumptions rather than final architecture facts.

---

### 4. Cross-System Identity and Correlation

A single return investigation may involve:

- order_id
- order_line_id
- return_id
- return_case_id
- payment_id
- refund_id
- transaction_id
- receipt_id
- customer_id
- shipment_id
- tracking_number
- sku
- store_id

The platform must not assume that every enterprise system uses one universal identifier.

A future correlation layer may require:

- Identifier mapping
- Cross-reference tables
- Source-specific identifiers
- Correlation APIs
- Match-confidence information
- Preservation of original source identifiers

Incorrect correlation is a high-risk failure mode because evidence belonging to one transaction or customer could otherwise be associated with another case.

---

### 5. Conceptual Investigation Data Model

The investigation layer may normalize evidence without replacing authoritative source records.

Potential entities include:

#### ReturnCase

- case_id
- return_id
- order_id
- customer_reference
- exception_type
- current_status
- created_at
- updated_at

#### OrderEvidence

- source_system
- order_id
- order_status
- fulfillment_status
- source_timestamp
- retrieved_at

#### PaymentEvidence

- source_system
- payment_id
- refund_id
- refund_status
- amount
- masked_payment_method
- processor_reference
- source_timestamp
- retrieved_at

#### ShipmentEvidence

- source_system
- shipment_id
- tracking_reference
- shipment_status
- delivery_events
- source_timestamp
- retrieved_at

#### PolicyEvidence

- policy_id
- policy_version
- effective_date
- applicable_rules
- retrieved_at

#### DecisionRecord

- case_id
- evidence_references
- deterministic_rule_results
- recommendation
- ai_assistance_used
- required_approval
- approver
- action_taken
- timestamp

This is a conceptual model, not the final production schema.

---

### 6. Data Freshness and Consistency

Enterprise systems may update at different times.

The platform must distinguish among:

- Genuine conflicting information
- Expected processing delays
- Stale cached information
- Eventually consistent updates
- Missing information
- Actual system failures

Retrieved evidence should preserve:

- source_system
- source_record_id
- source_timestamp
- retrieval_timestamp
- status

AI must not silently choose one conflicting status and present it as authoritative fact.

---

### 7. Integration Patterns

#### Synchronous APIs

Useful when employees require current information during an investigation.

Risks include:

- Latency
- Timeouts
- Rate limits
- Upstream outages

#### Event-Driven Integration

Potential events include:

- ReturnCreated
- ReturnReceived
- RefundInitiated
- RefundFailed
- RefundSettled
- ShipmentDelivered
- ApprovalRequested
- ApprovalCompleted

Event consumers must account for:

- Duplicate events
- Out-of-order events
- Missing events
- Schema evolution
- Idempotency

#### Batch Integration

Legacy systems may require batch feeds.

Risks include:

- Stale data
- Partial files
- Delayed synchronization
- Reprocessing complexity

The eventual architecture may require a combination of synchronous APIs, events, and batch integration.

---

### 8. Failure Modes

Important failure scenarios include:

- Upstream API unavailable
- API timeout
- Rate-limit exhaustion
- Authentication failure
- Authorization failure
- Missing source record
- Duplicate event
- Out-of-order event
- Stale cached information
- Conflicting system state
- Incorrect identifier correlation
- Partial investigation data
- Payment processor delay
- Carrier-data delay
- Policy service unavailable
- AI service unavailable

Missing information must be represented explicitly.

The system must never fabricate missing source-system evidence.

---

### 9. Security and Data Boundaries

The platform must account for:

- PII
- Payment information
- RBAC
- Least privilege
- Encryption
- Secrets management
- Audit logging
- Data retention
- AI-provider data boundaries

Raw payment-card information should not enter the investigation platform.

Before AI implementation, NorthStar must establish:

- Which fields may be sent to an AI model
- Which fields require masking
- Which fields must never reach a model
- Provider retention requirements
- Prompt/response logging rules
- Model access controls

Authorization must be enforced by application and service controls rather than relying on prompts.

---

### 10. Audit and Provenance

Every investigation should preserve evidence provenance.

Relevant metadata includes:

- Source system
- Source record identifier
- Source timestamp
- Retrieval timestamp
- API or tool used
- Requesting user/service
- Policy version
- AI involvement
- Human approval
- Final action

AI-generated interpretations must remain distinguishable from authoritative source-system facts.

Recommendations should be traceable to the evidence and policy used.

---

### 11. Availability and Fallback

The platform must not become a single point of failure for standard returns.

If the investigation platform is unavailable:

- Normal in-policy returns should continue through existing systems.
- Complex exceptions should fall back to manual investigation.
- Required approvals must remain enforced.
- AI unavailability should not disable safe deterministic workflows.

---

### 12. Observability Requirements

Future integrations should expose operational metrics such as:

- Request volume
- API latency
- Error rate
- Timeout rate
- Rate-limit events
- Retry count
- Event-processing lag
- Dead-letter events
- Data freshness
- Correlation failures
- Upstream availability
- Tool-call success and failure

These requirements will be implemented during later production-engineering phases.

---

### 13. Key Questions for System Owners

Before final architecture, the FDE must validate:

- Which APIs actually exist?
- Which events are available?
- Which systems support batch only?
- What are the rate limits?
- What are normal latency expectations?
- What are availability guarantees?
- How long is historical data retained?
- Which system is authoritative for each disputed state?
- How are records correlated?
- Which operations support idempotency?
- Which data is classified as sensitive?
- Which roles may access which evidence?
- How are policies stored and versioned?
- What information may be exposed to AI services?
- What fallback processes already exist?

---

### 14. Assumptions Requiring Validation

The project currently assumes:

- OMS is authoritative for order state.
- Payments is authoritative for refund state.
- Returns is authoritative for return-case state.
- POS is authoritative for store transactions.
- Shipping/Fulfillment provides authoritative shipment evidence within defined boundaries.
- Stable identifiers or mappings exist for cross-system correlation.
- Enterprise systems expose APIs, events, or batch feeds.
- Policy versions can be retrieved programmatically.
- Required evidence can be accessed without violating security controls.
- AI services can operate within approved NorthStar data-governance boundaries.

These assumptions must be validated before they become implementation requirements.

---

### 15. FDE Assessment

The central technical problem is not simply connecting an LLM to enterprise APIs.

The difficult problem is constructing trustworthy investigation context from distributed systems whose information may be incomplete, stale, delayed, contradictory, or subject to different authorization boundaries.

The future architecture should therefore maintain clear separation among:

1. Authoritative source-system facts
2. Integration and correlation logic
3. Deterministic business rules
4. Policy retrieval
5. AI interpretation and recommendations
6. Human review and approval
7. Authorized operational actions

This separation will guide later architecture and AI design.

---

## Phase 4 Outcome

Phase 4 establishes the initial enterprise system landscape, source-of-truth assumptions, cross-system identity requirements, conceptual investigation data model, integration patterns, security boundaries, failure modes, audit requirements, and system-owner validation questions.

The future platform should operate as an investigation and orchestration layer over existing transactional systems rather than becoming a new system of record.

The next phase will prioritize candidate use cases according to business value, feasibility, risk, data readiness, and suitability for AI-assisted workflows.
