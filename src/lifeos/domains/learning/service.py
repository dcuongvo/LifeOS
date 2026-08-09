from lifeos.domains.learning.models import LearningMemory
from lifeos.domains.learning.repository import LearningMemoryRepository


class LearningService:
    def __init__(
        self,
        repository: LearningMemoryRepository,
    ) -> None:
        self.repository = repository

    def save_memory(
        self,
        memory: LearningMemory,
    ) -> LearningMemory:
        self.repository.add(memory)
        return memory

    def search_memories(
        self,
        query: str,
        limit: int = 5,
    ) -> list[LearningMemory]:
        return self.repository.search(
            query=query,
            limit=limit,
        )