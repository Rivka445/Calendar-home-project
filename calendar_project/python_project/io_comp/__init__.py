"""
Comp Calendar Application
"""
"""Top-level package API for the calendar app.

This module exposes a few convenience functions used by the tests and the
simple CLI. The functions are intentionally thin wrappers around the
repository and service layers so tests can call them directly.
"""
from typing import List
from datetime import timedelta
import pandas as pd
"""Top-level package exports for the calendar app.

This module exposes the commonly used domain and repository/service
symbols so callers can import them from `io_comp` directly, e.g.

    from io_comp import Event, Calendar, Person, CalendarRepository

Keep this file small — implementation details live in submodules.
"""

from .models import Event, Calendar, Person
from .repository.repository import CalendarRepository
from .service.service import SchedulerService

__all__ = [
    "Event",
    "Calendar",
    "Person",
    "CalendarRepository",
    "SchedulerService",
]