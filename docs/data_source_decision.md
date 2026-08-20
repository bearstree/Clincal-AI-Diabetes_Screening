# Data Source Decision: NHANES 2017–March 2020 Pre-Pandemic

## Decision

Use the CDC/NCHS NHANES 2017–March 2020 pre-pandemic public-use combined sample. It provides a documented national survey sample with interviews, examinations, laboratory measures, public-use weights, masked strata, and masked primary sampling units.

The incomplete 2019–2020 cycle must not be analyzed independently as nationally representative. CDC combined it with 2017–2018 and instructs users to use the combined-sample weights.

## Frozen components

| File | Role |
|---|---|
| `P_DEMO.xpt` | age, sex, race/ethnicity, pregnancy status, weights, strata, PSU |
| `P_DIQ.xpt` | doctor-diagnosed diabetes component of outcome; prohibited as model input |
| `P_GHB.xpt` | HbA1c component of outcome; prohibited as model input |
| `P_BMX.xpt` | BMI and waist candidate predictors |
| `P_BPXO.xpt` | oscillometric blood-pressure candidate predictors |
| `P_PAQ.xpt` | physical-activity candidate predictors |
| `P_SMQ.xpt` | smoking candidate predictors |

Source base URL: `https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/`

Accessed: 2026-08-19. Exact SHA-256 values are in `data/raw/nhanes_2017_2020/manifest.sha256`.

## Terms and handling

The selected files are public-use, de-identified survey files. They remain governed by CDC/NCHS source terms and documentation and are not relicensed under the repository's MIT License. Raw or derived participant-level files are excluded from Git and the public application. The project will cite NHANES and state that CDC/NCHS does not endorse it.

## Known limitations

Cross-sectional measurement does not establish causality or future risk. Self-report can be misclassified. HbA1c availability and missingness can select the analytical cohort. Survey design affects population inference. The non-institutionalized U.S. population and pre-pandemic collection period limit transportability.

