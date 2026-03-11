from datetime import timedelta
from io_comp import find_available_slots

# Test with 120 minute duration
person_list = ['Alice', 'Jack']
event_duration = timedelta(minutes=120)

result = find_available_slots(person_list, event_duration)

print("Results for 120 minute meeting:")
for slot in result:
    print(f"  {slot}")
