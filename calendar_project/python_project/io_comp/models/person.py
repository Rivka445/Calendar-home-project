"""Person model."""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Person:
    """Represents a person (calendar owner/participant)."""
    name: str
    email: Optional[str] = None
