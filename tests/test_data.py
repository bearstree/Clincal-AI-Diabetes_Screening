import json

import numpy as np
import pandas as pd

from clinical_ml.analysis import save_app_schema, selected_app_features
from clinical_ml.data import _current_smoker, _physically_active, add_splits


def test_smoking_skip_pattern_is_recoded() -> None:
    frame = pd.DataFrame({"SMQ020": [2, 1, 1, 1, 7], "SMQ040": [np.nan, 1, 2, 3, np.nan]})
    result = _current_smoker(frame)
    assert result.iloc[:4].tolist() == [0, 1, 1, 0]
    assert np.isnan(result.iloc[4])


def test_activity_is_yes_if_any_domain_is_yes() -> None:
    columns = ["PAQ605", "PAQ620", "PAQ635", "PAQ650", "PAQ665"]
    frame = pd.DataFrame([[2, 2, 1, 2, 2], [2, 2, 2, 2, 2], [np.nan] * 5], columns=columns)
    result = _physically_active(frame)
    assert result.iloc[:2].tolist() == [1, 0]
    assert np.isnan(result.iloc[2])


def test_split_is_complete_disjoint_and_stratified() -> None:
    cohort = pd.DataFrame({"SEQN": range(200), "outcome": [0] * 160 + [1] * 40})
    result = add_splits(cohort)
    assert result["split"].value_counts().to_dict() == {
        "train": 140,
        "validation": 30,
        "test": 30,
    }
    assert result.groupby("split")["outcome"].mean().round(2).eq(0.20).all()


def test_app_schema_covers_selected_features(tmp_path) -> None:
    ranking = pd.DataFrame(
        {"feature": ["age_years", "bmi", "systolic_bp"], "mutual_information": [3, 2, 1]}
    )
    selected = selected_app_features(ranking)
    path = tmp_path / "schema.json"
    save_app_schema(selected, path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["selected_model_features"] == selected
    assert {field["name"] for field in payload["form_fields"]} == set(selected)
