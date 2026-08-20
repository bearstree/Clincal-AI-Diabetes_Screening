# App Input and Form Specification — Model 1.0.0

Validation ablation reduced the provisional six-feature form to four inputs without meaningful discrimination loss. The final model input contract is `configs/app_features.json`.

```text
┌──────────────────────────────────────────┐
│ Educational diabetes screening demo     │
│ Not a diagnosis or medical advice       │
├──────────────────────────────────────────┤
│ Age [  ] years                           │
│ Waist circumference [    ] cm            │
│ Diastolic blood pressure [   ] mmHg      │
│ Regular ≥10-minute activity? Yes / No    │
├──────────────────────────────────────────┤
│ [ Review inputs ]       [ Estimate ]     │
└──────────────────────────────────────────┘
```

## Interaction rules

- Use numeric mobile keyboards and visible units.
- Include illustrated waist-measurement help and explain that a recent BP reading is required.
- Do not infer or default any value, including activity.
- Validate on blur and submission; never silently clip values.
- Preserve input after recoverable network errors but do not persist it by default.
- Show the educational-use notice before submission and on results.
- Display probability as a research estimate. If the validation-derived flag is shown, call it a screening flag and explain that test sensitivity was lower than the validation target.

The model uses diastolic—not systolic—pressure because the prespecified validation ablation had better probability error and equivalent discrimination. This unusual choice is dataset-specific and reinforces that the system is not a clinical rule.

