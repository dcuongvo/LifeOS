from typing import Any, Callable, TypedDict

from langgraph.graph import END, StateGraph
from ollama import AsyncClient
from lifeos.platform.time.clock import Clock

SYSTEM_PROMPT = """
You are the LifeOS Planning Agent.

You help the user understand and manage their schedule.

Rules:
- Use available tools when the user's request requires calendar data.
- Never invent calendar events, dates, times, or missing event details.
- Treat calendar tool results as the source of truth for the user's schedule.
- If calendar information is needed, retrieve it before answering.
- Clearly distinguish existing calendar events from suggestions.

Tool usage:
- Use get_events_between when you need all calendar events within a time range.
- Use search_events only when searching for events that match specific text,
  such as a person, title, or keyword.
- Use check_availability when checking whether a specific time range is free or busy.

Calendar changes:
- Before creating an event, make sure the user's intent is clear and the
  required event details are known.
- Before updating or deleting an event, identify the exact event first.
- If no matching event is found, tell the user.
- If multiple matching events are found and the intended event is ambiguous,
  ask the user to clarify.
- Never choose among ambiguous events arbitrarily.
- Before creating or moving an event, use get_events_between to check
  the destination time for overlapping events.
- If another event overlaps the requested time, tell the user which event
  conflicts and ask for confirmation before making the change.
- When moving an existing event, do not treat that same event as a conflict.
""".strip()


class PlanningState(TypedDict):
    messages: list[Any]
    final_answer: str


class PlanningWorkflow:
    def __init__(
        self,
        model_name: str,
        ollama_host: str,
        clock: Clock,
        tool_registry: dict[str, Callable],
    ) -> None:
        self.model_name = model_name
        self.client = AsyncClient(
            host=ollama_host,
        )
        self.clock = clock
        self.tool_registry = tool_registry

        graph = StateGraph(PlanningState)

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

    async def call_model(
        self,
        state: PlanningState,
    ) -> dict:
        print(
            "▶ Planning Agent thinking...",
            flush=True,
        )
    
        current_time = self.clock.iso_now()
        messages = [
            {
                "role": "system",
                "content": (
                    f"{SYSTEM_PROMPT}\n\n"
                    f"Current date and time: {current_time}\n"
                    f"Timezone: {self.clock.timezone}"
                ),
            },
            *state["messages"],
        ]

        response = await self.client.chat(
            model=self.model_name,
            messages=messages,
            tools=list(
                self.tool_registry.values()
            ),
        )

        return {
            "messages": [
                *state["messages"],
                response.message,
            ],
            "final_answer":
                response.message.content or "",
        }

    def should_continue(
        self,
        state: PlanningState,
    ) -> str:
        last_message = state["messages"][-1]

        if last_message.tool_calls:
            return "tools"

        return "end"

    async def call_tools(
        self,
        state: PlanningState,
    ) -> dict:
        last_message = state["messages"][-1]
        new_messages = list(
            state["messages"]
        )

        for tool_call in (
            last_message.tool_calls or []
        ):
            function_name = (
                tool_call.function.name
            )
            arguments = (
                tool_call.function.arguments
            )

            print(
                f"▶ Tool requested: {function_name}",
                flush=True,
            )
            print(
                f"  Arguments: {arguments}",
                flush=True,
            )

            tool_function = (
                self.tool_registry.get(
                    function_name
                )
            )

            if tool_function is None:
                tool_result = (
                    f"Unknown tool: {function_name}"
                )

            else:
                try:
                    tool_result = (
                        await tool_function(
                            **arguments
                        )
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
                    "tool_name":
                        function_name,
                    "content": str(
                        tool_result
                    ),
                }
            )

        return {
            "messages": new_messages,
        }