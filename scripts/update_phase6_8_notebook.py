# ruff: noqa: E501
"""Append the completed Phase 6–8 implementation record to the cumulative notebook."""

from pathlib import Path

import nbformat

ROOT = Path(__file__).parents[1]
PATH = ROOT / "step_by_step.ipynb"
MARKER = "## 29. Phase 6 — Web application"


def markdown(text: str) -> nbformat.NotebookNode:
    return nbformat.v4.new_markdown_cell(text.strip())


def code(text: str) -> nbformat.NotebookNode:
    return nbformat.v4.new_code_cell(text.strip())


def main() -> None:
    notebook = nbformat.read(PATH, as_version=4)
    if any(cell.cell_type == "markdown" and MARKER in cell.source for cell in notebook.cells):
        print("Phase 6–8 record already exists")
        return

    notebook.cells.extend(
        [
            markdown(
                """
## 29. Phase 6 — Web application

Implemented a responsive, keyboard-accessible, dependency-free client in `web/`. The four controls exactly match model order and API validation: age (years), waist circumference (cm), physical activity (yes/no), and diastolic blood pressure (mmHg). The page includes persistent research-only language, loading/error states, model/threshold context, mobile layout, and reduced-motion support.

FastAPI mounts the static client after its API routes, so one deployment serves both UI and JSON endpoints. Optional cross-origin access is disabled unless exact origins are provided with `CLINICAL_ALLOWED_ORIGINS`. The client has no cookies, analytics, accounts, or application persistence.
"""
            ),
            code(
                """
# Local web/API launch (PowerShell)
# .\\.venv\\Scripts\\Activate.ps1
# uvicorn deployment.api.app:app --host 127.0.0.1 --port 8000
# Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs
"""
            ),
            markdown(
                """
### Phase 6 acceptance evidence

- `/` serves the research UI; `/v1/predict` remains the versioned API.
- Browser-side numeric constraints and server-side strict validation agree.
- An API regression test verifies static delivery; Node syntax-checks `web/app.js`.
- The result is framed as a statistical research estimate, never a diagnosis.
"""
            ),
            markdown(
                """
## 30. Phase 7 — Native Android application

Implemented a concise Kotlin/Jetpack Compose app in `android/` using the same four inputs and wording. It uses platform `HttpURLConnection` and `org.json`, avoiding a reflection-based networking layer. Only Internet permission is requested; backup is disabled and no health input/result is stored.

Pinned 2026 build foundation: Android Gradle Plugin 9.3.0, Gradle 9.5.0, JDK 17, compile/target SDK 36, Kotlin/Compose compiler 2.3.21, Compose BOM 2026.06.01. SDK 36 is the current generally available Android 16 platform on the clean CI runner. Debug uses the emulator-only host address `http://10.0.2.2:8000` and a debug-only cleartext exception. Release builds require an HTTPS API URL.
"""
            ),
            code(
                """
# Android build commands (PowerShell; requires Android Studio/SDK and Gradle)
# gradle -p android :app:assembleDebug
# gradle -p android :app:assembleRelease `
#   -PclinicalApiBaseUrl=https://OWNER-SPACE.hf.space
"""
            ),
            markdown(
                """
Local Android compilation was not available on this workstation because Gradle, Android SDK tools, and ADB are not installed. `.github/workflows/android.yml` supplies JDK 17, Android SDK 36/build-tools 36.0.0, and Gradle 9.5.0 to compile the debug APK on every Android change. Public CI exposed three environment assumptions in sequence: platform 37 was unavailable; a redundant third-party SDK setup action stalled; and the runner's preinstalled `sdkmanager` directory was not on `PATH`. The final workflow pins SDK 36 and calls the hosted tool by its explicit path.
"""
            ),
            markdown(
                """
## 31. Phase 8 — Deployment and operations

The production shape is a non-root Python 3.14 Docker container serving FastAPI and the same-origin web client. Access logging is disabled to reduce accidental sensitive-body handling; application code stores no request data. Liveness `/health`, readiness `/ready`, contract `/metadata`, OpenAPI `/docs`, and synthetic prediction checks support operations.

`scripts/build_hf_space.py` assembles a clean ignored directory at `dist/huggingface-space/`. It includes only the Space metadata/Dockerfile, source package, API, web client, project metadata, and checksummed model artifact—never raw or processed participant data. `scripts/publish_hf_space.py` creates or updates a Docker Space through `huggingface_hub`.
"""
            ),
            code(
                """
# Local container and Space bundle
# docker build -f deployment/api/Dockerfile -t clinical-ai:1.0.0 .
# docker run --read-only --tmpfs /tmp -p 8000:8000 clinical-ai:1.0.0
# python scripts/build_hf_space.py

# Authenticated Hugging Face publication (never paste token into source/notebook)
# $env:HF_SPACE_ID = "OWNER/clinical-diabetes-screening"
# $env:HF_TOKEN = Read-Host -AsSecureString  # prefer `hf auth login` or CI secret
# python scripts/publish_hf_space.py
"""
            ),
            markdown(
                """
CI/CD now has four workflows:

1. `ci.yml`: lint, format, type check, tests, notebook parsing, model SHA verification, web syntax, Space assembly, and Docker build.
2. `android.yml`: clean Android debug compilation.
3. `release.yml`: tagged model checksum verification, GitHub artifact attestation, and release assets.
4. `deploy-huggingface.yml`: protected-environment Docker Space creation/update from `HF_TOKEN` and `HF_SPACE_ID` secrets.

The operations runbook defines smoke tests, body-free monitoring, incident handling, rollback, credential rotation, and versioned model reassessment.
"""
            ),
            markdown(
                """
## 32. 7. Version control, reproducibility, and artifact lineage

The detailed policy is saved in `docs/version_control_reproducibility_lineage.md`.

- Protected `main`, short reviewed branches, conventional descriptive commits, semantic release tags, and no secrets/participant data in Git.
- Exact direct dependency/interpreter versions, fixed split seed, executable data/training scripts, clean-runner CI, model card, tests, and notebook validation.
- Lineage: **CDC URL → raw file SHA → cohort/code + processed SHA → fixed split → training configuration → metrics/model card → model SHA → API v1 → web/Android contract → Git commit/tag/CI run → GitHub attestation/Hugging Face commit**.
- The 1.4 KB promoted joblib is release-tracked because it contains fitted preprocessing/model state, not participant rows. `manifest.json` records and the API enforces SHA-256 `eeff07066a6898af46daceae6b7708dabdc60de15bd0a0c60566ad1a42f9caf8`.
- A changed cohort, feature contract, dependency, threshold, fitted state, or API schema requires regeneration, revalidation, a version update, and a changelog entry.
"""
            ),
            code(
                """
# First authenticated GitHub publication
# git remote add origin https://github.com/OWNER/clinical-ai-portfolio.git
# git push -u origin main
# git tag -s v1.0.0 -m "Clinical AI portfolio v1.0.0"
# git push origin v1.0.0

# Verify the tagged GitHub provenance after release
# gh attestation verify deployment/model/clinical_diabetes_screening_v1.joblib `
#   -R OWNER/clinical-ai-portfolio
"""
            ),
            markdown(
                """
## 33. 8. Copyright, licensing, attribution, and privacy

The complete decision record is `docs/copyright_licensing_attribution_privacy.md`; user-facing terms are in `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md`, `CITATION.cff`, and `PRIVACY.md`.

- Original repository work: copyright 2026 contributors, MIT licensed, no warranty or clinical-fitness claim.
- NHANES data/docs/marks are not relicensed. Preserve exact CDC/NCHS attribution, current public-use terms, and a clear non-endorsement statement.
- Keep the model artifact paired with its manifest, model card, source attribution, limitations, intended-use restrictions, and safety notice.
- Review transitive dependency licenses before release; package availability is not a license conclusion.
- Never commit or deploy participant rows. Do not attempt re-identification. Accept only four structured values, reject extra fields, use HTTPS, avoid request-body logs/analytics, minimize platform retention, and publish the actual operator contact/policy.
- This remains educational research—not diagnosis, prognosis, treatment advice, an emergency service, regulatory approval, or a medical device claim.
"""
            ),
            markdown(
                """
## 34. How to use the API and applications

Full instructions are in `docs/user_guide.md`.

**API:** start Uvicorn, inspect `/docs`, POST the four fields to `/v1/predict`, and treat the response threshold flag only as model-evaluation context. HTTP 422 indicates contract/range errors; HTTP 503 indicates a model-readiness problem.

**Web:** open `/`, enter values in the units/ranges shown, submit once, and read the probability together with the model version and warning. No application data are saved.

**Android:** run the debug app in an emulator while the local API is active; build release only with the final HTTPS Space URL. A physical phone needs an authorized reachable HTTPS endpoint.
"""
            ),
            code(
                """
# Example API request (PowerShell)
# $body = @{age_years=50; waist_cm=100; physically_active=$true; diastolic_bp=75} | ConvertTo-Json
# Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/v1/predict `
#   -ContentType application/json -Body $body
"""
            ),
            markdown(
                """
## 35. Publication status and final Phase 6–8 gate

Publication completed without writing credentials into source. The audited baseline commit `20aa229` was pushed to the public repository [bearstree/clinical-ai-portfolio](https://github.com/bearstree/clinical-ai-portfolio). The clean Docker Space bundle was uploaded to [weiyi/clinical-diabetes-screening](https://huggingface.co/spaces/weiyi/clinical-diabetes-screening); the source-linked deployment commit is `92787c8ecdb0e63480340686ac88e8ae0e85455c`.

The live HTTPS service returned `status=ok` from `/health`, `status=ready` from `/ready`, and model `1.0.0` probability `0.103587325784365` (below threshold `0.13012152100670846`) for the documented synthetic input. The workstation Docker daemon and Android/Gradle toolchain were unavailable, so clean Docker and Android builds are enforced by GitHub Actions rather than claimed as local results.

Verified locally on 2026-08-19:

- Ruff: all checks passed; 49 Python files formatted.
- mypy: no issues in 5 source files.
- pytest: 11 passed, including the web delivery test.
- Node: `web/app.js` syntax valid.
- Android: clean GitHub Actions debug build passed in run `32324401854`.
- Space: clean bundle assembled, uploaded, and live-smoke-tested successfully.
- Model: tracked artifact SHA-256 matches the manifest.
- Notebook: parsed and validated after this append.
"""
            ),
        ]
    )
    nbformat.validate(notebook)
    nbformat.write(notebook, PATH)
    print(f"Appended {len(notebook.cells)} total cells to {PATH}")


if __name__ == "__main__":
    main()
