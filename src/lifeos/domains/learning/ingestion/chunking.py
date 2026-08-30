import re


def chunk_markdown_by_heading(text: str) -> list[str]:
    sections = re.split(r"(?=^#{2,3}\s)", text, flags=re.MULTILINE)

    chunks = []

    for section in sections:
        cleaned = section.strip()

        if cleaned:
            chunks.append(cleaned)

    return chunks