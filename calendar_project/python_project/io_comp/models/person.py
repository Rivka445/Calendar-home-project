"""Person model."""
from typing import Optional


class Person:
    """Represents a person (calendar owner/participant).

    Kept intentionally small so it can be extended later without touching
    other modules. Right now it only stores a `name` and optional `email`.
    """

    def __init__(self, name: str, email: Optional[str] = None):
        self.name = name
        self.email = email

    def __repr__(self) -> str:
        if self.email:
            return f"Person(name={self.name!r}, email={self.email!r})"
        return f"Person(name={self.name!r})"
