import icalendar as ical
from datetime import datetime

cal = ical.Calendar()
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')

def createEvent(location, dateStart, dateEnd):
  event = ical.Event()
  event.add('summary', 'Cinemacity Work')
  event.add('dtstart', dateStart)
  event.add('dtend', dateEnd)
  event['location'] = ical.vText(location)
  cal.add_component(event)

def saveCal():
  with open("cal.ics", 'wb') as f:
    f.write(cal.to_ical())