from sqlalchemy.orm import Session
from . import models, schemas


def create_assessment(db: Session, data: schemas.RiskAssessmentCreate) -> models.RiskAssessment:
    obj = models.RiskAssessment(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_assessment(db: Session, assessment_id: int) -> models.RiskAssessment | None:
    return db.get(models.RiskAssessment, assessment_id)


def list_assessments(db: Session, skip: int = 0, limit: int = 50) -> list[models.RiskAssessment]:
    return db.query(models.RiskAssessment).offset(skip).limit(limit).all()


def set_status(db: Session, assessment_id: int, status: str) -> None:
    obj = db.get(models.RiskAssessment, assessment_id)
    if obj:
        obj.status = status
        db.commit()


def set_score(db: Session, assessment_id: int, score: float) -> None:
    obj = db.get(models.RiskAssessment, assessment_id)
    if obj:
        obj.risk_score = score
        obj.status = "scored"
        db.commit()