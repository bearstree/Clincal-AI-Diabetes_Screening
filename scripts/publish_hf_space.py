"""Create or update the configured Hugging Face Docker Space."""

import os
from pathlib import Path

from huggingface_hub import HfApi


def main() -> None:
    space_id = os.environ["HF_SPACE_ID"]
    token = os.getenv("HF_TOKEN") or True
    bundle = Path(__file__).parents[1] / "dist" / "huggingface-space"
    api = HfApi(token=token)
    api.create_repo(space_id, repo_type="space", space_sdk="docker", exist_ok=True)
    result = api.upload_folder(
        repo_id=space_id,
        repo_type="space",
        folder_path=bundle,
        commit_message=os.getenv("HF_COMMIT_MESSAGE", "Deploy verified clinical AI release"),
    )
    print(result.oid)


if __name__ == "__main__":
    main()
