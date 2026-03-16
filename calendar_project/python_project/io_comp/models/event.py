"""Event model."""
from dataclasses import dataclass
from datetime import datetime
from .person import Person


@dataclass(frozen=True)
class Event:
    """Represents a scheduled event with start and end datetimes."""
    start: datetime
    end: datetime
    subject: str
    person: Person
