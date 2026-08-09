from lifeos.domains.learning.models import (
    LearningMemory,
    LearningMemoryType,
)
from lifeos.domains.learning.service import LearningService
from lifeos.platform.vectorstore.qdrant_learning_repository import (
    QdrantLearningMemoryRepository,
)


repository = QdrantLearningMemoryRepository(
    qdrant_path="data/qdrant",
    ollama_host="http://172.27.80.1:11434",
    embedding_model="qwen3-embedding:4b",
)

service = LearningService(repository=repository)

memory = LearningMemory(
    memory_type=LearningMemoryType.SKILL,
    title="Arduino PWM practice",
    content=(
        "I practiced using analogWrite to control LED brightness "
        "and motor speed with PWM."
    ),
    topics=["arduino", "pwm", "motor-control"],
    project="robotics-kit",
    source="manual",
    confidence=0.75,
)

saved_memory = service.save_memory(memory)

results = service.search_memories(
    query="What have I practiced with PWM?",
    limit=3,
)

print(f"\nSaved through service: {saved_memory.title}\n")

for result in results:
    print(f"Type: {result.memory_type}")
    print(f"Title: {result.title}")
    print(f"Content: {result.content}")
    print(f"Topics: {result.topics}")
    print()