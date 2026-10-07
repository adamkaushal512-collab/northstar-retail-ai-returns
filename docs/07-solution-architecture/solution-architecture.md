# NorthStar Health — Solution Architecture

## Phase 7 — Solution Architecture

## 1. Purpose

This document defines the proposed architecture for NorthStar Health's first deployable vertical slice:

**AI-assisted clinical evidence investigation for MRI/CT prior authorization exceptions.**

The architecture converts the discovery, workflow, system-landscape, prioritization, and success-metric work from Phases 1–6 into a production-shaped technical design. It is intentionally modular and implementation-oriented without prematurely introducing distributed-system complexity.

The system helps a Prior Authorization Specialist understand the case, retrieve relevant payer requirements and clinical evidence, identify gaps or conflicts, verify source provenance, and decide the appropriate operational next step.

The platform is decision support. Existing clinical, authorization, scheduling, eligibility, and payer systems remain authoritative.

---

## 2. Architecture Goals

The initial architecture must:

- integrate with existing healthcare systems rather than replace them
- retrieve structured and unstructured clinical evidence
- preserve source provenance for every evidence item
- distinguish missing evidence from unavailable systems
- keep human review in the authorization workflow
- constrain AI access to enterprise systems
- support measurable evaluation from Phase 6
- fail safely without blocking the existing authorization process
- expose enough telemetry for debugging and operational support
- remain simple enough to implement as a realistic portfolio vertical slice

---

## 3. Core Architecture Principles

### 3.1 Systems of Record Remain Authoritative

The platform does not become the source of truth for clinical or payer data.

Working ownership assumptions are:

| Domain | Authoritative Source |
|---|---|
| Clinical order and documentation | EHR / originating clinical repository |
| Imaging appointment | Scheduling system |
| Verified coverage | Eligibility service / payer response |
| Internal authorization workflow | Prior authorization platform |
| Payer requirements | Payer-approved source |
| Payer authorization decision | Payer |

The platform may normalize and temporarily assemble this information for investigation, but it does not replace the originating systems.

### 3.2 AI Output Is Derived Information

AI-generated summaries, mappings, classifications, missing-evidence flags, and investigation suggestions are derived artifacts.

They must not overwrite source clinical records or be represented as authoritative facts without supporting evidence.

### 3.3 Provenance Is Mandatory

Every evidence item presented as supporting an authorization requirement must retain sufficient metadata for a specialist to verify it against the source.

### 3.4 Human Review Is Required

The initial deployment will not autonomously:

- approve or deny authorization
- determine medical necessity
- diagnose a patient
- recommend treatment
- change clinical documentation
- modify payer requirements
- submit an authorization without an explicitly designed and approved human workflow

### 3.5 Absence and Unavailability Are Different States

The system must distinguish:

- evidence searched and not found
- source not searched
- source unavailable
- access denied
- retrieval timed out
- incomplete response
- ambiguous evidence

A failed integration must never silently become "no evidence exists."

---

## 4. High-Level Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                 Enterprise Healthcare Systems                │
│                                                              │
│ EHR/FHIR │ Documents │ Scheduling │ Coverage │ PA │ Payers   │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                    Integration Layer                         │
│ Adapters │ Auth │ Timeouts │ Retries │ Validation │ Mapping  │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                  Canonical Case Context                      │
│ Patient │ Coverage │ Order │ Appointment │ PA │ Requirements │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                    Evidence Retrieval                        │
│ Structured Search │ Document Search │ Hybrid Retrieval       │
│ Candidate Selection │ Provenance Capture                     │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                     AI Evidence Engine                       │
│ Requirement Matching │ Extraction │ Summarization            │
│ Missing Evidence │ Conflict / Uncertainty Detection          │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                 Orchestration + Guardrails                   │
│ Case State │ Tool Policy │ Validation │ Audit │ Failures     │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                 Specialist Review Experience                 │
│ Context │ Requirements │ Evidence │ Sources │ Gaps │ Warnings│
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
                    Human operational decision
