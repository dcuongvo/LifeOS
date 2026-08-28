from lifeos.domains.learning.dependencies import (
    build_learning_service,
    build_learning_workflow,
)


def main() -> None:
    service = build_learning_service()
    workflow = build_learning_workflow(service)

    try:
        print("▶ Running Learning Agent...", flush=True)

        result = workflow.graph.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            "What have I learned about Arduino inputs, "
                            "and what should I study next?"
                        ),
                    }
                ],
                "final_answer": "",
            }
        )

        print("✓ Learning Agent complete", flush=True)

        print("\n=== FINAL ANSWER ===\n")
        print(result["final_answer"])

    finally:
        service.close()


if __name__ == "__main__":
    main()