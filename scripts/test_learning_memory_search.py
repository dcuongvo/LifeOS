from lifeos.domains.learning.dependencies import build_learning_service


def main() -> None:
    service = build_learning_service()

    try:
        print("▶ Searching learning memories...\n", flush=True)

        results = service.search_memories(
            query="Arduino inputs",
            limit=10,
        )

        print(f"Found {len(results)} memories.\n")

        for index, memory in enumerate(results, start=1):
            print(f"=== RESULT {index} ===")
            print(f"Title: {memory.title}")
            print(f"Type: {memory.memory_type}")
            print(f"Project: {memory.project}")
            print(f"Topics: {memory.topics}")
            print(f"Source: {memory.source}")
            print(f"Confidence: {memory.confidence}")
            print("Content:")
            print(memory.content)
            print()

    finally:
        service.close()


if __name__ == "__main__":
    main()