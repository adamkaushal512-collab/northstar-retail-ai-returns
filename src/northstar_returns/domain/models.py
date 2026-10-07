from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class RefundStatus(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ReturnStatus(str, Enum):
    OPEN = "OPEN"
    APPROVED = "APPROVED"
    COMPLETED = "COMPLETED"


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class OrderEvidence(BaseModel):
    order_id: str
    customer_id: str
    total_amount: float = Field(ge=0)
    payment_transaction_id: str


class ReturnEvidence(BaseModel):
    return_id: str
    order_id: str
    status: ReturnStatus
    refund_amount: float = Field(ge=0)


class PaymentEvidence(BaseModel):
    payment_transaction_id: str
    refund_id: Optional[str] = None
    refund_status: RefundStatus
    refund_amount: float = Field(ge=0)
    failure_reason: Optional[str] = None


class InvestigationFinding(BaseModel):
    code: str
    severity: Severity
    summary: str
    evidence_sources: List[str]


class InvestigationResult(BaseModel):
    case_id: str
    order: OrderEvidence
    return_case: ReturnEvidence
    payment: PaymentEvidence
    findings: List[InvestigationFinding]
    recommended_next_step: str
    human_approval_required: bool
