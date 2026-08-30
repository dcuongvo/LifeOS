from typing import Any, Callable, TypedDict

from langgraph.graph import END, StateGraph
from ollama import Client


SYSTEM_PROMPT = """
You are the LifeOS Learning Agent.

You help the user track, retrieve, and reason about their learning.

Memory rules:
- Treat stored learning memories as the source of truth about
  the user's learning history.
- Never claim the user learned, completed, built, or mastered
  something unless the user said so or stored memory supports it.
- When saving learning memory, only save information explicitly
  provided by the user.
- Do not use your general knowledge to expand what the user
  claims to have learned.
- If the user asks to save a topic without explaining what they
  learned, ask for clarification instead of inventing content.

You may use general knowledge to answer educational questions,
but clearly distinguish it from the user's recorded learning history.
""".strip()


class ToolLearningState(TypedDict):
    messages: list[Any]
    final_answer: str


class LearningWorkflow:
    def __init__(
        self,
        model_name: str,
        ollama_host: str,
        tool_registry: dict[str, Callable],
    ) -> None:
        self.model_name = model_name
        self.client = Client(host=ollama_host)
        self.tool_registry = tool_registry

        graph = StateGraph(ToolLearningState)

        graph.add_node(
            "agent",
            self.call_model,
        )

        graph.add_node(
            "tools",
            self.call_tools,
        )

        graph.set_entry_point("agent")

        graph.add_conditional_edges(
            "agent",
            self.should_continue,
            {
                "tools": "tools",
                "end": END,
            },
        )

        graph.add_edge(
            "tools",
            "agent",
        )

        self.graph = graph.compile()

    def call_model(
        self,
        state: ToolLearningState,
    ) -> dict:
        """
        Ask the LLM what to do next.

        The model may:
        - request one or more tools
        - return a final answer
        """

        print("▶ Agent thinking...", flush=True)

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            *state["messages"],
        ]

        response = self.client.chat(
            model=self.model_name,
            messages=messages,
            tools=list(self.tool_registry.values()),
        )

        return {
            "messages": [
                *state["messages"],
                response.message,
            ],
            "final_answer": response.message.content or "",
        }

    def should_continue(
        self,
        state: ToolLearningState,
    ) -> str:
        """
        Decide whether the graph should execute tools
        or stop with the model's final answer.
        """

        last_message = state["messages"][-1]

        if last_message.tool_calls:
            return "tools"

        return "end"

    def call_tools(
        self,
        state: ToolLearningState,
    ) -> dict:
        """
        Execute every tool requested by the LLM and
        append the tool results to the conversation.
        """

        last_message = state["messages"][-1]

        new_messages = list(state["messages"])

        for tool_call in last_message.tool_calls or []:
            function_name = tool_call.function.name
            arguments = tool_call.function.arguments

            print(
                f"▶ Tool requested: {function_name}",
                flush=True,
            )
            print(
                f"  Arguments: {arguments}",
                flush=True,
            )

            tool_function = self.tool_registry.get(
                function_name
            )

            if tool_function is None:
                tool_result = (
                    f"Unknown tool: {function_name}"
                )

            else:
                try:
                    tool_result = tool_function(
                        **arguments
                    )

                except Exception as exc:
                    tool_result = (
                        f"Tool '{function_name}' "
                        f"failed: {exc}"
                    )

            print(
                f"✓ Tool completed: {function_name}",
                flush=True,
            )

            new_messages.append(
                {
                    "role": "tool",
                    "tool_name": function_name,
                    "content": str(tool_result),
                }
            )

        return {
            "messages": new_messages,
        }