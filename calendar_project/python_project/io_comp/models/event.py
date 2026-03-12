"""Event model."""
from datetime import datetime
from .person import Person


class Event:
    """Represents a scheduled event with start and end datetimes.

    Constructor requires start, end, subject and person in this project.
    """

    def __init__(
        self,
        start: datetime,
        end: datetime,
        subject: str,
        person: Person,
    ):
        self.start = start
        self.end = end
        self.subject = subject
        self.person = person

    def __repr__(self) -> str:
        return (
            f"Event("
            f"start={self.start!r}, "
            f"end={self.end!r}, "
            f"subject={self.subject!r}, "
            f"person={self.person!r})"
        )
