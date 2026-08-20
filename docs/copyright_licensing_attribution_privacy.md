# 8. Copyright, licensing, attribution, and privacy

## Rights and licenses

Original source code and documentation are copyright 2026 Clinical AI Portfolio Contributors and are offered under MIT (`LICENSE`). Contributions are accepted under the same license. The license grants broad software reuse but provides no warranty, clinical validity, or fitness for a particular purpose.

NHANES files, labels, documentation, and agency marks are not relicensed. Users must follow current CDC/NCHS public-use terms, analytic guidance, citation practice, and disclosure restrictions. This repository does not redistribute participant data and makes no endorsement claim. See `NOTICE` and `THIRD_PARTY_NOTICES.md`.

The fitted artifact is repository output under the project license to the extent copyright applies; it must remain paired with its model card, checksum manifest, safety notice, and source-data attribution. Third-party packages keep their own licenses. Before each release, generate and review Python and Gradle dependency/license inventories; do not assume MIT compatibility from package availability alone.

## Attribution checklist

1. Preserve `LICENSE`, `NOTICE`, `CITATION.cff`, model card, and source links.
2. Cite the exact NHANES cycle/components and access date in scholarly outputs.
3. Cite the repository release/tag and model version.
4. State that CDC/NCHS neither created nor endorsed this model.
5. Do not use agency logos or imply regulatory approval.

## Privacy and clinical safety

Only four structured inputs are accepted; names, identifiers, dates, location, free text, and accounts are intentionally absent. The web and Android clients store nothing and include no telemetry. The API rejects extra fields and runs without access-body logging in its container. Production must use HTTPS, minimum infrastructure logs, access controls, a short documented retention period, dependency scanning, and a breach/abuse contact.

Public NHANES data are de-identified public-use research files, but derived participant rows are still excluded from Git, releases, containers, logs, screenshots, and issue attachments. Never attempt re-identification or join to external identity data. The output is a research screening estimate—not diagnosis, prognosis, treatment advice, or an emergency service. The older-adult subgroup result and other limitations in the model card must remain visible to evaluators.

See `PRIVACY.md` for the user-facing notice. A real operator must replace the repository-owner contact placeholder after account publication and reassess whether applicable privacy, consumer-protection, medical-device, accessibility, or institutional review requirements apply before expanding scope.
