# 7. Version control, reproducibility, and artifact lineage

## Git workflow

Use `main` as the protected, releasable branch. Create short feature branches, require the CI checks and one review, squash or merge with a descriptive message, and never commit credentials or participant-level raw/derived data. Releases use semantic tags such as `v1.0.0`; model and API versions change deliberately and are recorded in the changelog.

```powershell
git switch -c feature/short-description
git add --all
git diff --cached
git commit -m "feat: describe the change"
git push -u origin feature/short-description
```

For first publication, create an empty public GitHub repository, then:

```powershell
git remote add origin https://github.com/OWNER/clinical-ai-portfolio.git
git push -u origin main
```

Do not put a token in the URL or notebook. Authenticate using Git Credential Manager, SSH, or a connected GitHub account.

## Reproducibility controls

- Python 3.14.2 and exact direct dependency versions are pinned; CI starts from a clean runner.
- Download code and SHA-256 manifests identify every raw NHANES file; raw and processed participant data remain outside Git.
- Fixed split seed `20260819`, cohort rules, prohibited leakage variables, feature order, selected threshold, metrics, and model/data hashes are versioned.
- `scripts/build_phase2_3.py` and `scripts/train_phase4.py` regenerate preprocessing and model outputs; tests, Ruff, mypy, notebooks, JavaScript syntax, model checksum, and Docker build are CI gates.
- The promoted model binary is tracked because it contains only fitted state; `manifest.json` is the authoritative verification record.

## Lineage chain

`CDC URLs → raw SHA-256 manifest → cohort/preprocessing code + data SHA → fixed split → training config/seed → metrics/model card → joblib SHA → API v1 → web/Android request contract → Git tag/CI run → GitHub attestation/Hugging Face commit`.

Each release should record the Git commit SHA and deployed Hugging Face commit in `CHANGELOG.md`. A changed input, dependency, cohort rule, feature, coefficient, threshold, or contract requires regeneration and revalidation; never overwrite an old version silently.

## Verification

```powershell
python scripts/build_phase2_3.py
python scripts/train_phase4.py
python -c "import hashlib,json,pathlib; p=pathlib.Path('deployment/model'); m=json.loads((p/'manifest.json').read_text()); assert hashlib.sha256((p/m['artifact']).read_bytes()).hexdigest()==m['artifact_sha256']"
ruff check .
mypy src
pytest
```

Tagged GitHub releases run an artifact attestation for the model. Verify it with `gh attestation verify deployment/model/clinical_diabetes_screening_v1.joblib -R OWNER/clinical-ai-portfolio`.
