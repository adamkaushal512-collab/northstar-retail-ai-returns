# NorthStar Retail — Return & Refund Exception Workflow

## Phase 3 — Current-State Workflow Mapping

### Purpose

This document maps the current-state operational workflow used to investigate and resolve return and refund exceptions at NorthStar Retail.

The goal is to understand how employees, managers, specialist teams, and enterprise systems participate in exception handling before designing changes to the workflow or introducing AI-assisted capabilities.

### Workflow Trigger

The workflow begins when a return or refund cannot be completed confidently through the standard return process and requires additional investigation, decision-making, approval, or escalation.

A case may become an exception when available information is incomplete, inconsistent, or insufficient to determine the appropriate action through the normal workflow.

### Actors

The current-state exception workflow may involve the following participants:

- **Customer** — initiates the return or refund request and may provide transaction, product, payment, or fulfillment information.

- **Store or Customer Service Associate** — begins the standard return workflow, gathers initial information, and identifies when the case cannot be resolved through the normal process.


- **Store Manager or Supervisor** — reviews exceptions requiring additional judgment, authorization, or escalation.

- **Specialist Operations Team** — investigates cases that require expertise or access beyond the store or frontline employee.

- **IT or Application Support** — assists when the exception involves system availability, integration failures, incorrect system behavior, or other technical issues


### Systems Consulted

Depending on the exception, employees may need to consult multiple enterprise systems during investigation:

- **POS** — transaction details, purchase history, tender information, and store return activity.

- **Order Management System (OMS)** — order details, fulfillment status, cancellations, and order-level history.

- **Returns System** — return requests, return status, prior return activity, and return-related records.

- **Payments System** — payment authorization, capture, refund status, payment method, and payment-processing results.

- **Shipping and Fulfillment Systems** — shipment status, delivery information, pickup status, and fulfillment events.

- **Customer and Loyalty Systems** — customer account information and relevant loyalty or purchase context.

- **Inventory System** — product and inventory information when inventory state is relevant to the exception.

- **IT Service Management (ITSM)** — incidents or support tickets when investigation requires technical escalation.

### Current-State Workflow

#### Step 1 — Exception Identification

**Primary actor:** Store or Customer Service Associate

The employee begins processing the customer's return or refund request through the standard return workflow.

During this process, the employee encounters information, system behavior, or a policy condition that prevents the request from being completed confidently through the normal process.

The case is then treated as an exception requiring additional investigation.

Examples may include:

- Transaction or order information cannot be located or confidently matched.
- Information differs across systems.
- Return eligibility cannot be determined from the available information.
- Refund status or payment information is unclear.
- Fulfillment or delivery information conflicts with the customer's request.
- The requested action requires additional authorization or review.

#### Step 2 — Initial Evidence Gathering

**Primary actor:** Store or Customer Service Associate

The employee gathers the information needed to understand the exception and reconstruct the relevant transaction, order, return, refund, or fulfillment history.

Depending on the case, the employee may search across multiple systems to collect evidence such as:

- Original transaction or order details
- Product and quantity information
- Purchase date and location
- Payment method and payment status
- Existing return or refund records
- Shipment, delivery, or pickup information
- Customer-provided information
- Relevant customer or loyalty account information
- Previous case notes or support records

Because this information may be distributed across different systems, the employee may need to manually search for and correlate records using identifiers such as order number, transaction number, customer information, product identifiers, or return identifiers.
#### Step 3 — Evidence Reconciliation

**Primary actor:** Store or Customer Service Associate

After gathering the available evidence, the employee compares information across the relevant systems to determine whether the records describe a consistent sequence of events.

The employee may need to investigate differences such as:

- POS transaction status differs from the return record.
- OMS order status differs from fulfillment information.
- Payment or refund status differs from the status shown in another system.
- Shipment or delivery information conflicts with the customer's account of the event.
- Multiple records exist for the same order, transaction, return, or refund.
- Required information is missing from one or more systems.

When records conflict, the employee must determine which information is relevant and sufficiently reliable to continue the investigation.

If the conflicting or missing information cannot be resolved with the employee's available systems and access, the case may require escalation to a manager, specialist team, or technical support team.
#### Step 4 — Policy Determination

**Primary actor:** Store or Customer Service Associate

After reconstructing the available evidence, the employee determines which return or refund policy applies to the case.

The employee may need to consider factors such as:

- Purchase date and return window
- Product or merchandise category
- Original purchase channel
- Return channel
- Receipt or proof-of-purchase availability
- Product condition
- Original payment method
- Fulfillment method
- Previous return or refund activity relevant to the case
- Policy-specific restrictions or exceptions

