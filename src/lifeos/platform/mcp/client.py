from pathlib import Path
from typing import Any

from mcp import Client, StdioServerParameters


PROJECT_ROOT = Path(__file__).resolve().parents[4]

CALENDAR_SERVER_PATH = (
    PROJECT_ROOT
    / "src"
    / "lifeos"
    / "platform"
    / "mcp"
    / "google_calendar_server.py"
)


class LifeOSMCPClient:
    def __init__(self) -> None:
        self.calendar_server = StdioServerParameters(
            command="uv",
            args=[
                "run",
                "python",
                str(CALENDAR_SERVER_PATH),
            ],
            cwd=str(PROJECT_ROOT),
        )

    async def call_calendar_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
    ):
        """
        Call a tool exposed by the LifeOS Google Calendar
        MCP server.
        """

        async with Client(self.calendar_server) as client:
            return await client.call_tool(
                tool_name,
                arguments or {},
            )