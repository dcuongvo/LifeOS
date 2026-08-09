from abc import ABC, abstractmethod

from lifeos.domains.learning.models import LearningMemory


class LearningMemoryRepository(ABC):
    @abstractmethod
    def add(self, memory: LearningMemory) -> None:
        pass

    @abstractmethod
    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[LearningMemory]:
        pass