import asyncio

from lifeos.platform.mcp.client import LifeOSMCPClient


async def main() -> None:
    client = LifeOSMCPClient()

    result = await client.call_calendar_tool(
        "get_upcoming_events",
        {
            "limit": 5,
        },
    )

    print("\n=== MCP RESULT ===\n")

    for item in result.content:
        print(item)


if __name__ == "__main__":
    asyncio.run(main())