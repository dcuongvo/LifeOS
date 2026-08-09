from ollama import Client


OLLAMA_HOST = "http://172.27.80.1:11434"
CHAT_MODEL = "qwen3:8b"

client = Client(host=OLLAMA_HOST)

response = client.chat(
    model=CHAT_MODEL,
    messages=[
        {
            "role": "system",
            "content": (
                "You are the LifeOS Learning Agent. "
                "Give clear, concise, practical answers."
            ),
        },
        {
            "role": "user",
            "content": "Explain the difference between PWM and an H-bridge.",
        },
    ],
)

print(response["message"]["content"])