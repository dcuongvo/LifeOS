from lifeos.domains.learning.models import (
    LearningMemory,
    LearningMemoryType,
)
from lifeos.domains.learning.service import LearningService


class LearningTools:
    def __init__(
        self,
        service: LearningService,
    ) -> None:
        self.service = service

    def search_learning_memory(
        self,
        query: str,
        limit: int = 5,
    ) -> str:
        """
        Search the user's learning memories for relevant information.
        """

        results = self.service.search_memories(
            query=query,
            limit=limit,
        )

        if not results:
            return "No relevant learning memories found."

        return "\n\n".join(
            (
                f"Title: {memory.title}\n"
                f"Content: {memory.content}"
            )
            for memory in results
        )

    def save_learning_memory(
        self,
        title: str,
        content: str,
        topics: list[str],
        project: str = "general",
        confidence: float = 0.8,
    ) -> str:
        """
        Save learning information explicitly provided by the user.

        Rules:
        - Only save facts, concepts, projects, or learning progress
        explicitly stated by the user.
        - Never invent or expand what the user learned using your
        own general knowledge.
        - Never invent projects, completion status, or experiences.
        - Preserve the meaning of what the user actually said.
        - If the user asks to save a topic but does not provide
        what they learned about it, do not call this tool.
        Ask the user for more information instead.
        """

        memory = LearningMemory(
            memory_type=LearningMemoryType.CONCEPT,
            title=title,
            content=content,
            topics=topics,
            project=project,
            source="agent",
            confidence=confidence,
        )

        saved_memory = self.service.save_memory(
            memory
        )

        return (
            "Learning memory saved successfully.\n"
            f"Title: {saved_memory.title}\n"
            f"Content: {saved_memory.content}"
        )