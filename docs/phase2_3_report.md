# Phase 2/3 Data and EDA Report

## Cohort flow

| Step | Participants remaining |
|---|---:|
| Source demographics | 15,560 |
| Age 20+ | 9,232 |
| Exclude recorded pregnancy | 9,145 |
| Positive MEC examination weight | 9,145 |
| Unambiguous combined outcome | 8,160 |
| Positive outcome | 1,701 |

The 985 otherwise eligible participants without a diagnosable positive outcome and without sufficient evidence for a negative combined label were excluded. Missing HbA1c was not treated as normal.

Unweighted positive prevalence is 20.85%; survey-weighted prevalence is 14.56%. The difference demonstrates why predictive-sample summaries and population estimands must be labeled separately.

## Leakage-safe split

| Split | N | Positive | Positive rate |
|---|---:|---:|---:|
| Train | 5,712 | 1,191 | 20.85% |
| Validation | 1,224 | 255 | 20.83% |
| Test | 1,224 | 255 | 20.83% |

Participants are unique and disjoint. The seed is 20260819. The random split is a limitation: the combined public-use file does not provide a clean independent temporal/site validation set. Preprocessing and feature selection use training data only; the test partition remains locked until Phase 4 final evaluation.

## Train-only feature ranking

| Rank | Feature | Mutual information | Missing |
|---:|---|---:|---:|
| 1 | Age | 0.05881 | 0.00% |
| 2 | Waist circumference | 0.04228 | 6.00% |
| 3 | BMI | 0.03877 | 2.87% |
| 4 | Physical activity | 0.00872 | 0.00% |
| 5 | Diastolic BP | 0.00716 | 10.91% |
| 6 | Systolic BP | 0.00702 | 10.91% |
| 7 | Sex | 0.00086 | 0.00% |
| 8 | Current smoking | 0.00069 | 0.05% |

Mutual information is a screening statistic, not causal importance and not final model evidence. The top six are provisionally frozen as the app-facing feature set for Phase 4 comparison. BMI and waist are strongly correlated (0.905); systolic and diastolic BP are moderately correlated (0.604). Regularized models and ablation tests must determine whether both members of each pair improve validation performance.

The provisional schema is preserved as `configs/app_features_phase3.json`. Phase 4 superseded it with the four-field `configs/app_features.json` contract.

## Selected-feature observations

| Feature mean | Outcome 0 | Outcome 1 |
|---|---:|---:|
| Age (years) | 48.80 | 62.12 |
| Waist (cm) | 98.95 | 110.01 |
| BMI (kg/m²) | 29.36 | 32.83 |
| Physically active (proportion) | 0.78 | 0.62 |
| Diastolic BP (mmHg) | 74.79 | 74.61 |
| Systolic BP (mmHg) | 123.47 | 131.32 |

These are descriptive, unadjusted sample means and do not imply causality.

## Subgroup inspection

Weighted prevalence varies across age and race/ethnicity groups. For age bands it is 3.25% (20–39), 15.25% (40–59), and 26.82% (60+). Race/ethnicity subgroup sample sizes range from 390 to 2,863 and weighted prevalence ranges from 13.24% to 19.29%. These differences are not fairness conclusions. Phase 4 must report performance, calibration, uncertainty, and sample sizes—not prevalence alone—for prespecified groups.

## Aggregate figures

- `reports/figures/phase3/outcome_prevalence.png`
- `reports/figures/phase3/feature_missingness.png`
- `reports/figures/phase3/feature_ranking.png`
