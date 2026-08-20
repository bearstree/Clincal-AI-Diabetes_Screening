# Third-party notices

- Data source: National Health and Nutrition Examination Survey (NHANES), 2017–March 2020 pre-pandemic public-use files, CDC/NCHS. CDC/NCHS does not endorse this project. Source files are not covered by this repository's Personal Use License.
- Python and Android dependencies retain their own copyright and license terms. Exact direct versions are pinned in `pyproject.toml` and `android/app/build.gradle.kts`; transitive licenses must be reviewed from the generated dependency reports before a public release.
- Product and organization names are used only for identification. Android, GitHub, Hugging Face, CDC, NCHS, and NHANES trademarks belong to their owners.

Release commands for dependency evidence:

```powershell
python -m pip freeze
gradle -p android :app:dependencies
```
