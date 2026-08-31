import asyncio

from lifeos.domains.planning.dependencies import (
    build_planning_workflow,
)


async def main() -> None:
    workflow = build_planning_workflow()

    messages = []

    print("\nLifeOS Planning Agent")
    print("Type 'exit' or 'quit' to stop.\n")

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
            result = await workflow.graph.ainvoke(
                {
                    "messages": messages,
                    "final_answer": "",
                }
            )

            messages = result["messages"]

            print("\nAgent:")
            print(result["final_answer"])
            print()

        except Exception as exc:
            print(f"\nError: {exc}\n")


if __name__ == "__main__":
    asyncio.run(main())