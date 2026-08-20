# API and application user guide

## Start locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
uvicorn deployment.api.app:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` for the web app, `/docs` for Swagger UI, `/health` for liveness, `/ready` for model readiness, and `/metadata` for the deployed contract.

## Call the API

```powershell
$body = @{ age_years=50; waist_cm=100; physically_active=$true; diastolic_bp=75 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/v1/predict -ContentType application/json -Body $body
```

The response contains a probability, whether it is above the validation-selected threshold, that threshold, model version, outcome definition, and safety notice. HTTP 422 means an input is absent, extra, wrongly typed, or outside its displayed range; 503 means the model is not ready. Do not convert the threshold flag into a diagnosis.

## Use the web app

Enter age, waist circumference, diastolic blood pressure, and activity status, then select **Estimate research probability**. The browser sends the values once to the same-origin API and displays the model version and threshold context. It does not save the values. For a separately hosted UI, set the `api-base-url` meta value in `web/index.html` and configure the exact HTTPS origin in `CLINICAL_ALLOWED_ORIGINS`.

## Use the Android app

Start the local API, open `android/` in current Android Studio, create an API 36 emulator, and run the debug app. Android's emulator reaches the host service at `10.0.2.2:8000`. Release builds reject cleartext transport and must be built with the deployed URL:

```powershell
gradle -p android :app:assembleRelease -PclinicalApiBaseUrl=https://OWNER-SPACE.hf.space
```

The app requests only Internet permission and retains no input or result. A physical phone cannot use `10.0.2.2`; use an authorized HTTPS deployment.

## Docker and Hugging Face Space

```powershell
docker build -f deployment/api/Dockerfile -t clinical-ai:1.0.0 .
docker run --read-only --tmpfs /tmp -p 8000:8000 clinical-ai:1.0.0
python scripts/build_hf_space.py
```

Set repository secrets `HF_TOKEN` (write-scoped token) and `HF_SPACE_ID` (`OWNER/SPACE`) in GitHub, then dispatch **Deploy Hugging Face Space**. The workflow creates/updates a public Docker Space. The token is never written into source.
