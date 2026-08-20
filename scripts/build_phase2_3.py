"""Build validated Phase 2/3 analytical outputs."""

from pathlib import Path

from clinical_ml.analysis import save_app_schema, save_figures, selected_app_features
from clinical_ml.data import prepare_dataset


def main() -> None:
    raw = Path("data/raw/nhanes_2017_2020")
    processed = Path("data/processed")
    figures = Path("reports/figures/phase3")
    processed.mkdir(parents=True, exist_ok=True)

    cohort, ranking, counts = prepare_dataset(raw)
    cohort.to_csv(processed / "modeling_cohort.csv", index=False)
    ranking.to_csv(processed / "feature_ranking.csv", index=False)
    save_figures(cohort, ranking, figures)
    selected = selected_app_features(ranking)
    save_app_schema(selected, Path("configs/app_features_phase3.json"))

    print("cohort_counts", counts)
    print("split_counts", cohort["split"].value_counts().to_dict())
    print("selected_app_features", selected)


if __name__ == "__main__":
    main()
