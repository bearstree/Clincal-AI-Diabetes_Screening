FROM python:3.14-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY deployment ./deployment
COPY web ./web
RUN python -m pip install --no-cache-dir . && useradd --create-home appuser

USER appuser
EXPOSE 8000
CMD ["uvicorn", "deployment.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
