# Phase 8 operations runbook

## Release and deploy

1. Run all local quality gates and review the model card, privacy notice, dependency licenses, artifact/data hashes, and changelog.
2. Merge through protected `main`; create a signed semantic tag only from a green commit.
3. The release workflow verifies the model checksum, packages it, creates GitHub provenance, and uploads the release asset.
4. Dispatch the Hugging Face workflow with protected `HF_TOKEN` and `HF_SPACE_ID` secrets. Record the deployed Space commit and smoke-test `/health`, `/ready`, `/metadata`, `/`, and one synthetic `/v1/predict` request.
5. Build Android release with the final HTTPS Space URL; do not distribute a build pointing to a mutable or development endpoint.

## Observe

Monitor uptime, latency, HTTP status counts, container restarts, and dependency/security alerts without logging request bodies. Never monitor individual risk values. `/health` tests the process; `/ready` verifies the checksummed model can load. Set an external HTTPS uptime probe and a synthetic request using non-personal values.

## Incident and rollback

On checksum failure, readiness failure, unexpected schema/output, privacy leak, or unsafe behavior: stop traffic, preserve non-sensitive operational evidence, rotate exposed credentials, post a clear status notice, and roll back to the last known Git tag/Hugging Face commit. Do not “fix forward” while a potentially harmful clinical result remains public. Document impact, timeline, root cause, corrective tests, and whether users or providers must be notified.

## Model lifecycle

This cross-sectional research model must not drift silently. Reassess data relevance, calibration, discrimination, subgroup evidence, intended use, dependency vulnerabilities, and clinical wording at least per release and before any scope expansion. A new dataset, feature contract, threshold, or fitted state gets a new model version and full validation—not an in-place file replacement.
