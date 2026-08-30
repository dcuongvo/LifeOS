import asyncio

from mcp import Client, StdioServerParameters


async def main() -> None:
    server = StdioServerParameters(
        command="uv",
        args=[
            "run",
            "python",
            "src/lifeos/platform/mcp/google_calendar_server.py",
        ],
    )

    async with Client(server) as client:
        print("▶ Connected to MCP server")

        tools_result = await client.list_tools()

        print("\n=== AVAILABLE TOOLS ===\n")

        for tool in tools_result.tools:
            print(f"- {tool.name}")
            print(f"  {tool.description}")

        print("\n=== CALLING get_upcoming_events ===\n")

        result = await client.call_tool(
            "get_upcoming_events",
            {
                "limit": 5,
            },
        )

        for item in result.content:
            print(item)


if __name__ == "__main__":
    asyncio.run(main())