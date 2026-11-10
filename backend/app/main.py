from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from celery.result import AsyncResult

from .db import get_db, Base, engine
from . import models, schemas, crud
from .tasks import celery_app, score_assessment

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Risk Assessment POC", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/assessments", response_model=list[schemas.RiskAssessmentRead])
def list_assessments(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_assessments(db, skip, limit)


@app.post("/assessments", response_model=schemas.RiskAssessmentRead, status_code=201)
def create_assessment(payload: schemas.RiskAssessmentCreate, db: Session = Depends(get_db)):
    return crud.create_assessment(db, payload)


@app.get("/assessments/{assessment_id}", response_model=schemas.RiskAssessmentRead)
def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    obj = crud.get_assessment(db, assessment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@app.post("/assessments/{assessment_id}/score")
def trigger_score(assessment_id: int, db: Session = Depends(get_db)):
    obj = crud.get_assessment(db, assessment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    crud.set_status(db, assessment_id, "queued")
    task = score_assessment.delay(assessment_id)
    return {"task_id": task.id}


@app.get("/tasks/{task_id}")
def task_status(task_id: str):
    res = AsyncResult(task_id, app=celery_app)
    return {"task_id": task_id, "state": res.state, "result": res.result if res.ready() else None}