from pathlib import Path

from clinical_ml import PROJECT_STAGE, SAFETY_NOTICE


def test_safety_metadata_is_explicit() -> None:
    assert PROJECT_STAGE == "phase-5-model-api"
    assert "not a diagnosis" in SAFETY_NOTICE


def test_raw_data_are_git_ignored() -> None:
    ignore = Path(".gitignore").read_text(encoding="utf-8")
    assert "data/raw/**" in ignore


def test_deployment_boundaries_exist() -> None:
    assert Path("deployment/api/README.md").is_file()
    assert Path("deployment/model/README.md").is_file()
