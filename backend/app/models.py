from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime
from .db import Base


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), nullable=False)
    country = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    risk_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))