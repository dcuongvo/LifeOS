from lifeos.domains.learning.repository import (
    LearningMemoryRepository,
)
from lifeos.domains.learning.service import LearningService
from lifeos.domains.learning.tools import LearningTools
from lifeos.domains.learning.workflow import (
    LearningWorkflow,
)
from lifeos.platform.embeddings.ollama import (
    OllamaEmbeddingService,
)
from lifeos.platform.settings import get_settings
from lifeos.platform.vectorstore.qdrant_learning_repository import (
    QdrantLearningMemoryRepository,
)


def build_learning_repository() -> LearningMemoryRepository:
    settings = get_settings()

    embedding_service = OllamaEmbeddingService(
        model_name=settings.embedding_model,
        host=settings.ollama_host,
    )

    return QdrantLearningMemoryRepository(
        qdrant_path=settings.qdrant_path,
        embedding_service=embedding_service,
        collection_name=settings.learning_collection,
        vector_size=settings.embedding_vector_size,
    )


def build_learning_service() -> LearningService:
    repository = build_learning_repository()

    return LearningService(
        repository=repository,
    )


def build_learning_tools(
    service: LearningService,
) -> LearningTools:
    return LearningTools(
        service=service,
    )


def build_learning_workflow(
    service: LearningService,
) -> LearningWorkflow:
    settings = get_settings()

    tools = build_learning_tools(
        service=service,
    )

    tool_registry = {
        "search_learning_memory":
            tools.search_learning_memory,
        "save_learning_memory":
            tools.save_learning_memory,
    }

    return LearningWorkflow(
        model_name=settings.chat_model,
        ollama_host=settings.ollama_host,
        tool_registry=tool_registry,
    )