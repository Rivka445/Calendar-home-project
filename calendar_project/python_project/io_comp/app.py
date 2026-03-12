# app.py
import json
import logging
from .repository import CalendarRepository
from .service.service import SchedulerService
from .models import Calendar
from datetime import timedelta

logger = logging.getLogger(__name__)


class CalendarApp:
    def __init__(self, repository: CalendarRepository):
        self.repository = repository

    def run(self, participants, duration_minutes: int):
        calendar = self.repository.get_events_for_participants(participants)
        scheduler = SchedulerService(calendar)
        slots = scheduler.find_available_slots(timedelta(minutes=duration_minutes))
        for slot in slots:
            logger.info("Starting Time of available slots: %s", slot)
        return slots

    def get_available_slots_json(self, participants, duration_minutes: int) -> str:
        """Return available meeting slots in JSON format.

        Args:
            participants (list): List of participant names.
            duration_minutes (int): Duration of the meeting in minutes.

        Returns:
            str: JSON-formatted string of available slots.
        """
        slots = self.run(participants, duration_minutes)
        result = {"participants": participants, "duration_minutes": duration_minutes, "available_slots": slots}
        return json.dumps(result, indent=2)
    
def main():
    # Basic console logging configuration; production code should configure logging centrally
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    repo = CalendarRepository("./resources/calendar.csv")
    app = CalendarApp(repo)
    json_output = app.get_available_slots_json(["Alice", "Jack"], 60)
    print(json_output)


if __name__ == "__main__":
    main()
