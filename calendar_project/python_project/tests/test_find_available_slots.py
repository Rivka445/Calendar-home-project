import unittest
import pandas as pd
from io import StringIO
import json

from io_comp.repository.repository import CalendarRepository
from io_comp.app import CalendarApp

CSV_DATA = """Alice,"Team sync",09:00,10:00
Alice,"Project review",11:00,12:00
Alice,"One-on-one",15:00,15:30
Bob,"Team sync",09:00,09:30
Bob,"Client call",10:00,11:30
Bob,"Project review",12:00,13:00
Carol,"Morning workout",07:30,08:30
Carol,"Team sync",09:00,10:00
Carol,"Lunch",12:00,12:30
"""

class TestCalendarApp(unittest.TestCase):

    def setUp(self):
        # In-memory CSV
        self.csv_buffer = StringIO(CSV_DATA)

        # Mock repository
        self.repo = CalendarRepository.__new__(CalendarRepository)
        self.repo.csv_path = None

        def get_events_for_participants(participants):
            df = pd.read_csv(self.csv_buffer, header=None)
            df.columns = ["person_name","event_subject","event_start","event_end"]

            events = []
            for _, row in df.iterrows():
                if row["person_name"] not in participants:
                    continue
                # Convert to native python datetimes for consistency
                start = pd.to_datetime(row["event_start"], format="%H:%M").to_pydatetime()
                end = pd.to_datetime(row["event_end"], format="%H:%M").to_pydatetime()
                from io_comp.models import Event, Person
                subject = row["event_subject"]
                person = Person(row["person_name"])
                events.append(Event(start, end, subject=subject, person=person))

            from io_comp.models import Calendar
            return Calendar(events)

        self.repo.get_events_for_participants = get_events_for_participants
        self.app = CalendarApp(self.repo)

    def parse(self, json_output):
        """Return list of slots from JSON"""
        return json.loads(json_output)["available_slots"]

    # ------------------------------------------------

    def test_available_ranges_single_person(self):
        """Correct free time for a single participant with 60 min duration"""
        slots = self.parse(self.app.get_available_slots_json(["Alice"], 60))
        expected = [
            "07:00 - 08:00",
            "10:00",
            "12:00 - 14:00",  
            "15:30 - 18:00" 
        ]
        self.assertEqual(slots, expected)

    # ------------------------------------------------

    def test_shared_availability_two_people(self):
        """Correct shared free time for Alice and Bob with 60 min duration"""
        slots = self.parse(self.app.get_available_slots_json(["Alice", "Bob"], 60))
        expected = [
            "07:00 - 08:00", 
            "13:00 - 14:00",
            "15:30 - 18:00"
        ]
        self.assertEqual(slots, expected)

    # ------------------------------------------------

    def test_no_available_slot_for_long_meeting(self):
        """Empty list if no slot can fit requested duration"""
        slots = self.parse(self.app.get_available_slots_json(["Alice", "Bob", "Carol"], 280))
        expected = []  # no 3-hour slot free for all
        self.assertEqual(slots, expected)

    # ------------------------------------------------

    def test_day_boundaries_respected(self):
        """Slots stay within 07:00 - 19:00"""
        slots = self.parse(self.app.get_available_slots_json(["Carol"], 30))
        for slot in slots:
            if " - " in slot:
                start, end = slot.split(" - ")
            else:
                # single time, treat as start and calculate end from duration
                start = slot
                end = slot  # or handle duration if known
            self.assertGreaterEqual(start, "07:00")
            self.assertLessEqual(end, "18:30")

if __name__ == "__main__":
    unittest.main()