```

---

## 5. Enterprise Source Boundaries

### 5.1 EHR / FHIR Boundary

The EHR supplies patient context, imaging orders, diagnoses, encounters, clinical notes, medication history, procedures, prior imaging, observations, and related clinical information.

FHIR is preferred where the customer's implementation exposes the required data. Potential resources include:

- Patient
- ServiceRequest
- Encounter
- Condition
- Observation
- MedicationRequest
- Procedure
- DiagnosticReport
- DocumentReference
- Practitioner
- Organization

FHIR is an integration mechanism, not the entire architecture. Vendor-specific APIs or document interfaces may be required when standard resources do not expose required workflow data.

### 5.2 Clinical Document Repository

The document boundary provides unstructured or externally sourced information such as scanned records, outside specialist notes, physical-therapy documentation, imported reports, and historical documents.

Document source, date, type, and originating organization must be preserved when available.

### 5.3 Scheduling

Scheduling supplies the imaging appointment, facility, scheduled date/time, and appointment state. This context allows the workflow to understand operational urgency.

### 5.4 Eligibility / Coverage

The coverage boundary provides current verified insurance context. The architecture distinguishes recently verified eligibility from insurance information merely stored in another application.

### 5.5 Prior Authorization Platform

The PA platform supplies the internal operational case, including case ID, assigned specialist, workflow status, procedure, payer, payer case reference, and relevant operational metadata.

### 5.6 Payer Boundary

Payer integrations may provide authorization requirements, case status, additional-information requests, and authorization outcomes.

Connectivity is intentionally heterogeneous. A payer may use an API, clearinghouse, portal, telephone, fax, or another manual workflow. The architecture must not assume universal API access.

---

## 6. Integration Adapter Layer

Source-specific behavior is isolated behind adapters such as:

```text
EHRAdapter
DocumentAdapter
SchedulingAdapter
CoverageAdapter
AuthorizationAdapter
PayerAdapter
```

Adapters own:

- authentication and service identity
- authorization scopes
- request construction
- source-specific schemas
- timeouts
- bounded retries where safe
- rate-limit handling
- response validation
- source error translation
- correlation identifiers
- freshness metadata

Higher layers consume normalized contracts rather than embedding vendor-specific behavior.

This boundary is important for an FDE because customer environments vary even when the business workflow is similar.

---

## 7. Canonical Investigation Context

The platform assembles a normalized working representation:

```text
InvestigationCase
├── patient
├── coverage
├── imaging_order
├── appointment
├── authorization_case
├── payer_requirements
├── evidence_candidates
└── source_status
```

This object is not a new system of record. It is a temporary or controlled working context for investigation and evaluation.

Each field should preserve the originating system and retrieval metadata where appropriate.

---

## 8. Cross-System Identifier Resolution

Identifiers must be mapped explicitly.

Examples include:

```text
EHR patient ID
↔ Medical Record Number
↔ Coverage member ID
↔ Authorization patient reference
```

and:

```text
internal procedure ID ↔ CPT/HCPCS
internal provider ID ↔ NPI
internal authorization case ID ↔ payer case ID
```

The platform must not guess when identity resolution is ambiguous.

A failed or ambiguous correlation becomes a visible exception requiring human or integration-level resolution.

---

## 9. Evidence Retrieval Architecture

Clinical evidence may exist in structured and unstructured sources.

### Structured Retrieval

Examples:

- diagnoses
- medications
- procedures
- observations
- encounters
- diagnostic reports
- imaging history

### Unstructured Retrieval

Examples:

- progress notes
- specialist notes
- physical-therapy notes
- scanned documents
- external medical records

The retrieval pipeline will:

1. receive case context
2. identify evidence requirements
3. determine candidate source types
4. apply patient and case constraints
5. retrieve candidate records
6. preserve source metadata
7. rank relevant candidates
8. provide candidates to the AI evidence engine

---

## 10. Hybrid Retrieval Strategy

The initial solution uses hybrid retrieval rather than relying on vector search alone.

Potential retrieval signals include:

- structured filters
- date ranges
- document type
- encounter type
- procedure code
- keyword retrieval
- semantic similarity
- metadata relevance

Healthcare evidence investigation frequently requires hard constraints such as patient identity, time period, evidence category, and document provenance. Semantic similarity is useful, but it must operate inside those boundaries.

---

## 11. Evidence Data Model

A normalized evidence item should conceptually contain:

```text
EvidenceItem
├── evidence_id
├── patient_id
├── evidence_type
├── source_system
├── source_record_id
├── source_document_id
├── service_date
├── author
├── content_reference
├── retrieved_content
├── retrieval_timestamp
└── relevance_metadata
```

AI interpretation is stored separately from source evidence.

```text
Source Evidence
      │
      ▼
