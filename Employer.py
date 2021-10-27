from datetime import datetime
from http import server
class Shift:
  start: datetime
  end: datetime
  place: str
  note: str
  id: str

  def __init__(self, start: datetime, end: datetime, place: str, note: str, id: str='0') -> None:
    self.start = start
    self.end = end
    self.place = place
    self.note = note
    self.id = id
  
  def addToGCal(self, service, calendarId: str):
    event = {
      'start' : {'dateTime' : self.start.strftime("%Y-%m-%dT%H:%M:00+02:00")}, 
      'end' : {'dateTime' : self.end.strftime("%Y-%m-%dT%H:%M:00+02:00")},
      'summary' : "Cinema Work",
      'location' : self.place,
      'description' : self.note
    }
    _ = service.events().insert(calendarId=calendarId, body = event).execute()

  def deleteFromGCal(self, service, calendarId: str):
    _ = service.events().delete(calendarId=calendarId, eventId=self.id)

class Employee:
  id: str
  name: str
  employee_shifts: list
  service : any
  toAdd: list
  toRemove: list
  
  def getShifts(self, start: datetime, end: datetime) -> None:
    '''Fills employer shifts'''
    tmp_list = self.service.calendarList().list().execute()
    calList = tmp_list['items']
    while 'nextPageToken' in tmp_list:
      tmp_list = self.service.calendarList().list(pageToken=tmp_list['nextPageToken']).execute()
      calList += tmp_list['items']
    for cal in calList:
      if cal['summary'] == self.name:
        self.id = cal['id']
        break
    shifts = self.service.events().list(calendarId=self.id, timeMin=start.strftime("%Y-%m-%dT%H:%M:00.000Z"), timeMax=end.strftime("%Y-%m-%dT%H:%M:00.000Z")).execute()
    for item in shifts['items']:
      self.employee_shifts.append(Shift(start = datetime.strptime(item['start']['dateTime'], "%Y-%m-%dT%H:%M:00+02:00"), \
        end = datetime.strptime(item['end']['dateTime'], "%Y-%m-%dT%H:%M:00+02:00"), place = item['location'], note = item['description'], id = item['id']))

  def __init__(self, service, name: str) -> None:
    self.service = service
    self.name = name
    self.id = ""
    self.employee_shifts = []


  def diff(self, o: list) -> list:
    '''Method to compare two objects, returns tab of [toAdd, toRemove]'''
    toAdd = []
    toRemove = []
    for shiftToAdd in o:
      exist = False
      for shift in self.employee_shifts:
        if shiftToAdd.start == shift.start and shiftToAdd.end == shift.end and shiftToAdd.place == shift.place and shiftToAdd.note == shift.note:
          exist = True
      if not exist:
        toAdd.append(shiftToAdd)
    for shiftToRemove in self.employee_shifts:
      exist = False
      for shift in o.employee_shifts:
        if shiftToRemove.start == shift.start and shiftToRemove.end == shift.end and shiftToRemove.place == shift.place and shiftToRemove.note == shift.note:
          exist = True
      if not exist:
        toRemove.append(shiftToRemove)
    self.toAdd = toAdd
    self.toRemove =toRemove
    return [toAdd, toRemove]

  def resolveToAdd(self):
    for shift in self.toAdd:
      shift.addToGCal(self.service, self.id)
