from math import sqrt

from ollama import Client


MODEL_NAME = "qwen3-embedding:4b"

client = Client(host="http://172.27.80.1:11434")

sentences = [
    "I learned how PWM controls LED brightness with Arduino.",
    "Arduino analogWrite can change the brightness of an LED.",
    "I cooked chicken curry for dinner.",
]


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    magnitude_a = sqrt(sum(a * a for a in vector_a))
    magnitude_b = sqrt(sum(b * b for b in vector_b))

    return dot_product / (magnitude_a * magnitude_b)


response = client.embed(
    model=MODEL_NAME,
    input=sentences,
)

embeddings = response["embeddings"]

print(f"Number of sentences: {len(embeddings)}")
print(f"Vector dimensions: {len(embeddings[0])}")

print(
    "Arduino sentence vs Arduino sentence:",
    cosine_similarity(embeddings[0], embeddings[1]),
)

print(
    "Arduino sentence vs cooking sentence:",
    cosine_similarity(embeddings[0], embeddings[2]),
)