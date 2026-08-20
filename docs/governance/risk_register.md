# Initial Risk Register

| Risk | Potential harm | Initial control | Release consequence |
|---|---|---|---|
| Cross-sectional data described as future risk | Misleading users | Current-status wording everywhere; automated documentation review | Block release |
| Outcome leakage | Inflated performance | Prohibited-variable list; pipeline/test review | Block model promotion |
| Poor calibration | Misleading probabilities | Calibration evaluation and recalibration on validation data only | Block model promotion |
| Subgroup instability | Unequal or unreliable behavior | Prespecified subgroup metrics, counts, uncertainty; limitations | Block or narrow intended use |
| Survey-design misuse | Invalid population claims | Use combined-cycle weights/strata/PSUs for population estimands | Remove population claim |
| Missing/special codes treated as values | Biased model | Codebook-driven recoding and range tests | Block data release |
| Public demo interpreted as care advice | Unsafe action | Persistent disclaimer, no diagnosis language, professional-care guidance | Block deployment |
| Health inputs logged or retained | Privacy harm | No raw input logging; minimal telemetry; retention documentation | Incident/kill switch |
| Dependency or artifact compromise | Supply-chain harm | Pins, scans, SBOM, protected CI, signed release artifacts | Block deployment |
| Dataset or third-party license violation | Legal/ethical harm | No raw data in Git; NOTICE, provenance, license review | Block release |

