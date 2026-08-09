from ollama import Client
from qdrant_client import QdrantClient, models


OLLAMA_HOST = "http://172.27.80.1:11434"
EMBEDDING_MODEL = "qwen3-embedding:4b"

COLLECTION_NAME = "learning_memories"
VECTOR_SIZE = 2560

ollama_client = Client(host=OLLAMA_HOST)

qdrant_client = QdrantClient(
    path="data/qdrant",
)


learning_memories = [
    {
        "id": 1,
        "text": "I learned how PWM controls LED brightness using analogWrite on Arduino.",
        "topic": "arduino",
        "project": "robotics",
    },
    {
        "id": 2,
        "text": "I learned how an H-bridge motor driver controls motor speed and direction.",
        "topic": "arduino",
        "project": "robotics",
    },
    {
        "id": 3,
        "text": "LifeOS uses a modular monolith organized with domain-driven design.",
        "topic": "architecture",
        "project": "lifeos",
    },
    {
        "id": 4,
        "text": "Embeddings convert text into vectors so semantically similar text can be retrieved.",
        "topic": "rag",
        "project": "lifeos",
    },
]


if not qdrant_client.collection_exists(COLLECTION_NAME):
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=VECTOR_SIZE,
            distance=models.Distance.COSINE,
        ),
    )


texts = [memory["text"] for memory in learning_memories]

embedding_response = ollama_client.embed(
    model=EMBEDDING_MODEL,
    input=texts,
)

embeddings = embedding_response["embeddings"]


points = []

for memory, embedding in zip(learning_memories, embeddings):
    points.append(
        models.PointStruct(
            id=memory["id"],
            vector=embedding,
            payload={
                "text": memory["text"],
                "topic": memory["topic"],
                "project": memory["project"],
            },
        )
    )


qdrant_client.upsert(
    collection_name=COLLECTION_NAME,
    points=points,
)


question = "What have I learned about Arduino motor control?"

question_response = ollama_client.embed(
    model=EMBEDDING_MODEL,
    input=question,
)

question_embedding = question_response["embeddings"][0]


results = qdrant_client.query_points(
    collection_name=COLLECTION_NAME,
    query=question_embedding,
    limit=3,
).points


print(f"\nQuestion: {question}\n")

for result in results:
    print(f"Score: {result.score:.3f}")
    print(f"Text: {result.payload['text']}")
    print(f"Topic: {result.payload['topic']}")
    print(f"Project: {result.payload['project']}")
    print()