import asyncio

from lifeos.domains.planning.agent.tools import PlanningTools
from lifeos.platform.mcp.client import LifeOSMCPClient


async def main() -> None:
    mcp_client = LifeOSMCPClient()

    tools = PlanningTools(
        mcp_client=mcp_client,
    )

    result = await tools.get_upcoming_events(
        limit=5,
    )

    print("\n=== PLANNING TOOL RESULT ===\n")

    for item in result.content:
        print(item)


if __name__ == "__main__":
    asyncio.run(main())