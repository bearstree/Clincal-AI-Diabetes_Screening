# Phase 0 Project Charter

## Intended use

Develop an research model that estimates the probability that an adult aged 20 or older in the NHANES 2017–March 2020 pre-pandemic public-use sample meets a **current diabetes-status research definition**, using non-invasive information available at a screening encounter.

The preliminary outcome definition for feasibility testing is:

- doctor-diagnosed diabetes (`DIQ010 = 1`, excluding pregnancy-only wording), **or**
- glycohemoglobin/HbA1c (`LBXGH`) at or above 6.5%.

This definition is provisional until Phase 2 codebook review and cohort counts are complete. It defines a research label, not a clinical diagnosis.

A negative label requires both a negative/borderline diabetes response (`DIQ010` in 2 or 3) and observed HbA1c below 6.5%. A diagnosed participant or a participant with HbA1c at or above 6.5% is positive. Other combinations are outcome-ambiguous and excluded; a missing HbA1c is never silently treated as normal.

## Intended users and context

- Portfolio reviewers, students, data scientists, and software engineers.
- A synthetic-input public demonstration of responsible ML engineering.
- Population-level research evaluation using the NHANES survey design.

## Explicit non-use

The system must not be used to diagnose, treat, triage, prescribe, replace laboratory testing, predict future diabetes, or guide care for an individual. It is not intended for clinical workflow integration, emergencies, children, pregnant people, or populations outside the supported cohort. No score should be interpreted without the displayed limitations.

## Prediction time and candidate inputs

Prediction time is a hypothetical non-invasive screening encounter before laboratory results are known. Candidate features are age, sex, body-mass index, waist circumference, averaged measured blood pressure, physical-activity responses, and smoking responses. Race/ethnicity is reserved initially for subgroup evaluation, not prediction. `DIQ010`, `LBXGH`, diabetes treatment variables, and downstream consequences are outcome-defining or post-outcome variables and are prohibited as predictors.

## Population and exclusions

- Include adults age 20 or older with an examination record and an observable outcome definition.
- Exclude participants recorded as pregnant at examination from the initial model-development cohort because pregnancy changes diabetes interpretation and the project does not address gestational diabetes.
- Apply all additional exclusions transparently during Phase 2, with a cohort flow table.

## Claims boundary

The output may be called a research probability or screening score for the project's current-status definition. It must not be called a diagnosis, future-risk prediction, personalized medical advice, or proof of benefit.
