from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow


PROJECT_ROOT = Path(__file__).resolve().parents[1]

GOOGLE_CALENDAR_SECRET_DIR = (
    PROJECT_ROOT
    / "secrets"
    / "google"
    / "calendar"
)

CREDENTIALS_PATH = (
    GOOGLE_CALENDAR_SECRET_DIR
    / "credentials.json"
)

TOKEN_PATH = (
    GOOGLE_CALENDAR_SECRET_DIR
    / "token.json"
)

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
]


def main() -> None:
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_PATH,
        SCOPES,
    )

    credentials = flow.run_local_server(
        port=0,
    )

    TOKEN_PATH.write_text(
        credentials.to_json()
    )

    print(
        f"Google Calendar token saved to: {TOKEN_PATH}"
    )


if __name__ == "__main__":
    main()