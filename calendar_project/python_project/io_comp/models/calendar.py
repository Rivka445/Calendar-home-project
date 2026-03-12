"""Calendar container model."""
from typing import List
from .event import Event


class Calendar:
    """Container for Event objects representing a person's or group's calendar."""

    def __init__(self, events: List[Event] = None):
        self.events = events or []

    def add_event(self, event: Event):
        """Append an Event to this calendar."""
        self.events.append(event)
