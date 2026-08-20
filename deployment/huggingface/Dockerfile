FROM python:3.14-slim

WORKDIR /app
COPY pyproject.toml README-project.md ./
COPY src ./src
COPY deployment ./deployment
COPY web ./web
RUN python -m pip install --no-cache-dir . && useradd --create-home appuser

USER appuser
EXPOSE 7860
CMD ["uvicorn", "deployment.api.app:app", "--host", "0.0.0.0", "--port", "7860", "--no-access-log"]
