from lifeos.domains.learning.models import (
    LearningMemory,
    LearningMemoryType,
)
from lifeos.platform.vectorstore.qdrant_learning_repository import (
    QdrantLearningMemoryRepository,
)


repository = QdrantLearningMemoryRepository(
    qdrant_path="data/qdrant",
    ollama_host="http://172.27.80.1:11434",
    embedding_model="qwen3-embedding:4b",
)

memory = LearningMemory(
    memory_type=LearningMemoryType.CONCEPT,
    title="Arduino H-bridge motor control",
    content=(
        "An H-bridge changes motor direction by reversing "
        "the polarity applied to the motor."
    ),
    topics=["arduino", "motor-control", "electronics"],
    project="robotics-kit",
    source="manual",
    confidence=0.8,
)

repository.add(memory)

results = repository.search(
    "What have I learned about controlling motor direction?",
    limit=3,
)

print(f"\nSaved memory ID: {memory.id}\n")

for result in results:
    print(f"Type: {result.memory_type}")
    print(f"Title: {result.title}")
    print(f"Content: {result.content}")
    print(f"Topics: {result.topics}")
    print(f"Project: {result.project}")
    print(f"Confidence: {result.confidence}")
    print()