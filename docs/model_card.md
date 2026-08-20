# Model Card: Clinical Diabetes Screening Research Model 1.0.0

## Summary

Regularized logistic regression estimating the project's current diabetes-status research label from age, waist circumference, physical activity, and diastolic blood pressure. The complete median-imputation and standardization pipeline is packaged with the estimator.

This model is for education and portfolio demonstration only. It is not a diagnosis, future-risk model, medical advice, clinically validated system, or medical device.

## Training and selection

- Source: NHANES 2017–March 2020 pre-pandemic public-use files.
- Cohort: 8,160 adults; train 5,712, validation 1,224, locked test 1,224.
- Training used normalized combined-cycle MEC weights.
- Candidates: prevalence baseline, regularized logistic variants/ablations, and histogram gradient boosting.
- Selection rule: lowest weighted validation Brier score among candidates within 0.005 ROC-AUC of the best validation ROC-AUC.
- Selected: `logistic_compact_diastolic`, four features, `C=0.01`.

## Performance

| Partition/weighting | ROC-AUC | PR-AUC | Brier | Log loss |
|---|---:|---:|---:|---:|
| Validation, survey-weighted | 0.772 | 0.325 | 0.1047 | 0.3411 |
| Test, survey-weighted | 0.771 | 0.396 | 0.1171 | 0.3764 |
| Test, unweighted | 0.774 | 0.431 | 0.1449 | 0.4420 |

Participant-bootstrap unweighted 95% intervals on test: ROC-AUC 0.744–0.803; Brier 0.1326–0.1590. These are not complex-survey confidence intervals.

## Screening threshold

Threshold 0.1301 was selected on weighted validation data as the lowest-false-positive operating point reaching at least 80% sensitivity.

| Partition | Sensitivity | Specificity | PPV | NPV |
|---|---:|---:|---:|---:|
| Validation, weighted | 0.801 | 0.628 | 0.253 | 0.953 |
| Test, weighted | 0.771 | 0.656 | 0.300 | 0.937 |
| Test, unweighted | 0.827 | 0.613 | 0.360 | 0.931 |

The target sensitivity did not fully transport to weighted test data. The threshold is therefore a research screening flag, not a clinical decision boundary.

## Subgroup observations

Unweighted test ROC-AUC was 0.789 for ages 20–39, 0.731 for ages 40–59, and 0.622 for ages 60+. Sex-group ROC-AUCs were 0.760 and 0.785. Race/ethnicity groups ranged from 0.727 to 0.867, with subgroup sizes from 50 to 418. These estimates are imprecise, do not establish fairness, and show weak discrimination in older adults.

## Limitations

- Cross-sectional current-status label; no prospective-risk claim.
- Internal random split only; no external, temporal, or clinical-site validation.
- Self-report and single-survey measurements can be misclassified.
- Missingness and exclusion rules may limit transportability.
- Age is top-coded at 80; pregnancy is excluded.
- Physical activity is a simplified composite of questionnaire domains.
- Performance, calibration, and threshold behavior may change in any other population.

## Reproducibility and provenance

The binary artifact is Git-ignored. `deployment/model/manifest.json` records its SHA-256, analytical-data SHA-256, feature order, threshold, and metrics pointer. Rebuild with `scripts/train_phase4.py`. The API verifies the binary checksum before loading it.

