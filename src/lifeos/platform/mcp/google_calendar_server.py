from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from mcp.server.mcpserver import MCPServer

from lifeos.platform.settings import get_settings
from lifeos.platform.time.clock import Clock


PROJECT_ROOT = Path(__file__).resolve().parents[4]

GOOGLE_CALENDAR_SECRET_DIR = (
    PROJECT_ROOT
    / "secrets"
    / "google"
    / "calendar"
)

TOKEN_PATH = (
    GOOGLE_CALENDAR_SECRET_DIR
    / "token.json"
)

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
]


settings = get_settings()

clock = Clock(
    timezone=settings.timezone,
)

mcp = MCPServer(
    "LifeOS Google Calendar",
)


def get_google_credentials() -> Credentials:
    """
    Load Google OAuth credentials from the saved token.

    If the access token has expired and a refresh token exists,
    refresh it automatically.
    """

    if not TOKEN_PATH.exists():
        raise FileNotFoundError(
            f"Google Calendar token not found: {TOKEN_PATH}"
        )

    credentials = Credentials.from_authorized_user_file(
        TOKEN_PATH,
        SCOPES,
    )

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(
            Request()
        )

        TOKEN_PATH.write_text(
            credentials.to_json()
        )

    return credentials

def get_calendar_service():
    """
    Create an authenticated Google Calendar API service.
    """

    credentials = get_google_credentials()

    return build(
        "calendar",
        "v3",
        credentials=credentials,
    )

@mcp.tool()
def get_upcoming_events(
    limit: int = 10,
) -> list[dict]:
    """
    Get the user's upcoming Google Calendar events.

    Args:
        limit: Maximum number of upcoming events to return.

    Returns:
        A list of upcoming calendar events.
    """

    service = get_calendar_service()

    now = datetime.now(
        timezone.utc
    ).isoformat()

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=limit,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get(
        "items",
        [],
    )

    return [
        {
            "id": event.get("id"),
            "summary": event.get(
                "summary",
                "(No title)",
            ),
            "start": event["start"].get(
                "dateTime",
                event["start"].get("date"),
            ),
            "end": event["end"].get(
                "dateTime",
                event["end"].get("date"),
            ),
        }
        for event in events
    ]


@mcp.tool()
def get_events_between(
    start_time: str,
    end_time: str,
) -> list[dict]:
    """
    Get calendar events between two timestamps.

    Args:
        start_time: Start of the time range as an ISO 8601 timestamp.
        end_time: End of the time range as an ISO 8601 timestamp.

    Returns:
        A list of calendar events that occur within the given time range.
    """

    start_time = clock.ensure_timezone(
        start_time
    )

    end_time = clock.ensure_timezone(
        end_time
    )

    service = get_calendar_service()

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get(
        "items",
        [],
    )

    return [
        {
            "id": event.get("id"),
            "summary": event.get(
                "summary",
                "(No title)",
            ),
            "start": event["start"].get(
                "dateTime",
                event["start"].get("date"),
            ),
            "end": event["end"].get(
                "dateTime",
                event["end"].get("date"),
            ),
        }
        for event in events
    ]


@mcp.tool()
def search_events(
    query: str,
    start_time: str | None = None,
    end_time: str | None = None,
    limit: int = 20,
) -> list[dict]:
    """
    Search the user's Google Calendar events by text.

    Args:
        query: Text to search for in calendar events.
        start_time: Optional ISO 8601 start timestamp.
        end_time: Optional ISO 8601 end timestamp.
        limit: Maximum number of matching events to return.

    Returns:
        A list of matching calendar events.
    """

    service = get_calendar_service()

    request_args = {
        "calendarId": "primary",
        "q": query,
        "maxResults": limit,
        "singleEvents": True,
        "orderBy": "startTime",
    }

    if start_time is not None:
        request_args["timeMin"] = (
            clock.ensure_timezone(
                start_time
            )
        )

    if end_time is not None:
        request_args["timeMax"] = (
            clock.ensure_timezone(
                end_time
            )
        )

    events_result = (
        service.events()
        .list(**request_args)
        .execute()
    )

    events = events_result.get(
        "items",
        [],
    )

    return [
        {
            "id": event.get("id"),
            "summary": event.get(
                "summary",
                "(No title)",
            ),
            "description": event.get(
                "description",
            ),
            "location": event.get(
                "location",
            ),
            "start": event["start"].get(
                "dateTime",
                event["start"].get("date"),
            ),
            "end": event["end"].get(
                "dateTime",
                event["end"].get("date"),
            ),
        }
        for event in events
    ]


