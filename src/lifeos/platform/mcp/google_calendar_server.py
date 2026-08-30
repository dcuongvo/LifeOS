from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from mcp.server.mcpserver import MCPServer


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
    "https://www.googleapis.com/auth/calendar.readonly",
]


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

    credentials = get_google_credentials()

    service = build(
        "calendar",
        "v3",
        credentials=credentials,
    )

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


if __name__ == "__main__":
    mcp.run()