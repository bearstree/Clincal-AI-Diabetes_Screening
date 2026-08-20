# Analytical Data Dictionary

The local `data/processed/modeling_cohort.csv` contains one row per `SEQN`. It is reproducible but ignored by Git because it contains participant-level public-use records.

| Analytical field | Source/derivation | Role | Missing handling planned for Phase 4 |
|---|---|---|---|
| `SEQN` | NHANES participant sequence number | Join/audit only; never a predictor or public output | Must be unique |
| `outcome` | 1 when `DIQ010=1` or `LBXGH≥6.5`; 0 only when `DIQ010∈{2,3}` and `LBXGH<6.5` | Current-status research label | Ambiguous outcomes excluded |
| `age_years` | `RIDAGEYR`; age 80+ is top-coded at 80 | Candidate/app predictor | Required in app |
| `sex_female` | `RIAGENDR`: male→0, female→1 | Candidate; not selected for app; subgroup audit | Training-only imputation if needed |
| `height_cm` | `BMXHT` | Supporting app input used to derive BMI; not direct model candidate | Required if app derives BMI |
| `weight_kg` | `BMXWT` | Supporting app input used to derive BMI; not direct model candidate | Required if app derives BMI |
| `bmi` | `BMXBMI`; CDC calculation from height and weight | Selected app/model predictor | Training-fold median inside pipeline |
| `waist_cm` | `BMXWAIST` | Selected app/model predictor | Training-fold median inside pipeline |
| `systolic_bp` | Mean of available `BPXOSY1–3` | Selected app/model predictor | Training-fold median inside pipeline |
| `diastolic_bp` | Mean of available `BPXODI1–3` | Selected app/model predictor | Training-fold median inside pipeline |
| `current_smoker` | `SMQ020` plus `SMQ040` skip-pattern recode | Candidate; not selected in top six | Training-fold imputation |
| `physically_active` | 1 if any PAQ work/transport/leisure domain is yes; 0 when domains are observed and all no | Selected app/model predictor | Required in app |
| `RIDRETH3` | CDC race/Hispanic-origin category | Subgroup evaluation only; not predictor | Preserve unknown separately |
| `WTMECPRP` | Combined-cycle MEC examination weight | Population estimands/sample weight | Must be positive |
| `SDMVPSU`, `SDMVSTRA` | Masked PSU and stratum | Survey variance estimation | Must be preserved |
| `split` | Deterministic stratified assignment, seed 20260819 | `train`, `validation`, or locked `test` | Must never be imputed |

Questionnaire codes 7/9 (refused/don't know) and structural skip-pattern missingness are never treated as ordinary numeric values. Outcome-defining fields and treatment variables are absent from the candidate feature set.

