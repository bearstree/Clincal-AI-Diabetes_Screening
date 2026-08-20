import pandas as pd

from clinical_ml.modeling import choose_candidate


def test_selection_prefers_calibration_within_auc_margin() -> None:
    comparison = pd.DataFrame(
        [
            {"candidate": "complex", "roc_auc": 0.80, "brier": 0.12, "feature_count": 6},
            {"candidate": "compact", "roc_auc": 0.797, "brier": 0.10, "feature_count": 4},
            {"candidate": "too_low", "roc_auc": 0.79, "brier": 0.09, "feature_count": 2},
        ]
    )
    assert choose_candidate(comparison) == "compact"
