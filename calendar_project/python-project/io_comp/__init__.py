"""Comp Calendar Exercise - Python Implementation"""

from typing import List, Dict
from datetime import time, timedelta
from .models import Event, PersonCalendar
import pandas as pd
from datetime import datetime

def read_csv(file_name):
    import pandas as pd
    df = pd.read_csv(file_name, header=None)
    df.columns = ['Person name', 'Event subject', 'Event start time', 'Event end time']
    return df

def person_availability(df, person_names) -> Dict[str, PersonCalendar]:
    """Returns a dictionary mapping person names to their PersonCalendar objects."""
    people_calendars = {}
    
    for _, row in df.iterrows():
        person = row['Person name']
        
        if person not in person_names:
            continue
        
        if person not in people_calendars:
            people_calendars[person] = PersonCalendar(person)
        
        event = Event(
            subject=row['Event subject'],
            start=datetime.strptime(row['Event start time'], '%H:%M'),
            end=datetime.strptime(row['Event end time'], '%H:%M')
        )
        people_calendars[person].add_event(event)
    
    return people_calendars

def is_time_slot_available(people_calendars, current_time, event_duration):
    for person in people_calendars:
        people_calendars[person].events = [e for e in people_calendars[person].events if e.start >= current_time]

    for person in people_calendars:
        for event in people_calendars[person].events:
            if(event.start - event_duration >= current_time):
                continue
            else:
                return False
    return True        

def end_time_available(people_calendars, current_time, event_duration):

    for person in people_calendars:
        people_calendars[person].events = [e for e in people_calendars[person].events if e.start >= current_time]

    end_time = datetime.strptime('19:00', '%H:%M') - event_duration

    for person in people_calendars:
        if people_calendars[person].events:
            end_tim_p = people_calendars[person].events[0].start - event_duration
            if end_tim_p < end_time and end_tim_p+ event_duration <= datetime.strptime('19:00', '%H:%M'):
                end_time = end_tim_p

    return end_time

def start_time_available(people_calendars, current_time, event_duration):
    start_time = current_time

    for person in people_calendars:
        for event in people_calendars[person].events:
            if event.start <= start_time < event.end:
                start_time = event.end
                break

    for person in people_calendars:
        people_calendars[person].events = [e for e in people_calendars[person].events if e.end >= start_time]

    return start_time

def find_available(person_list, event_duration):
    available_slots = []
    start_time = datetime.strptime('07:00', '%H:%M')
    end_time =  datetime.strptime('19:00', '%H:%M') - event_duration
    current_time = start_time
    current_end_time = end_time
    bool = True
    while current_time <= end_time:
        if is_time_slot_available(person_list, current_time, event_duration):
            current_end_time = end_time_available(person_list, current_time, event_duration)
            if current_end_time == current_time and bool:
                available_slots.append("Starting Time of available slots: " + current_time.strftime('%H:%M'))
                current_time = current_time + event_duration
                bool = False
            elif current_end_time > current_time:
                available_slots.append("Starting Time of available slots: " + current_time.strftime('%H:%M') + " - " + current_end_time.strftime('%H:%M'))
                current_time = current_end_time
            else:
                current_time = current_time + event_duration
        else:
            new_time = start_time_available(person_list, current_time, event_duration)
            if new_time == current_time:
                current_time += timedelta(minutes=1)
            else:
                current_time = new_time
           
    return available_slots


def find_available_slots(person_list: List[str], event_duration: timedelta) -> List[time]:
    data = read_csv(r"C:\Users\user1\Downloads\calendar_project\calendar_project\python-project\resources\calendar.csv")
    person_availability_list = person_availability(data, person_list)
    available_slots = find_available(person_availability_list, event_duration)
    return available_slots