AI Interpretation
├── requirement association
├── extracted finding
├── concise summary
├── uncertainty
└── evaluation metadata
```

This separation prevents model-generated interpretation from being confused with the original record.

---

## 12. Payer Requirement Representation

Payer requirements require their own provenance and versioning.

Conceptually:

```text
PayerRequirement
├── requirement_id
├── payer_id
├── plan_id
├── procedure_code
├── requirement_type
├── description
├── effective_date
├── source
├── source_version
└── retrieved_at
```

A requirement update should not silently rewrite the historical basis of a completed investigation.

---

## 13. AI Evidence Engine

The AI layer performs bounded tasks.

### Requirement Interpretation

Translate payer evidence requirements into structured investigation targets.

### Evidence Matching

Associate candidate clinical evidence with the requirement it may support.

### Evidence Extraction

Identify relevant portions of source material while retaining source references.

### Evidence Summarization

Produce concise specialist-facing summaries. Summaries remain derived information.

### Missing-Evidence Detection

Identify requirements for which supporting evidence was not found in the successfully searched sources.

Preferred wording is bounded, for example:

> No supporting evidence was found in the sources successfully searched.

The model must not convert that into a claim that the patient never received the treatment or service.

### Conflict Detection

Surface potentially contradictory information rather than silently choosing one version.

### Uncertainty

The engine must be able to return:

- insufficient evidence
- ambiguous evidence
- conflicting evidence
- source unavailable
- manual review required

A definitive answer is not required for every case.

---

## 14. LLM Trust Boundary

The LLM does not receive unrestricted direct access to enterprise systems.

```text
LLM
 │
 ▼
Controlled Orchestration / Tool Layer
 │
 ▼
Approved Integration Adapters
 │
 ▼
Enterprise Systems
```

Tool access is:

- allow-listed
- schema validated
- permission controlled
- logged
- limited to required workflow operations

The model cannot invent arbitrary enterprise actions.

The initial vertical slice should favor read-oriented tools.

---

## 15. Investigation Orchestrator

The orchestrator coordinates workflow execution.

```text
Receive Investigation Request
        ↓
Validate Request and Identity
        ↓
Load Authorization Context
        ↓
Load Scheduling / Coverage Context
        ↓
Load Payer Requirements
        ↓
Retrieve Clinical Evidence
        ↓
Evaluate Source Completeness
        ↓
Run AI Evidence Analysis
        ↓
Validate Provenance and Guardrails
        ↓
Assemble Structured Result
        ↓
Present to Specialist
```

The orchestrator owns execution state, not clinical truth.

---

## 16. Structured Investigation Result

The API-facing result should be structured rather than only free-form text.

```text
InvestigationResult
├── case_context
├── payer_requirements
├── supporting_evidence
├── missing_evidence
├── conflicting_information
├── unavailable_sources
├── warnings
├── provenance
└── audit_reference
```

Structured output improves UI behavior, automated evaluation, guardrails, testing, and observability.

---

## 17. Specialist Review Experience

The specialist should receive a unified investigation view containing:

### Case Context

- procedure
- diagnosis / indication
- payer
- appointment
- authorization status

### Requirement Checklist

Each requirement can be represented as:

```text
Evidence found
Evidence not found in searched sources
Uncertain
Source unavailable
```

### Evidence

Each evidence item exposes:

- concise finding
- source system
- source date
- document/note reference
- ability to inspect source context

### Warnings

Examples:

- source unavailable
- coverage may be stale
- procedure information conflicts
- payer requirements incomplete
- evidence ambiguous

Uncertainty must be visible rather than hidden behind fluent AI text.

---

## 18. Human Decision Boundary

After reviewing the result, the Prior Authorization Specialist may:

- accept relevant evidence
- reject irrelevant evidence
- inspect additional records
- request missing documentation
- escalate
- continue authorization preparation

The initial AI workflow does not make the final operational decision.

---

## 19. Guardrail Layer

Before model output is presented, deterministic validation should verify where possible that:

- evidence claims contain source references
- required result fields exist
- source failures are represented
- missing-data language is qualified
- prohibited autonomous actions are absent
- schema contracts are satisfied

Probabilistic model behavior should not be the only enforcement mechanism for deterministic workflow rules.

---

## 20. Audit Architecture

Important events produce audit records, including:

- investigation requested
- source queried
- source failed
- evidence retrieved
- AI analysis performed
- evidence surfaced
- specialist accepted/rejected evidence
- correction recorded
- investigation completed

Audit records should preserve useful metadata without unnecessarily copying protected clinical content into logs.

---

## 21. Security Boundary

Detailed controls are defined in Phase 8, but the architecture establishes the trust path:

```text
User
 ↓
