import json
import os
from datetime import date, datetime
from typing import List, Optional

from icalendar import Calendar


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def iterate_through_calendars(source_directory: str, target_directory: str):
    events = []
    for file in os.listdir(os.fsencode(source_directory)):
        filename = os.fsdecode(file)
        if filename.endswith(".ics"):
            events.extend(_parse_to_json(os.path.join(source_directory, filename)))
        else:
            continue
    open(f'{target_directory}/events.json', 'w').write(json.dumps(events, default=json_serial))


def _parse_to_json(filename: str) -> List[dict]:
    events = []
    belongs_to = None

    g = open(filename, 'rb')
    gcal = Calendar.from_ical(g.read())
    for component in gcal.walk():
        if component.name == 'VCALENDAR':
            belongs_to = component.get('x-wr-calname')
        if component.name == 'VEVENT':
            event = {
                'belongs_to': belongs_to,
                'summary': component.get('summary'),
                'start': component.get('dtstart').dt,
                'end': component.get('dtend').dt,
                'organizer': _cleanse_emails(component.get('organizer')),
                'attendees': [_cleanse_emails(attendee) for attendee in component.get('attendee')]
                if component.get('attendee') else [],
            }
            events.append(event)
    g.close()
    return events


def _cleanse_emails(email: Optional[str]) -> str:
    return email.replace('mailto:', '') if email else ''
