import argparse
from pathlib import Path
from typing import Optional

from scripts.meta.docker_dev_env.file_templates import FILE_CONTENT_MAPPINGS, CLIENT_FOLDER_STRUCTURE


def create_file(filepath: str) -> Optional[Path]:
    """Will create the file in the project. It accepts files inside folders."""
    print(f"Creating {filepath}...")
    file = Path(filepath)
    if file.exists():
        print("File already exists. Skipping...")
        return

    if "/" in str(file):
        file.parent.mkdir(exist_ok=True, parents=True)
    file.touch()
    return file


def create_docker_dev_env():
    args = parser.parse_args()
    params = {
        "package_src": args.package_src
    }
    for filepath, content in FILE_CONTENT_MAPPINGS:
        file = create_file(filepath=filepath)
        if not file:
            # File already existed
            continue
        file.write_text(content.lstrip().format(**params))

    if args.client_structure:
        for file in CLIENT_FOLDER_STRUCTURE:
            create_file(filepath=file.format(package_src=args.package_src.replace("-", "_")))


parser = argparse.ArgumentParser(
    prog=__file__.split("/")[-1],
    description="A simple CLI tool to create docker dev environments",
)
parser.add_argument("--package-src", required=True)
parser.add_argument("--client-structure", action="store_true", help="If defined, will add the whole proposed folder structure")


if __name__ == "__main__":
    create_docker_dev_env()
