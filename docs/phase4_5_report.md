# Phase 4/5 Model and API Report

## Model decision

The selected regularized logistic model has four inputs and the best weighted validation Brier score among candidates within 0.005 ROC-AUC of the best model. The six-feature logistic candidate reached ROC-AUC 0.7722 and Brier 0.1054; the compact selected model reached 0.7716 and 0.1047. Histogram gradient boosting did not justify its additional complexity (ROC-AUC 0.7675, Brier 0.1067).

BMI and systolic pressure were removed after validation ablations. The app/API contract is now age, waist circumference, physical activity, and diastolic blood pressure.

## Locked-test result

The test partition was evaluated only after the candidate, features, hyperparameter, and threshold rule were frozen. Weighted test ROC-AUC was 0.771 and Brier score was 0.117. Weighted sensitivity at the validation-selected threshold was 0.771, below the 0.80 validation target; this is explicitly disclosed.

## API package

The API is implemented in `deployment/api/app.py` and exposes:

- `GET /health`
- `GET /ready`
- `GET /metadata`
- `POST /v1/predict`

Pydantic rejects missing, extra, wrong-type, and out-of-range inputs. The API recomposes features in the artifact's stored order, returns probability, threshold flag, version, outcome wording, and safety notice, and does not log request bodies. The model artifact checksum is verified before joblib loading.

## Local commands

```powershell
.\.venv\Scripts\python.exe scripts\train_phase4.py
.\.venv\Scripts\python.exe -m scripts.export_openapi
.\.venv\Scripts\uvicorn.exe deployment.api.app:app --host 127.0.0.1 --port 8000
```

Container build from repository root:

```powershell
docker build -f deployment/api/Dockerfile -t clinical-risk-api:1.0.0 .
```

Deployment to external infrastructure, TLS termination, rate limiting, monitoring, and public hosting are not part of Phase 5 and have not been performed.
