# Changelog

All notable changes follow Keep a Changelog conventions. Versions follow Semantic Versioning.

## [Unreleased]

### Changed

- Renamed the user-facing tool to **Diabetes Screening**, shortened the action to **Estimate probability**, and added a plain-language explanation of the probability in both clients.
- Renamed the GitHub repository and Hugging Face Space to `Clincal-AI-Diabetes_Screening`.
- Replaced the MIT license with the Personal Use License: personal, non-commercial use only; commercial use requires prior written approval.
- Removed the retired wording from the repository, API, model bundle, web client, Android client, and deployment card.
- Rebuilt the model artifact and OpenAPI document; model performance and threshold are unchanged.

### Added

- Phase 0 governance and clinical-question artifacts.
- Phase 1 reproducible repository, CI, tests, licensing, and contribution foundation.
- Reproducible NHANES 2017–March 2020 public-use download script and checksum manifest.
- Phase 2 validated cohort builder and data dictionary.
- Phase 3 EDA, leakage-safe splits, train-only feature ranking, aggregate figures, and app input schema.
- Phase 4 candidate comparison, locked-test evaluation, model card, and checksummed model bundle.
- Phase 5 versioned FastAPI prediction service, OpenAPI contract, container definition, and API tests.