Authenticated Application
 ↓
Authorization / RBAC
 ↓
Investigation Service
 ↓
Controlled Integration Layer
 ↓
Enterprise Systems
```

Key principles include:

- least privilege
- minimum necessary access
- service identity
- user authorization
- encrypted transport
- encryption at rest for approved persisted data
- secrets management
- auditability
- restricted logging of clinical content

---

## 22. Data Persistence

The platform should minimize unnecessary clinical-data replication.

Persist only information required for:

- investigation workflow
- provenance
- approved evaluation
- audit
- reliability
- explicitly approved operational needs

Large authoritative clinical records should remain in source systems whenever practical.

Derived AI artifacts require explicit retention rules.

---

## 23. Caching and Freshness

Caching policy depends on business consequence.

Potentially stable data may include selected reference configuration and versioned payer requirement metadata.

Short-lived caching may be appropriate for investigation context and retrieved evidence.

Stricter freshness applies to:

- authorization status
- appointment state
- verified eligibility
- changed imaging orders

The system should carry retrieval/freshness metadata so users and downstream logic can distinguish current from potentially stale information.

---

## 24. Failure and Degraded Modes

### EHR Unavailable

The result indicates clinical-source unavailability and incomplete investigation. The system does not claim that evidence is absent.

### Document Repository Unavailable

Structured evidence may still be presented, but document coverage is marked incomplete.

### Payer Requirement Source Unavailable

The system does not invent payer requirements. The specialist continues through the existing manual process when necessary.

### AI Service Unavailable

The core authorization workflow continues without AI assistance.

### Partial Retrieval Failure

Successfully retrieved evidence may be shown while unavailable sources are explicitly identified.

### Identifier Mismatch

The workflow stops or degrades safely rather than attaching evidence to an uncertain patient or case.

---

## 25. Reliability Controls

Integration calls should use appropriate:

- timeouts
- bounded retries
- rate-limit handling
- circuit breaking where justified
- correlation IDs
- structured error categories

Retries must not accidentally duplicate state-changing operations.

The first vertical slice is primarily read-oriented, reducing integration risk.

---

## 26. Observability

The architecture supports three telemetry layers.

### Technical Telemetry

- request latency
- service error rate
- source-system latency
- timeout rate
- retrieval failure rate
- model latency
- token/cost usage where appropriate

### AI Quality Telemetry

- evidence accepted
- evidence rejected
- specialist correction rate
- missing-evidence corrections
- unsupported-output detections

### Workflow Telemetry

- investigation duration
- records reviewed
- repeat investigation
- workflow abandonment
- completion state

This connects the implementation directly to the Phase 6 success framework.

---

## 27. End-to-End Data Flow

```text
Authorization Case
        ↓
Investigation API
        ↓
Authorization Adapter
        ↓
Canonical Case Context
        ↓
Scheduling + Coverage Context
        ↓
Payer Requirement Retrieval
        ↓
EHR + Document Retrieval
        ↓
Candidate Evidence
        ↓
Hybrid Retrieval / Ranking
        ↓
AI Evidence Analysis
        ↓
Requirement ↔ Evidence Mapping
        ↓
Provenance Validation
        ↓
Guardrail Validation
        ↓
Structured Investigation Result
        ↓
Prior Authorization Specialist
        ↓