@mcp.tool()
def check_availability(
    start_time: str,
    end_time: str,
) -> dict:
    """
    Check whether the user's primary calendar is busy
    during a specific time range.

    Args:
        start_time: Start of the time range as an ISO 8601 timestamp.
        end_time: End of the time range as an ISO 8601 timestamp.

    Returns:
        Availability information including busy periods.
    """

    start_time = clock.ensure_timezone(
        start_time
    )

    end_time = clock.ensure_timezone(
        end_time
    )

    service = get_calendar_service()

    result = (
        service.freebusy()
        .query(
            body={
                "timeMin": start_time,
                "timeMax": end_time,
                "items": [
                    {
                        "id": "primary",
                    }
                ],
            }
        )
        .execute()
    )

    busy_periods = (
        result
        .get("calendars", {})
        .get("primary", {})
        .get("busy", [])
    )

    return {
        "start": start_time,
        "end": end_time,
        "is_available": len(busy_periods) == 0,
        "busy_periods": busy_periods,
    }


@mcp.tool()
def create_event(
    summary: str,
    start_time: str,
    end_time: str,
    description: str | None = None,
    location: str | None = None,
) -> dict:
    """
    Create a Google Calendar event.

    Args:
        summary: Title of the event.
        start_time: Event start as an ISO 8601 timestamp.
        end_time: Event end as an ISO 8601 timestamp.
        description: Optional event description.
        location: Optional event location.

    Returns:
        The created calendar event.
    """

    start_time = clock.ensure_timezone(
        start_time
    )

    end_time = clock.ensure_timezone(
        end_time
    )

    service = get_calendar_service()

    event_body = {
        "summary": summary,
        "start": {
            "dateTime": start_time,
        },
        "end": {
            "dateTime": end_time,
        },
    }

    if description is not None:
        event_body["description"] = description

    if location is not None:
        event_body["location"] = location

    created_event = (
        service.events()
        .insert(
            calendarId="primary",
            body=event_body,
        )
        .execute()
    )

    return {
        "id": created_event.get("id"),
        "summary": created_event.get("summary"),
        "description": created_event.get("description"),
        "location": created_event.get("location"),
        "start": created_event["start"].get(
            "dateTime",
            created_event["start"].get("date"),
        ),
        "end": created_event["end"].get(
            "dateTime",
            created_event["end"].get("date"),
        ),
        "html_link": created_event.get("htmlLink"),
    }

@mcp.tool()
def update_event(
    event_id: str,
    summary: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    description: str | None = None,
    location: str | None = None,
) -> dict:
    """
    Update an existing Google Calendar event.
    The event_id should come from a previously identified calendar event.
    Do not use this tool until the intended event is unambiguous.
    Args:
        event_id: Google Calendar event ID.
        summary: Optional new event title.
        start_time: Optional new start time as an ISO 8601 timestamp.
        end_time: Optional new end time as an ISO 8601 timestamp.
        description: Optional new event description.
        location: Optional new event location.

    Returns:
        The updated calendar event.
    """

    service = get_calendar_service()

    existing_event = (
        service.events()
        .get(
            calendarId="primary",
            eventId=event_id,
        )
        .execute()
    )

    if summary is not None:
        existing_event["summary"] = summary

    if start_time is not None:
        start_time = clock.ensure_timezone(
            start_time
        )

        existing_event["start"] = {
            "dateTime": start_time,
        }

    if end_time is not None:
        end_time = clock.ensure_timezone(
            end_time
        )

        existing_event["end"] = {
            "dateTime": end_time,
        }

    if description is not None:
        existing_event["description"] = description

    if location is not None:
        existing_event["location"] = location

    updated_event = (
        service.events()
        .update(
            calendarId="primary",
            eventId=event_id,
            body=existing_event,
        )
        .execute()
    )

    return {
        "id": updated_event.get("id"),
        "summary": updated_event.get("summary"),
        "description": updated_event.get("description"),
        "location": updated_event.get("location"),
        "start": updated_event["start"].get(
            "dateTime",
            updated_event["start"].get("date"),
        ),
        "end": updated_event["end"].get(
            "dateTime",
            updated_event["end"].get("date"),
        ),
        "html_link": updated_event.get("htmlLink"),
    }

@mcp.tool()
def delete_event(
    event_id: str,
) -> dict:
    """
    Delete an existing Google Calendar event.

    The event_id should refer to the exact event to delete.
    """

    service = get_calendar_service()

    service.events().delete(
        calendarId="primary",
        eventId=event_id,
    ).execute()

    return {
        "deleted": True,
        "event_id": event_id,
    }

if __name__ == "__main__":
    mcp.run()