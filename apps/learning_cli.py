from lifeos.domains.learning.dependencies import (
    build_learning_service,
    build_learning_workflow,
)


def main() -> None:
    service = build_learning_service()
    workflow = build_learning_workflow(service)

    messages = []

    print("\nLifeOS Learning Agent")
    print("Type 'exit' or 'quit' to stop.\n")

    try:
        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            messages.append(
                {
                    "role": "user",
                    "content": user_input,
                }
            )

            try:
                result = workflow.graph.invoke(
                    {
                        "messages": messages,
                        "final_answer": "",
                    }
                )

                # Preserve the entire conversation
                messages = result["messages"]

                print("\nAgent:")
                print(result["final_answer"])
                print()

            except Exception as exc:
                print(f"\nError: {exc}\n")

    finally:
        service.close()


if __name__ == "__main__":
    main()