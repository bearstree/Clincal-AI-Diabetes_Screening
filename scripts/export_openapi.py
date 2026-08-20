"""Export the versioned OpenAPI contract."""

import json
from pathlib import Path

from deployment.api.app import app


def main() -> None:
    Path("deployment/api/openapi.json").write_text(
        json.dumps(app.openapi(), indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
