"""Customize the docs build process"""

from pathlib import Path

from mkdocs.config import Config
from mkdocs.structure.files import File, Files

PLUGIN_DIR = Path(__file__).parent
DOCS_DIR = PLUGIN_DIR.parent
PROJECT_ROOT = DOCS_DIR.parent


def on_files(files: Files, config: Config):
    """Implement this hook to get the CHANGELOG.md and the README.md from the project root."""
    dest_dir_base_path = Path(config.site_dir)
    for file_path in ["./README.md", "./CHANGELOG.md"]:
        file = File(
            path=file_path,
            src_dir=str(PROJECT_ROOT),
            dest_dir=str(dest_dir_base_path),
            use_directory_urls=True,
        )
        files.append(file)
