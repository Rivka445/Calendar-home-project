"""Scheduling service: merge intervals and compute available time ranges.

This module contains the business logic for computing available meeting
start times given a `Calendar` (a collection of `Event` objects) and a
requested meeting duration.
"""
import configparser
import os
from datetime import timedelta, datetime
from typing import List
from ..models import Calendar, Event, Person
from ..exceptions import InvalidDurationError

_config = configparser.ConfigParser()
_config.read(os.path.join(os.path.dirname(__file__), "../../resources/config.ini"))


class SchedulerService:
    """Service for scheduling operations on a Calendar instance."""

    WORKDAY_START = _config.get("workday", "start", fallback="07:00")
    WORKDAY_END = _config.get("workday", "end", fallback="19:00")

    def __init__(self, calendar: Calendar):
        """Initialize with a Calendar object.

        Args:
            calendar (Calendar): The calendar containing Event objects.
        """
        self.calendar = calendar

    def merge_intervals(self) -> List[Event]:
        """Merge overlapping events in the calendar.

        Returns:
            List[Event]: List of non-overlapping events sorted by start time.
        """
        if not self.calendar.events:
            return []
        self.calendar.events.sort(key=lambda e: e.start)
        merged = [self.calendar.events[0]]
        for event in self.calendar.events[1:]:
            last = merged[-1]
            if event.start <= last.end:
                merged[-1] = Event(last.start, max(last.end, event.end), last.subject, last.person)
            else:
                merged.append(event)
        return merged

    def find_available_slots(self, meeting_duration: timedelta) -> List[str]:
        """Find all available start-time ranges for a meeting of given duration.

        The method computes gaps between merged events and returns a list of
        human-readable strings describing the earliest start times where a
        meeting of `meeting_duration` would fit.

        Args:
            meeting_duration (timedelta): Desired meeting duration.

        Returns:
            List[str]: Available ranges formatted as 'HH:MM - HH:MM'.
        """
        if meeting_duration.total_seconds() <= 0:
            raise InvalidDurationError(int(meeting_duration.total_seconds() // 60))

        work_start = datetime.strptime(self.WORKDAY_START, "%H:%M")
        work_end = datetime.strptime(self.WORKDAY_END, "%H:%M")

        # Early exit: duration longer than entire workday
        if meeting_duration > work_end - work_start:
            return []

        available_ranges = []
        merged_events = self.merge_intervals()
        previous_end = work_start

        for event in merged_events:
            gap_start = previous_end
            gap_end = event.start
            latest_start = gap_end - meeting_duration
            if latest_start >= gap_start:
                if latest_start == gap_start:
                    available_ranges.append(f"{gap_start.strftime('%H:%M')}")
                else:
                    available_ranges.append(f"{gap_start.strftime('%H:%M')} - {latest_start.strftime('%H:%M')}")
            previous_end = max(previous_end, event.end)
            # Early exit: no time left in workday
            if previous_end >= work_end:
                return available_ranges

        latest_start = work_end - meeting_duration
        if latest_start >= previous_end:
            if latest_start == previous_end:
                available_ranges.append(f"{previous_end.strftime('%H:%M')}")
            else:
                available_ranges.append(f"{previous_end.strftime('%H:%M')} - {latest_start.strftime('%H:%M')}")
        return available_ranges
