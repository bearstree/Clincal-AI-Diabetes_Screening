# Diabetes Screening

[Live web application](https://weiyi-clincal-ai-diabetes-screening.hf.space) · [Hugging Face Space](https://huggingface.co/spaces/weiyi/Clincal-AI-Diabetes_Screening) · [API documentation](https://weiyi-clincal-ai-diabetes-screening.hf.space/docs)

An end-to-end, clinical AI portfolio project using public-use CDC NHANES data: reproducible preprocessing, an evaluated screening model, a versioned API, a responsive web client, and a native Android client.

> Research only. This project is not a diagnostic tool, medical advice, a clinically validated system, or a medical device.

## Current status

The release includes governance, verified data lineage, leakage-safe modeling, a checksummed model, FastAPI, web and Android clients, CI/CD, a deployed Docker Space, and release/privacy documentation.

## Intended use

The planned model will estimate the probability that a U.S. adult aged 20 or older meets the project's **current diabetes-status research definition**, using non-invasive information available at screening time. It is meant to demonstrate ML engineering and responsible evaluation—not to diagnose an individual or predict future diabetes.

See [governance](docs/governance/project_charter.md) for the precise scope and exclusions.

## Local setup

Python 3.14.2 is the pinned development interpreter for this foundation.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pre-commit install
pytest
uvicorn deployment.api.app:app --reload
```

Download or verify the public-use source files:

```powershell
.\scripts\download_nhanes.ps1
```

Open <http://127.0.0.1:8000> for the web app or <http://127.0.0.1:8000/docs> for interactive API documentation. Raw and derived participant data are excluded from Git. The small model artifact contains no participant rows and is protected by a tracked checksum.

## Documentation

- `notebooks/01_end_to_end_clinical_ai_workflow.ipynb`: overall roadmap
- `docs/governance/`: Phase 0 decisions, risks, and acceptance gates
- `docs/data_source_decision.md`: dataset provenance and selection
- `docs/data_dictionary.md`: analytical variables and derivations
- `docs/phase2_3_report.md`: cohort, EDA, split, and feature-selection results
- `docs/app_input_spec.md`: provisional web/Android form and interaction design
- `docs/model_card.md`: promoted-model evidence, limitations, and subgroup results
- `docs/phase4_5_report.md`: model-selection and API implementation report
- `deployment/model/`: promoted local model and tracked provenance manifest
- `deployment/api/`: FastAPI entry point, container definition, and OpenAPI contract
- `web/` and `android/`: user clients
- `docs/user_guide.md`: API, web, Android, and deployment instructions
- `docs/version_control_reproducibility_lineage.md`: Git/release and artifact lineage controls
- `docs/copyright_licensing_attribution_privacy.md`: rights, attribution, and privacy decisions
- `docs/operations_runbook.md`: deployment, monitoring, rollback, and incident procedure

## License

Original repository code, documentation, and model output are available for personal, non-commercial use only. Commercial use requires prior written approval from the copyright holder. Dataset files and third-party software remain governed by their own terms. See `LICENSE`, `NOTICE`, and `THIRD_PARTY_NOTICES.md`.
