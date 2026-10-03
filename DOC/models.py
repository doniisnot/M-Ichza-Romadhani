"""
models.py — Pydantic v2 data contract
AI Credit Scoring Engine Koperasi
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRole(str, Enum):
    member = "member"
    credit_analyst = "credit_analyst"
    admin = "admin"
    auditor = "auditor"


class LoanStatus(str, Enum):
    pending_review = "Pending Review"
    diterima = "Diterima"
    ditolak = "Ditolak"


class YesNo(str, Enum):
    yes = "yes"
    no = "no"


class Prediction(str, Enum):
    yes = "Yes"
    no = "No"


class Recommendation(str, Enum):
    diterima = "Diterima"
    ditolak = "Ditolak"


class AnalystDecision(str, Enum):
    approved = "approved"
    rejected = "rejected"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class LoginRequest(StrictModel):
    email: EmailStr
    password: str = Field(min_length=1)


class LoginResponse(BaseModel):
    token: str
    role: UserRole


class CreateMemberRequest(StrictModel):
    full_name: str = Field(min_length=1)
    member_number: str = Field(min_length=1)


class MemberResponse(BaseModel):
    id: int
    member_number: str
    full_name: str


class CreateLoanRequest(StrictModel):
    amount: Decimal = Field(gt=0)


class LoanResponse(BaseModel):
    id: int
    member_id: int
    amount: Decimal
    status: LoanStatus
    created_at: datetime


class ScoringPredictRequest(StrictModel):
    """
    Tepat empat field input AI.
    Field tambahan ditolak dengan HTTP 422 melalui extra='forbid'.
    """
    job: str = Field(min_length=1)
    education: str = Field(min_length=1)
    housing: YesNo
    loan: YesNo

    @field_validator("job", "education")
    @classmethod
    def non_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value tidak boleh kosong")
        return value.strip()


class ScoringModelInfo(BaseModel):
    name: str
    algorithm: str
    version: str


class ScoringPredictResponse(BaseModel):
    success: bool
    prediction: Prediction
    recommendation: Recommendation
    processing_time_ms: int = Field(ge=0)
    model: ScoringModelInfo
    fallback: bool = False
    fallback_reason: Optional[str] = None
    loan_status_unchanged: bool = True


class AnalystDecisionRequest(StrictModel):
    decision: AnalystDecision
    notes: Optional[str] = None


class AuditLogResponse(BaseModel):
    id: int
    action: str
    details: str
    created_at: datetime


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail


# Persistence-oriented models / kontrak internal.
class UserDB(BaseModel):
    id: int
    email: EmailStr
    password_hash: str
    role: UserRole


class MemberDB(BaseModel):
    id: int
    member_number: str
    full_name: str


class LoanApplicationDB(BaseModel):
    id: int
    member_id: int
    amount: Decimal
    status: LoanStatus
    created_at: datetime


class AIScoringAttributesDB(BaseModel):
    id: int
    loan_application_id: int
    job: str
    education: str
    housing: YesNo
    loan: YesNo


class AIScoringResultDB(BaseModel):
    id: int
    loan_application_id: int
    success: bool
    prediction: Prediction
    recommendation: Recommendation
    processing_time_ms: int
    model_name: str
    algorithm: str
    model_version: str
    fallback: bool = False
    fallback_reason: Optional[str] = None
    loan_status_unchanged: bool = True


class AnalystDecisionDB(BaseModel):
    id: int
    loan_application_id: int
    analyst_user_id: int
    decision: AnalystDecision
    notes: Optional[str] = None
    is_override: bool


class AuditLogDB(BaseModel):
    id: int
    action: str
    details: str
    created_at: datetime
    actor_user_id: Optional[int] = None
