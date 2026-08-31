from datetime import datetime
from zoneinfo import ZoneInfo


class Clock:
    def __init__(
        self,
        timezone: str,
    ) -> None:
        self.timezone = ZoneInfo(timezone)

    def now(self) -> datetime:
        return datetime.now(self.timezone)

    def iso_now(self) -> str:
        return self.now().isoformat()

    def ensure_timezone(
        self,
        value: str,
    ) -> str:
        dt = datetime.fromisoformat(value)

        if dt.tzinfo is None:
            dt = dt.replace(
                tzinfo=self.timezone,
            )

        return dt.isoformat()