from dataclasses import dataclass

from ollama import Client

from lifeos.domains.learning.models import LearningMemory
from lifeos.domains.learning.repository import LearningMemoryRepository


@dataclass
class LearningAgentResponse:
    answer: str
    sources: list[LearningMemory]


class LearningAgent:
    def __init__(
        self,
        repository: LearningMemoryRepository,
        model_name: str,
        ollama_host: str,
    ) -> None:
        self.repository = repository
        self.model_name = model_name
        self.client = Client(host=ollama_host)

    def answer(
        self,
        question: str,
        retrieval_limit: int = 5,
    ) -> LearningAgentResponse:
        memories = self.repository.search(
            query=question,
            limit=retrieval_limit,
        )

        context = "\n\n".join(
            (
                f"Title: {memory.title}\n"
                f"Type: {memory.memory_type}\n"
                f"Project: {memory.project}\n"
                f"Content:\n{memory.content}"
            )
            for memory in memories
        )

        system_prompt = """
You are the LifeOS Learning Agent, a personalized learning coach.

Your responsibilities are to:
- Track what the user has learned
- Summarize completed projects and concepts
- Identify likely knowledge gaps
- Recommend practical next learning steps
- Connect current learning to longer-term goals

Rules:
- Use the provided learning memories as the source of truth for the user's learning history.
- Never claim the user completed something unless the memories support it.
- Clearly distinguish completed work, practiced concepts, inferred gaps, and suggested next steps.
- Never use words such as "mastered", "expert", or "proficient" unless explicitly supported.
- Completing a project demonstrates exposure or practice, not mastery.
- Do not infer knowledge or experience solely from related topics.
- Only claim relationships between concepts, tools, projects, or skills when the memories support them.
- Clearly distinguish the user's recorded learning history from recommendations based on general knowledge.
- If the memories are incomplete or ambiguous, say so.
""".strip()

        user_prompt = f"""
Learning memories:

{context}

Question:

{question}
""".strip()

        response = self.client.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return LearningAgentResponse(
            answer=response.message.content,
            sources=memories,
        )