import os
import time
from celery import Celery
from .db import SessionLocal
from . import crud

BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

celery_app = Celery("poc", broker=BROKER_URL, backend=RESULT_BACKEND)
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = ["json"]


@celery_app.task(name="score_assessment")
def score_assessment(assessment_id: int) -> dict:
    """Simple heuristic risk score (0-100). Replace with real model later."""
    time.sleep(2)  # simulate work
    db = SessionLocal()
    try:
        a = crud.get_assessment(db, assessment_id)
        if not a:
            return {"status": "not_found"}
        crud.set_status(db, assessment_id, "scoring")
        # toy scoring: higher amount -> higher risk; certain countries bump
        score = min(100.0, (a.amount / 10000.0) * 40 + 10)
        high_risk = {"IR", "KP", "SY", "RU"}
        if a.country.upper() in high_risk:
            score = min(100.0, score + 30)
        crud.set_score(db, assessment_id, round(score, 2))
        return {"status": "scored", "risk_score": score}
    finally:
        db.close()