"""Compatibility shim: legacy `calendar_models` module.

The models have been split into `person.py`, `event.py`, and `calendar.py`.
This module re-exports the same symbols for backward compatibility.
"""
from .event import Event
from .calendar import Calendar
from .person import Person

__all__ = ["Event", "Calendar", "Person"]
