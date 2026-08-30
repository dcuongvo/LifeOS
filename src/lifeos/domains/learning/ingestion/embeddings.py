from ollama import Client


class OllamaEmbeddingService:
    def __init__(
        self,
        model_name: str,
        host: str = "http://localhost:11434",
    ) -> None:
        self.model_name = model_name
        self.client = Client(host=host)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        response = self.client.embed(
            model=self.model_name,
            input=texts,
        )

        return [list(vector) for vector in response.embeddings]