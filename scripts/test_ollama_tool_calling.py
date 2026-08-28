from ollama import Client

from lifeos.domains.learning.dependencies import build_learning_service
from lifeos.domains.learning.tools import LearningTools


service = build_learning_service()
tools = LearningTools(service)

client = Client(host="http://172.27.80.1:11434")


def search_learning_memory(
    query: str,
    limit: int = 5,
) -> str:
    """
    Search the user's learning memories for relevant information.
    """

    results = tools.search_learning_memory(
        query=query,
        limit=limit,
    )

    if not results:
        return "No relevant learning memories found."

    return "\n\n".join(
        f"Title: {memory.title}\nContent: {memory.content}"
        for memory in results
    )


def save_learning_memory(
    title: str,
    content: str,
    topics: list[str],
    project: str = "general",
    confidence: float = 0.8,
) -> str:
    """
    Save something the user says they learned into long-term learning memory.
    """

    memory = tools.save_learning_memory(
        title=title,
        content=content,
        topics=topics,
        project=project,
        confidence=confidence,
    )

    return (
        "Learning memory saved successfully.\n"
        f"Title: {memory.title}\n"
        f"Content: {memory.content}"
    )


tool_registry = {
    "search_learning_memory": search_learning_memory,
    "save_learning_memory": save_learning_memory,
}


messages = [
    {
        "role": "user",
        "content": (
            "I learned that cosine similarity compares the angle between "
            "embedding vectors and is commonly used to measure semantic similarity. "
            "Save this, then tell me what I should study next related to RAG."
        ),
    }
]


MAX_STEPS = 10


try:
    for step in range(MAX_STEPS):

        print(f"\n=== AGENT STEP {step + 1} ===")

        response = client.chat(
            model="qwen3:8b",
            messages=messages,
            tools=list(tool_registry.values()),
        )

        messages.append(response.message)

        # If the model does not request any tools,
        # we are done.
        if not response.message.tool_calls:
            print("\n=== FINAL ANSWER ===")
            print(response.message.content)
            break

        # Execute every tool requested in this step
        for tool_call in response.message.tool_calls:

            function_name = tool_call.function.name
            arguments = tool_call.function.arguments

            print(f"\nTool requested: {function_name}")
            print(f"Arguments: {arguments}")

            tool_function = tool_registry.get(function_name)

            if tool_function is None:
                tool_result = f"Unknown tool: {function_name}"
            else:
                try:
                    tool_result = tool_function(**arguments)
                except Exception as exc:
                    tool_result = (
                        f"Tool '{function_name}' failed: {exc}"
                    )

            print("\n=== TOOL RESULT ===")
            print(tool_result)

            messages.append(
                {
                    "role": "tool",
                    "tool_name": function_name,
                    "content": tool_result,
                }
            )

    else:
        print(
            f"\nAgent stopped after reaching the maximum "
            f"of {MAX_STEPS} steps."
        )

finally:
    service.repository.close()