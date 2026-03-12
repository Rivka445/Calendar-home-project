"""Scheduling service: merge intervals and compute available time ranges.

This module contains the business logic for computing available meeting
start times given a `Calendar` (a collection of `Event` objects) and a
requested meeting duration.
"""
from datetime import timedelta, datetime
from typing import List
from ..models import Calendar, Event


class SchedulerService:
    """Service for scheduling operations on a Calendar instance.

    Attributes:
        WORKDAY_START (str): Default workday start time as HH:MM string.
        WORKDAY_END (str): Default workday end time as HH:MM string.
    """

    WORKDAY_START = "07:00"
    WORKDAY_END = "19:00"

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
                last.end = max(last.end, event.end)
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
        available_ranges = []
        work_start = datetime.strptime(self.WORKDAY_START, "%H:%M")
        work_end = datetime.strptime(self.WORKDAY_END, "%H:%M")

        merged_events = self.merge_intervals()
        previous_end = work_start

        for event in merged_events:
            gap_start = previous_end
            gap_end = event.start
            latest_start = gap_end - meeting_duration
            if latest_start >= gap_start:
                # If the earliest and latest possible start are identical,
                # present a single start time rather than a range.
                if latest_start == gap_start:
                    available_ranges.append(f"{gap_start.strftime('%H:%M')}")
                else:
                    available_ranges.append(f"{gap_start.strftime('%H:%M')} - {latest_start.strftime('%H:%M')}")
            previous_end = max(previous_end, event.end)

        latest_start = work_end - meeting_duration
        if latest_start >= previous_end:
            if latest_start == previous_end:
                available_ranges.append(f"{previous_end.strftime('%H:%M')}")
            else:
                available_ranges.append(f"{previous_end.strftime('%H:%M')} - {latest_start.strftime('%H:%M')}")
        return available_ranges
