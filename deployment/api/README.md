# Model API deployment

This clean folder contains the versioned FastAPI entry point and container definition. The promoted model lives separately in `deployment/model`.

```powershell
.\.venv\Scripts\uvicorn.exe deployment.api.app:app --host 127.0.0.1 --port 8000
```

- `GET /health` — process health.
- `GET /ready` — verifies that the checksummed model is loadable.
- `GET /metadata` — model version, features, outcome, and safety notice.
- `POST /v1/predict` — validated research probability and validation-derived flag.

Do not log request bodies or deploy without TLS, rate limiting, request-size limits, and platform-managed secrets.

