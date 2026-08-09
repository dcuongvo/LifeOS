from ollama import Client
from qdrant_client import QdrantClient, models

from lifeos.domains.learning.models import LearningMemory
from lifeos.domains.learning.repository import LearningMemoryRepository


class QdrantLearningMemoryRepository(LearningMemoryRepository):
    def __init__(
        self,
        qdrant_path: str,
        ollama_host: str,
        embedding_model: str,
        collection_name: str = "learning_memories",
        vector_size: int = 2560,
    ) -> None:
        self.collection_name = collection_name

        self.ollama_client = Client(host=ollama_host)
        self.qdrant_client = QdrantClient(path=qdrant_path)
        self.embedding_model = embedding_model
        self.vector_size = vector_size

        self._ensure_collection()
    # check if qdrant collection exist or not 
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
    #convert to embedding and upsert to qdrant collection
    def add(self, memory: LearningMemory) -> None:
        response = self.ollama_client.embed(
            model=self.embedding_model,
            input=memory.content,
        )

        embedding = response["embeddings"][0]

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
    # simple semantic search and return the result as LearningMemory list
    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[LearningMemory]:
        response = self.ollama_client.embed(
            model=self.embedding_model,
            input=query,
        )

        query_embedding = response["embeddings"][0]

        results = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit,
        ).points

        return [
            LearningMemory.model_validate(result.payload)
            for result in results
        ]