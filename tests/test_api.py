import numpy as np
from fastapi.testclient import TestClient

from deployment.api.app import create_app


class FixedPipeline:
    def predict_proba(self, frame: object) -> np.ndarray:
        return np.array([[0.80, 0.20]])


def test_prediction_contract() -> None:
    bundle = {
        "model_version": "test",
        "model_name": "fixed",
        "features": ["age_years", "waist_cm", "physically_active", "diastolic_bp"],
        "threshold": 0.13,
        "outcome_definition": "research outcome",
        "safety_notice": "not medical advice",
        "pipeline": FixedPipeline(),
    }
    client = TestClient(create_app(bundle))
    response = client.post(
        "/v1/predict",
        json={
            "age_years": 50,
            "waist_cm": 100,
            "physically_active": True,
            "diastolic_bp": 75,
        },
    )
    assert response.status_code == 200
    assert response.json()["probability"] == 0.20
    assert response.json()["above_validation_threshold"] is True
    assert client.get("/health").status_code == 200
    assert client.get("/ready").status_code == 200
    assert client.get("/metadata").json()["model_version"] == "test"


def test_prediction_rejects_bad_or_extra_inputs() -> None:
    client = TestClient(create_app({}))
    response = client.post(
        "/v1/predict",
        json={
            "age_years": 19,
            "waist_cm": 100,
            "physically_active": True,
            "diastolic_bp": 75,
            "name": "not accepted",
        },
    )
    assert response.status_code == 422


def test_web_client_is_served() -> None:
    response = TestClient(create_app({})).get("/")
    assert response.status_code == 200
    assert "Diabetes screening research tool" in response.text
