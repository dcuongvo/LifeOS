from lifeos.domains.planning.agent.tools import PlanningTools
from lifeos.domains.planning.agent.workflow import PlanningWorkflow
from lifeos.platform.mcp.client import LifeOSMCPClient
from lifeos.platform.settings import get_settings
from lifeos.platform.time.clock import Clock

def build_planning_mcp_client() -> LifeOSMCPClient:
    return LifeOSMCPClient()


def build_planning_tools(
    mcp_client: LifeOSMCPClient,
) -> PlanningTools:
    return PlanningTools(
        mcp_client=mcp_client,
    )


def build_planning_workflow() -> PlanningWorkflow:
    settings = get_settings()

    mcp_client = build_planning_mcp_client()

    tools = build_planning_tools(
        mcp_client=mcp_client,
    )

    clock = Clock(
    timezone=settings.timezone,
    )

    tool_registry = {
        "get_upcoming_events": tools.get_upcoming_events,
        "get_events_between": tools.get_events_between,
        "search_events": tools.search_events,
        "check_availability": tools.check_availability,
        "create_event": tools.create_event,
        "update_event": tools.update_event,
        "delete_event": tools.delete_event,
    }

    return PlanningWorkflow(
        model_name=settings.chat_model,
        ollama_host=settings.ollama_host,
        clock=clock,
        tool_registry=tool_registry,
    )