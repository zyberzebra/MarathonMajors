import csv

import pandas as pd
from icalendar import Calendar, Event

from marathon_urls import url_dict

# Define constants for date format and column names
DATE_FORMAT = "%d.%m.%Y"
RACE_COL = "Race"
RACE_DATE_COL = "Race Date"
ENTRY_TIME_START_COL = "Entry Time Start"
ENTRY_TIME_END_COL = "Entry Time End"


def create_ical_event(summary, dtstart, dtend, description):
    event = Event()
    event.add('summary', summary)
    event.add('dtstart', dtstart)
    event.add('dtend', dtend)
    event.add('description', description)
    return event


def convert_csv_to_ics(csv_filename, ics_filename):
    with open(csv_filename, 'r') as csv_file:
        csv_data = list(csv.reader(csv_file))

    data_all = [x for x in csv_data if x[0] in ['2024', '2025']]
    df = pd.DataFrame(data_all, columns=csv_data[0])

    cal = Calendar()
    cal.add('prodid', '-//Marathon Major Calendar//')
    cal.add('version', '2.0')

    for index, row in df.iterrows():
        race = row[RACE_COL]
        url = url_dict.get(row[RACE_COL], "")

        # Create an event for the race
        event1 = create_ical_event(f"{race} Marathon",
                                   pd.to_datetime(row[RACE_DATE_COL], format=DATE_FORMAT).date(),
                                   pd.to_datetime(row[RACE_DATE_COL], format=DATE_FORMAT).date(),
                                   url)

        # Add race event to the calendar
        cal.add_component(event1)

        # Check if "Entry Time Start" and "Entry Time End" cells are not empty
        if row[ENTRY_TIME_START_COL] and row[ENTRY_TIME_END_COL]:
            # Create events for the start and end of the entry time
            event2 = create_ical_event(f"Start: Entry {race} Marathon",
                                       pd.to_datetime(row[ENTRY_TIME_START_COL], format=DATE_FORMAT).date(),
                                       pd.to_datetime(row[ENTRY_TIME_START_COL], format=DATE_FORMAT).date(),
                                       url)
            event3 = create_ical_event(f"End: Entry {race} Marathon",
                                       pd.to_datetime(row[ENTRY_TIME_END_COL], format=DATE_FORMAT).date(),
                                       pd.to_datetime(row[ENTRY_TIME_END_COL], format=DATE_FORMAT).date(),
                                       url)

            # Add entry time start/end events to the calendar
            cal.add_component(event2)
            cal.add_component(event3)

        # Rest of your code remains unchanged ...

        # If the "Expected Time Frame" cell has a value
        if row["Expected Time Frame"]:
            expected_times = row["Expected Time Frame"].split("-")
            # Extract month and year from the first date
            start_month, start_year = map(int, expected_times[0].split("."))
            # Create start and end dates for the event
            event_start_date = pd.to_datetime(f"{start_year}-{start_month}-01", format="%Y-%m-%d").date()
            event_end_date = pd.to_datetime(f"{start_year}-{start_month}-03", format="%Y-%m-%d").date()
            # Create an event for the expected time frame
            event4 = create_ical_event(f"Expected Start: Entry {race} Marathon", event_start_date, event_end_date, url)
            # Add the event to the calendar
            cal.add_component(event4)

    # Write the calendar to the ics file
    with open(ics_filename, 'wb') as ics_file:
        ics_file.write(cal.to_ical())


# Run the function
convert_csv_to_ics('majors.csv', 'marathon_majors.ics')