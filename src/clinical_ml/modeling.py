"""Concise model selection, evaluation, and packaging utilities."""

from collections.abc import Iterable
from pathlib import Path
from typing import Any

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    log_loss,
    roc_auc_score,
    roc_curve,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

MODEL_VERSION = "1.0.0"
TARGET_SENSITIVITY = 0.80
SIX_FEATURES = [
    "age_years",
    "waist_cm",
    "bmi",
    "physically_active",
    "diastolic_bp",
    "systolic_bp",
]


def _logistic() -> Pipeline:
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(C=0.01, max_iter=2_000)),
        ]
    )


def candidates() -> dict[str, tuple[list[str], Pipeline]]:
    """Return prespecified candidates and redundancy ablations."""
    return {
        "prevalence_baseline": (
            SIX_FEATURES,
            Pipeline([("imputer", SimpleImputer(strategy="median")), ("model", DummyClassifier())]),
        ),
        "logistic_six": (SIX_FEATURES, _logistic()),
        "logistic_no_diastolic": (
            [feature for feature in SIX_FEATURES if feature != "diastolic_bp"],
            _logistic(),
        ),
        "logistic_no_bmi": ([feature for feature in SIX_FEATURES if feature != "bmi"], _logistic()),
        "logistic_compact_diastolic": (
            ["age_years", "waist_cm", "physically_active", "diastolic_bp"],
            _logistic(),
        ),
        "logistic_compact_systolic": (
            ["age_years", "waist_cm", "physically_active", "systolic_bp"],
            _logistic(),
        ),
        "hist_gradient_six": (
            SIX_FEATURES,
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="median")),
                    (
                        "model",
                        HistGradientBoostingClassifier(
                            learning_rate=0.05,
                            max_iter=150,
                            max_leaf_nodes=15,
                            l2_regularization=1.0,
                            random_state=20260819,
                        ),
                    ),
                ]
            ),
        ),
    }


def normalized_weights(frame: pd.DataFrame) -> np.ndarray:
    weights = frame["WTMECPRP"].to_numpy(dtype=float)
    normalized: np.ndarray = weights / float(weights.mean())
    return normalized


def fit_pipeline(model: Pipeline, frame: pd.DataFrame, features: list[str]) -> Pipeline:
    model.fit(
        frame[features],
        frame["outcome"],
        model__sample_weight=normalized_weights(frame),
    )
    return model


def probability_metrics(
    outcome: pd.Series, probability: np.ndarray, weights: Iterable[float] | None = None
) -> dict[str, float]:
    sample_weight = None if weights is None else np.asarray(list(weights), dtype=float)
    return {
        "roc_auc": float(roc_auc_score(outcome, probability, sample_weight=sample_weight)),
        "pr_auc": float(average_precision_score(outcome, probability, sample_weight=sample_weight)),
        "brier": float(brier_score_loss(outcome, probability, sample_weight=sample_weight)),
        "log_loss": float(log_loss(outcome, probability, sample_weight=sample_weight)),
    }


def compare_candidates(
    train: pd.DataFrame, validation: pd.DataFrame
) -> tuple[pd.DataFrame, dict[str, Pipeline]]:
    rows: list[dict[str, Any]] = []
    fitted: dict[str, Pipeline] = {}
    for name, (features, model) in candidates().items():
        fitted[name] = fit_pipeline(model, train, features)
        probability = fitted[name].predict_proba(validation[features])[:, 1]
        metrics = probability_metrics(validation["outcome"], probability, validation["WTMECPRP"])
        rows.append({"candidate": name, "feature_count": len(features), **metrics})
    return pd.DataFrame(rows).sort_values(["brier", "roc_auc"], ascending=[True, False]), fitted


def choose_candidate(comparison: pd.DataFrame) -> str:
    """Choose lowest Brier candidate within 0.005 weighted ROC-AUC of the best."""
    eligible = comparison.loc[comparison["roc_auc"].ge(comparison["roc_auc"].max() - 0.005)]
    return str(eligible.sort_values(["brier", "feature_count"]).iloc[0]["candidate"])


