"""Repository layer responsible for loading calendar data from CSV files.

This module provides a thin repository that returns domain `Calendar` objects
consisting of `Event` instances. The CSV is expected to have rows with
columns in the order: person_name, event_subject, event_start, event_end
(time formatted as HH:MM). The repository converts these to `datetime`
instances (same-day) and returns a `Calendar`.
"""
import pandas as pd
from typing import List
from ..models import Event, Calendar, Person
from datetime import datetime


class CalendarRepository:
    """Load events from a CSV file and return a `Calendar`.

    Args:
        csv_path (str): Path to CSV file. The loader expects no header and
            columns in the order: person_name, event_subject, event_start,
            event_end.
    """

    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def get_events_for_participants(self, participants: List[str]) -> Calendar:
        """Return a Calendar containing events for the given participants.

        Args:
            participants (List[str]): Person names to filter by.

        Returns:
            Calendar: Calendar instance with Event objects parsed from CSV.
        """
        df = pd.read_csv(self.csv_path, header=None)
        df.columns = ["person_name", "event_subject", "event_start", "event_end"]
        events = []
        for _, row in df.iterrows():
            if row['person_name'] not in participants:
                continue
            # Parse times formatted as HH:MM on the same reference day
            start = datetime.strptime(row['event_start'], "%H:%M")
            end = datetime.strptime(row['event_end'], "%H:%M")
            person = Person(row['person_name'])
            subject = row['event_subject']
            events.append(Event(start, end, subject, person))
        return Calendar(events)
