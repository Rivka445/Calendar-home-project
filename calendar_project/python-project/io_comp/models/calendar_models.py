from datetime import datetime
from typing import List

class Event:
    def __init__(self, subject: str, start: datetime, end: datetime):
        self.subject = subject
        self.start = start
        self.end = end

class PersonCalendar:
    def __init__(self, name: str):
        self.name = name
        self.events: List[Event] = []
    
    def add_event(self, event: Event):
        self.events.append(event)
        self.events.sort(key=lambda x: x.start)
    
    def remove_event(self, event: Event):
        self.events.remove(event)