def select_threshold(outcome: pd.Series, probability: np.ndarray, weights: pd.Series) -> float:
    false_positive, sensitivity, thresholds = roc_curve(outcome, probability, sample_weight=weights)
    eligible = np.flatnonzero(sensitivity >= TARGET_SENSITIVITY)
    best = eligible[np.argmin(false_positive[eligible])]
    return float(thresholds[best])


def threshold_metrics(
    outcome: pd.Series,
    probability: np.ndarray,
    threshold: float,
    weights: Iterable[float] | None = None,
) -> dict[str, float]:
    sample_weight = None if weights is None else np.asarray(list(weights), dtype=float)
    predicted = probability >= threshold
    tn, fp, fn, tp = confusion_matrix(
        outcome, predicted, labels=[0, 1], sample_weight=sample_weight
    ).ravel()
    return {
        "threshold": threshold,
        "sensitivity": float(tp / (tp + fn)),
        "specificity": float(tn / (tn + fp)),
        "ppv": float(tp / (tp + fp)),
        "npv": float(tn / (tn + fn)),
    }


def bootstrap_intervals(
    outcome: pd.Series, probability: np.ndarray, repetitions: int = 500
) -> dict[str, list[float]]:
    rng = np.random.default_rng(20260819)
    values: dict[str, list[float]] = {"roc_auc": [], "brier": []}
    indices = np.arange(len(outcome))
    y = outcome.to_numpy()
    for _ in range(repetitions):
        sample = rng.choice(indices, size=len(indices), replace=True)
        if np.unique(y[sample]).size < 2:
            continue
        values["roc_auc"].append(float(roc_auc_score(y[sample], probability[sample])))
        values["brier"].append(float(brier_score_loss(y[sample], probability[sample])))
    return {
        name: [float(value) for value in np.quantile(samples, [0.025, 0.975])]
        for name, samples in values.items()
    }


def subgroup_metrics(frame: pd.DataFrame, probability: np.ndarray) -> list[dict[str, Any]]:
    evaluated = frame.copy()
    evaluated["probability"] = probability
    evaluated["age_group"] = pd.cut(
        evaluated["age_years"], [19, 39, 59, 80], labels=["20-39", "40-59", "60+"]
    )
    race_labels = {
        1: "Mexican American",
        2: "Other Hispanic",
        3: "Non-Hispanic White",
        4: "Non-Hispanic Black",
        6: "Non-Hispanic Asian",
        7: "Other/multiracial",
    }
    evaluated["race_group"] = evaluated["RIDRETH3"].map(race_labels)
    groups = {"age": "age_group", "sex": "sex_female", "race_ethnicity": "race_group"}
    rows: list[dict[str, Any]] = []
    for family, column in groups.items():
        for value, group in evaluated.groupby(column, observed=True):
            if group["outcome"].nunique() < 2:
                continue
            metrics = probability_metrics(group["outcome"], group["probability"].to_numpy())
            rows.append({"family": family, "group": str(value), "n": len(group), **metrics})
    return rows


def save_evaluation_plots(
    validation: pd.DataFrame,
    validation_probability: np.ndarray,
    test: pd.DataFrame,
    test_probability: np.ndarray,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(1, 2, figsize=(10, 4))
    for label, frame, probability in (
        ("Validation", validation, validation_probability),
        ("Test", test, test_probability),
    ):
        false_positive, sensitivity, _ = roc_curve(frame["outcome"], probability)
        axes[0].plot(false_positive, sensitivity, label=label)
        bins = pd.qcut(probability, q=10, duplicates="drop")
        calibration = (
            pd.DataFrame({"outcome": frame["outcome"], "probability": probability})
            .groupby(bins, observed=True)
            .mean()
        )
        axes[1].plot(calibration["probability"], calibration["outcome"], marker="o", label=label)
    axes[0].plot([0, 1], [0, 1], "--", color="grey")
    axes[0].set(title="ROC curves", xlabel="False-positive rate", ylabel="Sensitivity")
    axes[1].plot([0, 1], [0, 1], "--", color="grey")
    axes[1].set(title="Calibration", xlabel="Mean predicted probability", ylabel="Observed rate")
    for axis in axes:
        axis.legend()
    figure.tight_layout()
    figure.savefig(output_dir / "model_evaluation.png", dpi=160)
    plt.close(figure)


def dump_bundle(bundle: dict[str, Any], path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, path, compress=3)
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()
