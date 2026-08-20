"""Versioned prediction API for the promoted research model."""

import hashlib
import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, StrictBool

DEFAULT_MODEL_DIR = Path(__file__).parents[1] / "model"
DEFAULT_WEB_DIR = Path(__file__).parents[2] / "web"
SAFETY_NOTICE = "Educational research only; not a diagnosis or medical advice."


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    age_years: int = Field(ge=20, le=80)
    waist_cm: float = Field(ge=40, le=200)
    physically_active: StrictBool
    diastolic_bp: float = Field(ge=20, le=160)


class PredictionResponse(BaseModel):
    probability: float
    above_validation_threshold: bool
    threshold: float
    model_version: str
    outcome: str
    safety_notice: str


def _model_dir() -> Path:
    return Path(os.getenv("CLINICAL_MODEL_DIR", DEFAULT_MODEL_DIR))


@lru_cache(maxsize=1)
def load_bundle() -> dict[str, Any]:
    model_dir = _model_dir()
    manifest = json.loads((model_dir / "manifest.json").read_text(encoding="utf-8"))
    artifact = model_dir / manifest["artifact"]
    if hashlib.sha256(artifact.read_bytes()).hexdigest() != manifest["artifact_sha256"]:
        raise RuntimeError("Model artifact checksum mismatch")
    return dict(joblib.load(artifact))


def create_app(bundle: dict[str, Any] | None = None) -> FastAPI:
    app = FastAPI(title="Clinical Diabetes Screening Research API", version="1.0.0")
    origins = [
        value.strip()
        for value in os.getenv("CLINICAL_ALLOWED_ORIGINS", "").split(",")
        if value.strip()
    ]
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=False,
            allow_methods=["GET", "POST"],
            allow_headers=["Content-Type"],
        )

    def current_bundle() -> dict[str, Any]:
        try:
            return bundle if bundle is not None else load_bundle()
        except (FileNotFoundError, RuntimeError, ValueError) as error:
            raise HTTPException(status_code=503, detail="Model is not ready") from error

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/ready")
    def ready() -> dict[str, str]:
        current_bundle()
        return {"status": "ready"}

    @app.get("/metadata")
    def metadata() -> dict[str, Any]:
        loaded = current_bundle()
        return {
            "model_version": loaded["model_version"],
            "model_name": loaded["model_name"],
            "features": loaded["features"],
            "outcome": loaded["outcome_definition"],
            "safety_notice": loaded["safety_notice"],
        }

    @app.post("/v1/predict", response_model=PredictionResponse)
    def predict(request: PredictionRequest) -> PredictionResponse:
        loaded = current_bundle()
        values = request.model_dump()
        features = loaded["features"]
        frame = pd.DataFrame([{feature: values[feature] for feature in features}])
        probability = float(loaded["pipeline"].predict_proba(frame)[0, 1])
        threshold = float(loaded["threshold"])
        return PredictionResponse(
            probability=probability,
            above_validation_threshold=probability >= threshold,
            threshold=threshold,
            model_version=loaded["model_version"],
            outcome=loaded["outcome_definition"],
            safety_notice=loaded["safety_notice"],
        )

    web_dir = Path(os.getenv("CLINICAL_WEB_DIR", DEFAULT_WEB_DIR))
    if web_dir.is_dir():
        app.mount("/", StaticFiles(directory=web_dir, html=True), name="web")

    return app


app = create_app()
