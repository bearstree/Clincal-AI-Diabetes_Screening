# Prespecified Acceptance Gates

## Before modeling

- Intended use, outcome, time zero, population, exclusions, and prohibited features are documented.
- Every selected variable is mapped to an official codebook definition and availability time.
- Raw checksums match the manifest; cohort construction is reproducible and tested.
- Split strategy and survey-weighted versus predictive estimands are documented before fitting.

## Before model promotion

- No known target leakage or participant overlap across partitions.
- Candidate beats the prevalence-only baseline and is compared with regularized logistic regression.
- Calibration, discrimination, operating metrics, uncertainty, and subgroup sample sizes are reported.
- A threshold has an explicit harm/benefit rationale; otherwise only a probability is returned.
- Model card, limitations, and failure analysis are complete.

No numeric performance threshold is invented during Phase 0. Quantitative gates will be set after Phase 2 feasibility analysis, before candidate-model comparison, to avoid selecting targets after seeing final test results.

## Before public deployment

- API contract, malformed/boundary inputs, golden predictions, latency, and failure states pass tests.
- Web and Android clients display the claims boundary and do not store inputs by default.
- Security scans, SBOM, secrets review, staging smoke tests, monitoring, rollback, and kill switch are verified.
- Only synthetic examples are demonstrated; no NHANES participant row is exposed.

