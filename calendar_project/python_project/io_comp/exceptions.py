"""Custom exceptions for the calendar application."""


class CalendarError(Exception):
    """Base exception for all calendar errors."""


class PersonNotFoundError(CalendarError):
    """Raised when a participant is not found in the calendar data."""

    def __init__(self, name: str):
        super().__init__(f"Person '{name}' not found in calendar data.")
        self.name = name


class InvalidDurationError(CalendarError):
    """Raised when meeting duration is invalid (zero or negative)."""

    def __init__(self, minutes: int):
        super().__init__(f"Meeting duration must be positive, got {minutes} minutes.")
        self.minutes = minutes


class CSVLoadError(CalendarError):
    """Raised when the CSV file cannot be loaded."""

    def __init__(self, path: str):
        super().__init__(f"Failed to load calendar CSV from '{path}'.")
        self.path = path
