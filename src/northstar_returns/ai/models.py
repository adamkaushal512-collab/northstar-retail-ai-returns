from typing import Literal
from pydantic import BaseModel, Field

class EvidenceReference(BaseModel):
    source: Literal["OMS", "Returns", "Payments"]
    record_id: str
    field: str

class Explanation(BaseModel):
    case_id: str
    summary: str
    finding_codes: list[str]
    evidence: list[EvidenceReference]
    recommended_next_step: str
    requires_human_review: bool
    generation_mode: Literal["deterministic"] = "deterministic"

class AgentRequest(BaseModel):
    case_id: str = Field(min_length=1, max_length=100)
    order_id: str = Field(min_length=1, max_length=100)
