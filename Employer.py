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
      'start' : {'dateTime' : self.start.strftime("%Y-%m-%dT%H:%M:00+01:00")}, 
      'end' : {'dateTime' : self.end.strftime("%Y-%m-%dT%H:%M:00+01:00")},
      'summary' : "Cinema Work",
      'location' : self.place,
      'description' : self.note
    }
    _ = service.events().insert(calendarId=calendarId, body = event).execute()

  def deleteFromGCal(self, service, calendarId: str):
    _ = service.events().delete(calendarId=calendarId, eventId=self.id).execute()

class Employee:
  id: str
  name: str
  employee_google_shifts: list
  employee_kadro_shifts: list
  service : any
  toAdd: list
  toRemove: list

  def getId(self) -> None:
    tmp_list = self.service.calendarList().list().execute()
    calList = tmp_list['items']
    while 'nextPageToken' in tmp_list:
      tmp_list = self.service.calendarList().list(pageToken=tmp_list['nextPageToken']).execute()
      calList += tmp_list['items']
    for cal in calList:
      if cal['summary'] == self.name:
        self.id = cal['id']
        break

  def getGoogleShifts(self, start: datetime, end: datetime) -> None:
    '''Fills employer shifts'''
    if self.id == 0:
      throw("No id")
    shifts = self.service.events().list(calendarId=self.id, timeMin=start.strftime("%Y-%m-%dT%H:%M:00.000Z"), timeMax=end.strftime("%Y-%m-%dT%H:%M:00.000Z")).execute()
    for item in shifts['items']:
      if not 'location' in item or not 'end' in item or not 'start' in item:
        self.toRemove.append(Shift(None, None, None, None, item['id']))
      else:
        note = ""
        if 'description' in item:
          note = item['description']
        self.employee_google_shifts.append(Shift(start = datetime.strptime(item['start']['dateTime'], "%Y-%m-%dT%H:%M:00+01:00"), \
          end = datetime.strptime(item['end']['dateTime'], "%Y-%m-%dT%H:%M:00+01:00"), place = item['location'], note = note, id = item['id']))

  def getKadroShifts(self, all_shifts: dict):
    for id, employee in all_shifts.items():
      if employee['name'] == self.name:
        for shift in employee['schedule']:
          self.employee_kadro_shifts.append(Shift(shift['dtstart'], shift['dtend'], shift['location'], shift['note']))

  def __init__(self, service, name: str, id: str = "") -> None:
    self.service = service
    self.name = name
    self.id = id
    self.employee_google_shifts = []
    self.employee_kadro_shifts = []
    self.toAdd = []
    self.toRemove = []


  def diff(self):
    '''Method to compare two objects, returns tab of [toAdd, toRemove]'''
    for shiftToAdd in self.employee_kadro_shifts:
      exist = False
      for shift in self.employee_google_shifts:
        if shiftToAdd.start == shift.start and shiftToAdd.end == shift.end and shiftToAdd.place == shift.place and shiftToAdd.note == shift.note:
          exist = True
      if not exist:
        self.toAdd.append(shiftToAdd)
    for shiftToRemove in self.employee_google_shifts:
      exist = False
      for shift in self.employee_kadro_shifts:
        if shiftToRemove.start == shift.start and shiftToRemove.end == shift.end and shiftToRemove.place == shift.place and shiftToRemove.note == shift.note:
          exist = True
      if not exist:
        self.toRemove.append(shiftToRemove)
    # return [toAdd, toRemove]

  def resolveChanges(self):
    for shift in self.toAdd:
      shift.addToGCal(self.service, self.id)
    for shift in self.toRemove:
      shift.deleteFromGCal(self.service, self.id)