Human Operational Action
```

---

## 28. Initial Deployment Boundary

The portfolio implementation should avoid premature microservices.

A practical initial service can contain modular boundaries:

```text
Application
│
├── API Layer
├── Investigation Orchestrator
├── Integration Adapters
├── Canonical Models
├── Retrieval Module
├── AI Evidence Module
├── Guardrails
├── Audit Module
└── Observability
```

These are logical modules, not necessarily separately deployed services.

This design keeps the vertical slice understandable, testable, and deployable while preserving future extraction points.

---

## 29. Proposed Technology Direction

Implementation choices will be finalized in later phases, but the architecture supports the following portfolio direction:

| Concern | Direction |
|---|---|
| Application language | Python |
| API | FastAPI or equivalent |
| Typed contracts | Pydantic or equivalent |
| Healthcare interfaces | FHIR-compatible + simulated enterprise adapters |
| Retrieval | Structured + semantic hybrid retrieval |
| AI | LLM-assisted extraction, matching, summarization |
| Metadata persistence | Relational database |
| Semantic retrieval | Vector capability where justified |
| Packaging | Docker |
| CI/CD | GitHub Actions |
| Testing | Unit, integration, contract, evaluation, failure-mode tests |
| Observability | Structured logs, metrics, tracing, correlation IDs |

These are project implementation choices, not claims about a real NorthStar environment.

---

## 30. Synthetic Data Boundary

Because this is a public portfolio project:

- no real PHI will be committed
- no real patient records will be used
- no real credentials will be stored
- no real payer credentials will be used

Synthetic fixtures will model:

- patients
- MRI/CT orders
- appointments
- coverage
- encounters
- clinical notes
- payer requirements
- authorization cases
- source failures
- conflicting evidence
- missing evidence

The synthetic environment should reproduce realistic integration and workflow complexity without exposing protected information.

---

## 31. Architecture Decisions

### ADR-1 — Integrate Rather Than Replace

Existing enterprise systems remain authoritative.

### ADR-2 — Human-in-the-Loop Is Mandatory

The initial deployment provides decision support, not autonomous authorization.

### ADR-3 — Provenance Is First-Class

Evidence without sufficient traceability cannot be treated as verified case-supporting evidence.

### ADR-4 — Use Hybrid Retrieval

Structured constraints and semantic retrieval are combined.

### ADR-5 — Isolate Enterprise Integrations

Vendor-specific behavior remains behind adapters.

### ADR-6 — Start Modular, Not Microservices

Logical boundaries are required; distributed deployment is deferred until justified.

### ADR-7 — No Direct LLM Enterprise Access

Enterprise access is mediated by controlled tools and adapters.

### ADR-8 — Fail Back to Existing Workflow

AI failure must not block the existing authorization process.

### ADR-9 — Distinguish Absence from Unavailability

Missing evidence and failed retrieval are represented separately.

### ADR-10 — Prefer Deterministic Guardrails

Schema, provenance, permission, and workflow constraints should be enforced deterministically where possible.

---

## 32. Key Architecture Risks

Important risks include:

- incomplete clinical retrieval
- payer requirement changes
- cross-system identity mismatch
- stale information
- poor document classification
- hallucinated evidence interpretation
- excessive reliance on summaries
- source-system downtime
- high retrieval latency
- low specialist trust
- unnecessary data persistence
- integration complexity

These risks become inputs to security, implementation, evaluation, guardrail, and pilot phases.

---

## 33. Implementation Sequence Enabled by This Architecture

The architecture supports an incremental build:

1. define typed canonical models
2. create synthetic enterprise adapters
3. implement case-context assembly
4. implement evidence retrieval
5. add provenance contracts
6. implement bounded AI evidence analysis
7. add deterministic guardrails
8. expose the investigation API
9. build evaluation datasets and tests
10. add security controls
11. instrument observability
12. pilot the complete vertical slice

This avoids attempting every enterprise integration at once.

---

## 34. What Phase 7 Does Not Implement

Phase 7 does not yet build:

- production APIs
- live FHIR connections
- embeddings or vector indexes
- LLM workflows
- databases
- user interface
- cloud infrastructure
- CI/CD
- production monitoring

It defines the architecture those components must follow.

---

## 35. Phase 7 Outcome

NorthStar Health now has a production-shaped architecture for the initial AI-assisted prior authorization evidence-investigation vertical slice.

The design establishes:

- authoritative source-system boundaries
- enterprise integration adapters
- canonical case context
- explicit identifier resolution
- hybrid evidence retrieval
- provenance-first evidence representation
- versioned payer requirements
- bounded AI responsibilities
- controlled tool access
- investigation orchestration
- structured outputs
- human review
- deterministic guardrails
- auditability
- security boundaries
- persistence and freshness principles
- safe degraded modes
- reliability controls
- observability
- modular implementation boundaries
- a synthetic-data strategy

The central architecture principle is:

**AI accelerates clinical evidence investigation while authoritative enterprise systems and human specialists retain control.**

The next phase is:

**Phase 8 — Security, Privacy & Governance**

Phase 8 will convert these trust boundaries into explicit controls for PHI handling, authentication, authorization, least privilege, secrets, auditability, retention, model/data governance, and secure AI usage.
