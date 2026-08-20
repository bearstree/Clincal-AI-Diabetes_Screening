# NHANES raw snapshot

This local directory contains seven immutable public-use XPT files downloaded from CDC/NCHS on 2026-08-19. XPT files are intentionally ignored by Git. Run `scripts/download_nhanes.ps1` to retrieve and verify them against `manifest.sha256`.

Do not edit files in place. Derived data belong in `data/interim` or `data/processed`, which are also excluded from Git.

