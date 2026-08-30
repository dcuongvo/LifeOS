from pathlib import Path


def load_markdown_file(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Learning file not found: {file_path}")

    if path.suffix.lower() != ".md":
        raise ValueError("Only Markdown files are supported for now.")

    return path.read_text(encoding="utf-8")