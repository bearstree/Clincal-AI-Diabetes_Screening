"""Validated NHANES cohort construction for model development."""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import train_test_split

RAW_FILES = (
    "P_DEMO.xpt",
    "P_DIQ.xpt",
    "P_GHB.xpt",
    "P_BMX.xpt",
    "P_BPXO.xpt",
    "P_PAQ.xpt",
    "P_SMQ.xpt",
)
CANDIDATE_FEATURES = (
    "age_years",
    "sex_female",
    "bmi",
    "waist_cm",
    "systolic_bp",
    "diastolic_bp",
    "current_smoker",
    "physically_active",
)
DISCRETE_FEATURES = frozenset({"sex_female", "current_smoker", "physically_active"})
RANDOM_STATE = 20260819


def load_components(raw_dir: Path) -> pd.DataFrame:
    """Load verified XPT components and enforce one row per participant."""
    frames: dict[str, pd.DataFrame] = {}
    for name in RAW_FILES:
        path = raw_dir / name
        if not path.is_file():
            raise FileNotFoundError(f"Missing source file: {path}")
        frame = pd.read_sas(path, format="xport")
        if "SEQN" not in frame or frame["SEQN"].duplicated().any():
            raise ValueError(f"{name} must contain unique SEQN values")
        frames[name] = frame

    merged = frames[RAW_FILES[0]]
    for name in RAW_FILES[1:]:
        merged = merged.merge(frames[name], on="SEQN", how="left", validate="one_to_one")
    return merged


def _current_smoker(frame: pd.DataFrame) -> pd.Series:
    conditions = (
        frame["SMQ020"].eq(2),
        frame["SMQ020"].eq(1) & frame["SMQ040"].isin([1, 2]),
        frame["SMQ020"].eq(1) & frame["SMQ040"].eq(3),
    )
    return pd.Series(np.select(conditions, [0.0, 1.0, 0.0], default=np.nan), index=frame.index)


def _physically_active(frame: pd.DataFrame) -> pd.Series:
    questions = ["PAQ605", "PAQ620", "PAQ635", "PAQ650", "PAQ665"]
    answers = frame[questions]
    any_valid = answers.isin([1, 2]).any(axis=1)
    return pd.Series(
        np.where(answers.eq(1).any(axis=1), 1.0, np.where(any_valid, 0.0, np.nan)),
        index=frame.index,
    )


def build_cohort(merged: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Create the adult analytical cohort without treating unknown outcomes as negative."""
    counts = {"source_demographics": len(merged)}
    frame = merged.loc[merged["RIDAGEYR"].ge(20)].copy()
    counts["adults_age_20_plus"] = len(frame)

    frame = frame.loc[frame["RIDEXPRG"].ne(1)]
    counts["after_pregnancy_exclusion"] = len(frame)
    frame = frame.loc[frame["WTMECPRP"].gt(0)]
    counts["positive_exam_weight"] = len(frame)

    positive = frame["DIQ010"].eq(1) | frame["LBXGH"].ge(6.5)
    negative = frame["DIQ010"].isin([2, 3]) & frame["LBXGH"].lt(6.5)
    frame = frame.loc[positive | negative].copy()
    frame["outcome"] = positive.loc[frame.index].astype("int8")
    counts["observable_outcome"] = len(frame)
    counts["positive_outcome"] = int(frame["outcome"].sum())

    frame["age_years"] = frame["RIDAGEYR"]
    frame["sex_female"] = frame["RIAGENDR"].map({1: 0.0, 2: 1.0})
    frame["height_cm"] = frame["BMXHT"]
    frame["weight_kg"] = frame["BMXWT"]
    frame["bmi"] = frame["BMXBMI"]
    frame["waist_cm"] = frame["BMXWAIST"]
    frame["systolic_bp"] = frame[["BPXOSY1", "BPXOSY2", "BPXOSY3"]].mean(axis=1)
    frame["diastolic_bp"] = frame[["BPXODI1", "BPXODI2", "BPXODI3"]].mean(axis=1)
    frame["current_smoker"] = _current_smoker(frame)
    frame["physically_active"] = _physically_active(frame)

    columns = [
        "SEQN",
        "outcome",
        *CANDIDATE_FEATURES,
        "height_cm",
        "weight_kg",
        "RIDRETH3",
        "WTMECPRP",
        "SDMVPSU",
        "SDMVSTRA",
    ]
    cohort = frame[columns].sort_values("SEQN").reset_index(drop=True)
    validate_cohort(cohort)
    return cohort, counts


def validate_cohort(cohort: pd.DataFrame) -> None:
    """Fail fast on structural errors and implausible derived values."""
    if cohort["SEQN"].duplicated().any() or not set(cohort["outcome"].unique()) <= {0, 1}:
        raise ValueError("Cohort keys must be unique and outcome must be binary")
    if not cohort["WTMECPRP"].gt(0).all():
        raise ValueError("Every included participant must have a positive examination weight")

    ranges = {
        "age_years": (20, 80),
        "bmi": (10, 100),
        "waist_cm": (40, 200),
        "systolic_bp": (40, 260),
        "diastolic_bp": (20, 160),
    }
    for column, (lower, upper) in ranges.items():
        observed = cohort[column].dropna()
        if not observed.between(lower, upper).all():
            raise ValueError(f"{column} contains values outside {lower}–{upper}")


def add_splits(cohort: pd.DataFrame) -> pd.DataFrame:
    """Create deterministic participant-level 70/15/15 stratified splits."""
    train_index, holdout_index = train_test_split(
        cohort.index,
        test_size=0.30,
        random_state=RANDOM_STATE,
        stratify=cohort["outcome"],
    )
    validation_index, test_index = train_test_split(
        holdout_index,
        test_size=0.50,
        random_state=RANDOM_STATE,
        stratify=cohort.loc[holdout_index, "outcome"],
    )
    result = cohort.copy()
    result["split"] = ""
    result.loc[train_index, "split"] = "train"
    result.loc[validation_index, "split"] = "validation"
    result.loc[test_index, "split"] = "test"
    if result["split"].eq("").any():
        raise RuntimeError("Every participant must receive exactly one split")
    return result


def rank_features(cohort: pd.DataFrame) -> pd.DataFrame:
    """Rank candidate inputs using training data only; no test-set feature selection."""
    train = cohort.loc[cohort["split"].eq("train")]
    features = list(CANDIDATE_FEATURES)
    prepared = train[features].fillna(train[features].median())
    discrete = [feature in DISCRETE_FEATURES for feature in features]
    scores = mutual_info_classif(
        prepared,
        train["outcome"],
        discrete_features=discrete,
        random_state=RANDOM_STATE,
    )
    ranking = pd.DataFrame(
        {
            "feature": features,
            "mutual_information": scores,
            "missing_percent": cohort[features].isna().mean().mul(100).to_numpy(),
        }
    )
    return ranking.sort_values("mutual_information", ascending=False).reset_index(drop=True)


def prepare_dataset(raw_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, int]]:
    """Run the complete Phase 2/3 preprocessing path in memory."""
    cohort, counts = build_cohort(load_components(raw_dir))
    cohort = add_splits(cohort)
    return cohort, rank_features(cohort), counts
