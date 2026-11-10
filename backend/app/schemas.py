from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RiskAssessmentBase(BaseModel):
    company_name: str
    country: str
    amount: float


class RiskAssessmentCreate(RiskAssessmentBase):
    pass


class RiskAssessmentRead(RiskAssessmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    risk_score: float | None = None
    created_at: datetime