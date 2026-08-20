"""Select, evaluate, and package the Phase 4 model."""

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from clinical_ml.metadata import SAFETY_NOTICE
from clinical_ml.modeling import (
    MODEL_VERSION,
    bootstrap_intervals,
    candidates,
    choose_candidate,
    compare_candidates,
    dump_bundle,
    probability_metrics,
    save_evaluation_plots,
    select_threshold,
    subgroup_metrics,
    threshold_metrics,
)


def main() -> None:
    cohort_path = Path("data/processed/modeling_cohort.csv")
    cohort = pd.read_csv(cohort_path)
    train = cohort.loc[cohort["split"].eq("train")]
    validation = cohort.loc[cohort["split"].eq("validation")]
    test = cohort.loc[cohort["split"].eq("test")]

    comparison, fitted = compare_candidates(train, validation)
    selected_name = choose_candidate(comparison)
    selected_features = candidates()[selected_name][0]
    model = fitted[selected_name]
    validation_probability = model.predict_proba(validation[selected_features])[:, 1]
    threshold = select_threshold(
        validation["outcome"], validation_probability, validation["WTMECPRP"]
    )

    test_probability = model.predict_proba(test[selected_features])[:, 1]
    metrics = {
        "model_version": MODEL_VERSION,
        "selected_candidate": selected_name,
        "features": selected_features,
        "selection_rule": "lowest weighted validation Brier within 0.005 ROC-AUC of best",
        "candidate_comparison": comparison.to_dict(orient="records"),
        "validation_weighted": probability_metrics(
            validation["outcome"], validation_probability, validation["WTMECPRP"]
        ),
        "validation_threshold": threshold_metrics(
            validation["outcome"], validation_probability, threshold, validation["WTMECPRP"]
        ),
        "test_unweighted": probability_metrics(test["outcome"], test_probability),
        "test_weighted": probability_metrics(test["outcome"], test_probability, test["WTMECPRP"]),
        "test_threshold_unweighted": threshold_metrics(
            test["outcome"], test_probability, threshold
        ),
        "test_threshold_weighted": threshold_metrics(
            test["outcome"], test_probability, threshold, test["WTMECPRP"]
        ),
        "test_bootstrap_95_percent_interval": bootstrap_intervals(
            test["outcome"], test_probability
        ),
        "test_subgroups_unweighted": subgroup_metrics(test, test_probability),
    }

    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    metrics_path = report_dir / "model_metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    save_evaluation_plots(
        validation,
        validation_probability,
        test,
        test_probability,
        report_dir / "figures/phase4",
    )

    artifact_path = Path("deployment/model/clinical_diabetes_screening_v1.joblib")
    bundle = {
        "model_version": MODEL_VERSION,
        "model_name": selected_name,
        "pipeline": model,
        "features": selected_features,
        "threshold": threshold,
        "outcome_definition": "Current diabetes-status research definition",
        "safety_notice": SAFETY_NOTICE,
    }
    artifact_sha256 = dump_bundle(bundle, artifact_path)
    manifest = {
        "model_version": MODEL_VERSION,
        "artifact": artifact_path.name,
        "artifact_sha256": artifact_sha256,
        "training_data_sha256": hashlib.sha256(cohort_path.read_bytes()).hexdigest(),
        "created_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "selected_candidate": selected_name,
        "features": selected_features,
        "threshold": threshold,
        "metrics": "reports/model_metrics.json",
    }
    Path("deployment/model/manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(comparison.to_string(index=False))
    print("selected", selected_name, selected_features)
    print("threshold", threshold)
    print("test_weighted", metrics["test_weighted"])


if __name__ == "__main__":
    main()
