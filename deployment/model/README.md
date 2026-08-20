# Promoted model bundle

The local promoted artifact is `clinical_diabetes_screening_v1.joblib`. It contains the fitted imputer, scaler, regularized logistic regression, ordered feature list, validation-selected threshold, version, outcome wording, and safety notice.

The 1.4 KB binary contains fitted coefficients and preprocessing state, not participant rows. It is tracked as a release artifact and can be rebuilt with:

```powershell
.\.venv\Scripts\python.exe scripts\train_phase4.py
```

`manifest.json` records the model/data hashes, feature order, threshold, and metrics pointer. The API verifies the artifact SHA-256 before deserialization. Joblib files must only be loaded from trusted build output.
