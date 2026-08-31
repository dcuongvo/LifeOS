from lifeos.platform.mcp.client import LifeOSMCPClient


class PlanningTools:
    def __init__(
        self,
        mcp_client: LifeOSMCPClient,
    ) -> None:
        self.mcp_client = mcp_client

    async def get_upcoming_events(
        self,
        limit: int = 10,
    ):
        """
        Get the user's upcoming calendar events.

        Args:
            limit: Maximum number of events to return.
        """

        return await self.mcp_client.call_calendar_tool(
            "get_upcoming_events",
            {
                "limit": limit,
            },
        )

    async def get_events_between(
        self,
        start_time: str,
        end_time: str,
    ):
        """
        Get calendar events within a specific time range.

        Args:
            start_time: Start of the range as an ISO 8601 timestamp.
            end_time: End of the range as an ISO 8601 timestamp.
        """

        return await self.mcp_client.call_calendar_tool(
            "get_events_between",
            {
                "start_time": start_time,
                "end_time": end_time,
            },
        )

    async def search_events(
        self,
        query: str,
        start_time: str | None = None,
        end_time: str | None = None,
        limit: int = 20,
    ):
        """
            Search the user's calendar events by text.

            Args:
                query: Text to search for in calendar events.
                start_time: Optional ISO 8601 start timestamp.
                end_time: Optional ISO 8601 end timestamp.
                limit: Maximum number of matching events to return.
            """

        return await self.mcp_client.call_calendar_tool(
            "search_events",
            {
                "query": query,
                "start_time": start_time,
                "end_time": end_time,
                "limit": limit,
            },
        )

    async def check_availability(
        self,
        start_time: str,
        end_time: str,
    ):
        """
        Check whether the user is available during a specific time range.

        Args:
            start_time: Start of the range as an ISO 8601 timestamp.
            end_time: End of the range as an ISO 8601 timestamp.
        """
        return await self.mcp_client.call_calendar_tool(
            "check_availability",
            {
                "start_time": start_time,
                "end_time": end_time,
            },
        )

    async def create_event(
        self,
        summary: str,
        start_time: str,
        end_time: str,
        description: str | None = None,
        location: str | None = None,
    ):
        """
        Create a calendar event.

        Args:
            summary: Title of the event.
            start_time: Event start as an ISO 8601 timestamp.
            end_time: Event end as an ISO 8601 timestamp.
            description: Optional event description.
            location: Optional event location.
        """
        return await self.mcp_client.call_calendar_tool(
            "create_event",
            {
                "summary": summary,
                "start_time": start_time,
                "end_time": end_time,
                "description": description,
                "location": location,
            },
        )

    async def update_event(
        self,
        event_id: str,
        summary: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        description: str | None = None,
        location: str | None = None,
    ):
        """
        Update an existing calendar event.
        """
        return await self.mcp_client.call_calendar_tool(
            "update_event",
            {
                "event_id": event_id,
                "summary": summary,
                "start_time": start_time,
                "end_time": end_time,
                "description": description,
                "location": location,
            },
        )

    async def delete_event(
        self,
        event_id: str,
    ):
        """
        Delete an existing calendar event.
        """
        return await self.mcp_client.call_calendar_tool(
            "delete_event",
            {
                "event_id": event_id,
            },
        )