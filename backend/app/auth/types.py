from dataclasses import dataclass


@dataclass
class CurrentUser:
    id: int
    email: str
    auth_id: str | None = None