The employee compares the available case evidence with the applicable policy requirements to determine whether the requested action is permitted through the standard process.

If the policy is unclear, multiple policies appear applicable, or the requested action requires an exception to standard policy, the employee may need additional review or approval.

#### Step 5 — Resolution Decision and Escalation

**Primary actor:** Store or Customer Service Associate

After reviewing the available evidence and applicable policy, the employee determines whether the case can be resolved within their authority.

If the evidence is sufficient, the applicable policy is clear, and the requested action is within the employee's permitted authority, the employee can proceed with the appropriate return or refund action.

The case may require escalation when:

- Evidence remains incomplete or conflicting.
- The applicable policy cannot be determined confidently.
- The requested action falls outside standard policy.
- Manager or supervisor authorization is required.
- The employee does not have sufficient system access or permissions.
- Payment or refund processing requires specialist investigation.
- A system or integration issue prevents the case from being resolved.

Depending on the reason for escalation, the case may be transferred to a store manager or supervisor, specialist operations team, or IT or application support team.

The receiving team may perform additional investigation, request more information, approve or reject an exception, or return the case to the frontline employee with resolution instructions.

#### Step 6 — Return or Refund Action Execution

**Primary actor:** Authorized Store or Customer Service Associate, Manager, or Specialist Operations Team

After the appropriate resolution has been determined and any required approval has been obtained, an authorized employee performs the permitted return or refund action.

Depending on the case, the action may include:

- Completing the return through the appropriate system.
- Initiating or completing a refund.
- Returning funds to the permitted payment method.
- Applying an approved policy exception.
- Updating the return or refund case status.
- Recording required approval or authorization information.
- Providing instructions for additional operational processing when immediate completion is not possible.

The employee verifies whether the requested action was accepted by the relevant system and records any resulting transaction, return, refund, or case identifiers.

If the action fails or produces an unexpected system response, the case may require additional investigation or technical escalation rather than being treated as successfully resolved.
#### Step 7 — Customer Communication

**Primary actor:** Store or Customer Service Associate

After the return or refund action has been completed, approved, rejected, or moved into additional processing, the employee communicates the current outcome to the customer.

Depending on the case, the communication may include:

- Whether the return or refund was approved or could not be completed.
- What action was taken.
- The expected next step when additional processing is required.
- Available refund status or processing information.
- Any additional information or action required from the customer.
- How the customer can follow up if the issue remains unresolved.

When the case cannot be resolved immediately, the employee may need to provide a case, return, refund, or support reference that can be used for subsequent follow-up.

The information communicated to the customer should reflect the current system state and approved resolution rather than an unverified assumption about the outcome.

#### Step 8 — Case Closure and Audit Trail

**Primary actor:** Store or Customer Service Associate, Manager, or Specialist Operations Team

After the required action and customer communication have been completed, the employee updates the case or relevant operational records to reflect the final outcome.

Depending on the systems and exception type, the employee may record:

- Final return or refund status
- Resolution outcome
- Relevant transaction, order, return, or refund identifiers
- Evidence used during the investigation
- Applicable policy or exception basis
- Approval or authorization information
- Escalation history
- Actions performed
- Customer communication or follow-up information
- Unresolved issues requiring additional monitoring or investigation

The case should only be considered closed when the required operational action has been completed or appropriately handed off, the current outcome has been communicated, and sufficient information exists to reconstruct how the case was handled.

When evidence, approvals, actions, and case notes are distributed across multiple systems, reconstructing the complete decision history may require additional manual effort during later review, dispute handling, or audit.
### Current-State Pain Points

The current-state workflow introduces several operational challenges:

- **Cross-system investigation** — employees may need to search multiple systems independently to reconstruct a single exception case.

- **Manual evidence correlation** — information from orders, transactions, payments, returns, fulfillment, and customer records may need to be manually connected.

- **Conflicting system information** — different systems may contain inconsistent statuses, timestamps, or records that require manual reconciliation.

- **Policy lookup and interpretation** — employees may need to locate the applicable policy and determine how it applies to the specific evidence in the case.

- **Repeated investigation during handoffs** — managers or specialist teams may need to review or reconstruct information already gathered by the frontline employee.

- **Permission and ownership boundaries** — resolution may be delayed when the employee investigating the case does not have authority or system access to perform the required action.

- **Technical escalation** — system or integration failures may introduce additional handoffs to IT or application support.

- **Customer follow-up** — unresolved cases may require repeated customer contacts when the outcome cannot be determined during the initial interaction.

- **Fragmented audit trail** — evidence, policy reasoning, approvals, actions, and communications may be distributed across multiple systems, making later reconstruction difficult.
