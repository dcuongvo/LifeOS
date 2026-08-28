from qdrant_client import QdrantClient, models

from lifeos.domains.learning.models import LearningMemory
from lifeos.domains.learning.repository import LearningMemoryRepository
from lifeos.platform.embeddings.ollama import OllamaEmbeddingService


class QdrantLearningMemoryRepository(LearningMemoryRepository):
    def __init__(
        self,
        qdrant_path: str,
        embedding_service: OllamaEmbeddingService,
        collection_name: str = "learning_memories",
        vector_size: int = 2560,
    ) -> None:
        self.collection_name = collection_name
        self.qdrant_client = QdrantClient(path=qdrant_path)
        self.embedding_service = embedding_service
        self.vector_size = vector_size

        self._ensure_collection()

    def _ensure_collection(self) -> None:
        if self.qdrant_client.collection_exists(self.collection_name):
            return

        self.qdrant_client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=self.vector_size,
                distance=models.Distance.COSINE,
            ),
        )

    def add(self, memory: LearningMemory) -> None:
        embeddings = self.embedding_service.embed_texts([memory.content])
        embedding = embeddings[0]

        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=str(memory.id),
                    vector=embedding,
                    payload=memory.model_dump(mode="json"),
                )
            ],
        )

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[LearningMemory]:
        query_embedding = self.embedding_service.embed_texts([query])[0]

        results = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit,
        ).points

        return [
            LearningMemory.model_validate(result.payload)
            for result in results
        ]

    def close(self) -> None:
        self.qdrant_client.close()