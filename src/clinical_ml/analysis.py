"""Aggregate Phase 2/3 outputs and plots; never exports participant rows to docs."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from clinical_ml.data import CANDIDATE_FEATURES

APP_FEATURE_COUNT = 6


def save_figures(cohort: pd.DataFrame, ranking: pd.DataFrame, figure_dir: Path) -> None:
    figure_dir.mkdir(parents=True, exist_ok=True)

    missing = cohort[list(CANDIDATE_FEATURES)].isna().mean().mul(100).sort_values()
    ax = missing.plot.barh(figsize=(8, 4), color="#2F6B8A")
    ax.set(xlabel="Missing (%)", ylabel="", title="Candidate-feature missingness")
    ax.figure.tight_layout()
    ax.figure.savefig(figure_dir / "feature_missingness.png", dpi=160)
    plt.close(ax.figure)

    ordered = ranking.sort_values("mutual_information")
    ax = ordered.plot.barh(
        x="feature", y="mutual_information", legend=False, figsize=(8, 4), color="#D97706"
    )
    ax.set(xlabel="Training-only mutual information", ylabel="", title="Feature ranking")
    ax.figure.tight_layout()
    ax.figure.savefig(figure_dir / "feature_ranking.png", dpi=160)
    plt.close(ax.figure)

    prevalence = pd.Series(
        {
            "Unweighted": cohort["outcome"].mean(),
            "Survey-weighted": np.average(cohort["outcome"], weights=cohort["WTMECPRP"]),
        }
    ).mul(100)
    ax = prevalence.plot.bar(figsize=(6, 4), color=["#64748B", "#0F766E"])
    ax.set(ylabel="Positive outcome (%)", xlabel="", title="Cohort outcome prevalence")
    ax.tick_params(axis="x", rotation=0)
    ax.figure.tight_layout()
    ax.figure.savefig(figure_dir / "outcome_prevalence.png", dpi=160)
    plt.close(ax.figure)


def save_app_schema(selected: list[str], path: Path) -> None:
    fields = {
        "age_years": {
            "name": "age_years",
            "widget": "integer_stepper",
            "label": "Age",
            "unit": "years",
            "minimum": 20,
            "maximum": 80,
        },
        "bmi": {
            "name": "bmi",
            "widget": "derived_read_only",
            "label": "Body mass index",
            "unit": "kg/m²",
            "derive_from": ["height_cm", "weight_kg"],
        },
        "waist_cm": {
            "name": "waist_cm",
            "widget": "decimal_input",
            "label": "Waist circumference",
            "unit": "cm",
            "minimum": 40,
            "maximum": 200,
        },
        "systolic_bp": {
            "name": "systolic_bp",
            "widget": "integer_input",
            "label": "Systolic blood pressure",
            "unit": "mmHg",
            "minimum": 40,
            "maximum": 260,
        },
        "diastolic_bp": {
            "name": "diastolic_bp",
            "widget": "integer_input",
            "label": "Diastolic blood pressure",
            "unit": "mmHg",
            "minimum": 20,
            "maximum": 160,
        },
        "physically_active": {
            "name": "physically_active",
            "widget": "yes_no",
            "label": "Regular moderate/vigorous activity or active transport",
            "help": "At least 10 continuous minutes in a typical week",
        },
        "current_smoker": {
            "name": "current_smoker",
            "widget": "yes_no",
            "label": "Currently smoke cigarettes",
        },
        "sex_female": {"name": "sex_female", "widget": "yes_no", "label": "Female sex"},
    }
    display_order = [
        "age_years",
        "bmi",
        "waist_cm",
        "systolic_bp",
        "diastolic_bp",
        "physically_active",
        "current_smoker",
        "sex_female",
    ]
    payload = {
        "schema_version": "0.1.0",
        "selected_model_features": selected,
        "form_fields": [fields[name] for name in display_order if name in selected],
        "supporting_inputs": {
            "height_cm": {
                "widget": "decimal_input",
                "label": "Height",
                "unit": "cm",
                "minimum": 100,
                "maximum": 250,
            },
            "weight_kg": {
                "widget": "decimal_input",
                "label": "Weight",
                "unit": "kg",
                "minimum": 20,
                "maximum": 300,
            },
        },
        "safety_text": (
            "Educational research only; this result is not a diagnosis or medical advice."
        ),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def selected_app_features(ranking: pd.DataFrame) -> list[str]:
    return [str(value) for value in ranking.head(APP_FEATURE_COUNT)["feature"].tolist()]
