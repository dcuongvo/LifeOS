from pathlib import Path

from lifeos.domains.learning.chunking import chunk_markdown_by_heading
from lifeos.domains.learning.ingestion import load_markdown_file
from lifeos.domains.learning.models import (
    LearningMemory,
    LearningMemoryType,
)
from lifeos.domains.learning.repository import LearningMemoryRepository


def index_learning_markdown(
    file_path: str,
    repository: LearningMemoryRepository,
    project: str,
) -> list[LearningMemory]:
    text = load_markdown_file(file_path)
    chunks = chunk_markdown_by_heading(text)

    source_name = Path(file_path).name
    memories: list[LearningMemory] = []

    for chunk in chunks:
        lines = chunk.splitlines()
        title = lines[0].removeprefix("### ").removeprefix("## ").removeprefix("# ").strip()

        memory = LearningMemory(
            memory_type=LearningMemoryType.CONCEPT,
            title=title,
            content=chunk,
            topics=[],
            project=project,
            source=source_name,
            confidence=1.0,
        )

        repository.add(memory)
        memories.append(memory)

    return memories