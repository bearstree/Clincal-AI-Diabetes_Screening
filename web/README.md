# Web client

FastAPI serves this dependency-free client at `/`. It sends four displayed fields to `/v1/predict`, stores nothing, and has no analytics. For a separate origin, set the `api-base-url` meta value and add that exact HTTPS origin to `CLINICAL_ALLOWED_ORIGINS`.
