# Clinical Question and Estimand

## Question

Among U.S. civilian, non-institutionalized adults aged 20 or older represented by the NHANES 2017–March 2020 pre-pandemic sample, how well can a model using non-invasive screening information discriminate and calibrate current diabetes status as defined in the project charter?

## Unit and time zero

- Unit of analysis: one survey participant (`SEQN`).
- Time zero: the modeled screening encounter, before HbA1c or diabetes questionnaire outcome fields are exposed to the model.
- Outcome horizon: current/contemporaneous status; there is no future horizon.

## Primary evaluation targets

- Discrimination: ROC-AUC and PR-AUC with uncertainty.
- Probability quality: calibration plot, calibration intercept/slope, and Brier score.
- Operating characteristics: sensitivity, specificity, PPV, and NPV at a threshold selected from an explicit screening-harm rationale.
- Equity inspection: the same metrics with sample sizes and uncertainty by prespecified age, sex, and race/ethnicity groups.
- Reproducibility: fixed source checksums, code revision, configuration, seeds, and tolerance-based metric reproduction.

Thresholds will not be chosen until prevalence and uncertainty are measured. Model selection must compare against prevalence-only and regularized logistic-regression baselines. Survey-weighted population estimates and unweighted predictive validation answer different questions and will be labeled separately.

