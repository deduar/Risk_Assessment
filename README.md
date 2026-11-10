# Risk Assessment POC

Small proof-of-concept demonstrating the requested stack:
**Python 3.11 + FastAPI + Celery + PostgreSQL + Redis + Docker + GitLab CI**,
with a B2B-trade-flavored domain (risk assessment of a trade inquiry).

## Run locally

```bash
cd poc
docker compose up --build
```

API: http://localhost:8000  (Swagger: /docs)

## Try it

```bash
# create an assessment
curl -X POST http://localhost:8000/assessments \
  -H 'Content-Type: application/json' \
  -d '{"company_name":"Acme","country":"BE","amount":5000}'

# trigger scoring (returns task id)
curl -X POST http://localhost:8000/assessments/1/score

# poll task
curl http://localhost:8000/tasks/<task_id>

# get updated assessment
curl http://localhost:8000/assessments/1
```

## Tests

```bash
cd backend
pip install -r requirements.txt
pytest -q
```

## Architecture

```
client -> FastAPI (api) -> PostgreSQL
              |
              +-> Celery task (worker) via Redis -> updates PostgreSQL
```

## Production next steps (not in POC)
JWT auth (Sanctum-equivalent), GKE/ArgoCD deploy, monitoring & alerting,
real scoring model (Vertex AI), rate limiting, migrations via Alembic in CI.# Risk_Assessment
