"""Assemble a clean, self-contained Hugging Face Docker Space directory."""

import shutil
from pathlib import Path

ROOT = Path(__file__).parents[1]
TARGET = ROOT / "dist" / "huggingface-space"


def main() -> None:
    if TARGET.exists():
        shutil.rmtree(TARGET)
    TARGET.mkdir(parents=True)
    shutil.copy2(ROOT / "deployment" / "huggingface" / "README.md", TARGET / "README.md")
    shutil.copy2(ROOT / "deployment" / "huggingface" / "Dockerfile", TARGET / "Dockerfile")
    shutil.copy2(ROOT / "README.md", TARGET / "README-project.md")
    shutil.copy2(ROOT / "pyproject.toml", TARGET / "pyproject.toml")
    shutil.copytree(ROOT / "src", TARGET / "src")
    shutil.copytree(ROOT / "web", TARGET / "web")
    for source in ("__init__.py", "api", "model"):
        path = ROOT / "deployment" / source
        destination = TARGET / "deployment" / source
        if path.is_dir():
            shutil.copytree(path, destination, ignore=shutil.ignore_patterns("__pycache__"))
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
    print(f"Built {TARGET}")


if __name__ == "__main__":
    main()
